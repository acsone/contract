# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order"

    def recompute_contract_cumulated_qty(self):
        draft_orders = self.filtered(lambda s: s.state == "draft")
        for line in draft_orders.mapped("order_line"):
            old_qty = line.contract_cumulated_qty
            line._compute_contract_cumulated_qty()
            if line.contract_cumulated_qty != old_qty:
                line._get_display_price(line.product_id)
