# Copyright 2017 LasLabs Inc.
# Copyright 2018 ACSONE SA/NV.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    contract_count = fields.Integer(compute="_compute_contract_count")

    @api.depends("order_line")
    def _compute_contract_count(self):
        # we don't support counting contract counts for multiple sale orders
        self.ensure_one()
        self.contract_count = len(
            self.env["contract.line"]
            .search([("sale_order_line_id", "in", self.order_line.ids)])
            .mapped("contract_id")
        )

    def action_show_contracts(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "contract.action_customer_contract"
        )

        contracts = (
            self.env["contract.line"]
            .search([("sale_order_line_id", "in", self.order_line.ids)])
            .mapped("contract_id")
        )
        action["domain"] = [
            ("contract_line_ids.sale_order_line_id", "in", self.order_line.ids)
        ]
        if len(contracts) == 1:
            # If there is only one contract, open it directly
            action.update(
                {
                    "res_id": contracts.id,
                    "view_mode": "form",
                    "views": filter(lambda view: view[1] == "form", action["views"]),
                }
            )
        return action
