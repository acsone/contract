# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Contract(models.Model):
    _inherit = "contract.contract"

    sale_order_count = fields.Integer(compute="_compute_sale_order_count")

    @api.depends("contract_line_ids")
    def _compute_sale_order_count(self):
        self.ensure_one()
        self.sale_order_count = len(
            self.contract_line_ids.mapped("sale_order_line_id.order_id")
        )

    def action_show_sale_orders(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id("sale.action_orders")

        sale_orders = self.contract_line_ids.mapped("sale_order_line_id.order_id")
        action["domain"] = [("id", "in", sale_orders.ids)]
        if len(sale_orders) == 1:
            # If there is only one sale order, open it directly
            action.update(
                {
                    "res_id": sale_orders.id,
                    "view_mode": "form",
                    "views": filter(lambda view: view[1] == "form", action["views"]),
                }
            )
        return action
