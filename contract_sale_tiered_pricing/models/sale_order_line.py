# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models

from odoo.addons import decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    contract_cumulated_qty = fields.Float(
        string="Contract Cumulated Quantity",
        help="This takes into account all products with a running contract line",
        digits=dp.get_precision("Product Unit of Measure"),
        compute="_compute_contract_cumulated_qty",
        required=True,
        default=0,
        store=True,
    )

    @api.depends("product_uom", "product_id", "order_id.partner_id")
    def _compute_contract_cumulated_qty(self):
        for line in self:
            uom = line.product_uom
            domain = [
                ("product_id", "=", line.product_id.id),
                ("contract_id.partner_id", "=", line.order_id.partner_id.id),
                ("state", "in", ["in-progress", "upcoming-close"]),
            ]
            lines = self.env["contract.line"].search(domain)
            get_qty = lambda l: l.uom_id._compute_quantity(l.quantity, uom)  # noqa
            line.contract_cumulated_qty = sum(lines.mapped(get_qty))

    def get_sale_order_line_multiline_description_sale(self, product):
        """Enrich the description with the tier computation.
        """
        if self.is_tier_priced and self.product_uom_qty and self.contract_cumulated_qty:
            context = {"lang": self.order_id.partner_id.lang}  # noqa  # used by _ below
            qty = self.product_uom_qty
            self.product_uom_qty = self.contract_cumulated_qty + qty
            res = super(
                SaleOrderLine, self
            ).get_sale_order_line_multiline_description_sale(product)
            self.product_uom_qty = qty
            history_message = _("Already paid: {}").format(self.contract_cumulated_qty)
            res = "\n".join([res, history_message])
        else:
            res = super(
                SaleOrderLine, self
            ).get_sale_order_line_multiline_description_sale(product)
        return res

    def _get_display_price(self, product):
        if self.is_tier_priced and self.product_uom_qty and self.contract_cumulated_qty:
            ccq = self.contract_cumulated_qty
            qty = self.product_uom_qty
            product_ccq = product.with_context(quantity=ccq)
            ccq_price = super(SaleOrderLine, self)._get_display_price(product_ccq)
            product.invalidate_cache(fnames=["price"], ids=product.ids)
            product_total = product.with_context(quantity=ccq + qty)
            total_price = super(SaleOrderLine, self)._get_display_price(product_total)
            price = ((total_price * (ccq + qty)) - (ccq * ccq_price)) / qty
        else:
            price = super(SaleOrderLine, self)._get_display_price(product)
        return price
