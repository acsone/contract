# Copyright 2024 ACSONE SA/NV.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    contract_line_ids = fields.One2many(
        comodel_name="contract.line",
        inverse_name="sale_order_line_id",
    )

    @api.depends("contract_line_ids")
    def _compute_invoice_status(self):
        contract_order_lines = self.filtered("contract_line_ids")
        contract_order_lines.update({"invoice_status": "no"})
        super(SaleOrderLine, self - contract_order_lines)._compute_invoice_status()
