# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.fields import Command


class ContractLine(models.Model):
    _inherit = "contract.line"

    sale_order_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        string="Sale Order Line",
        ondelete="restrict",
        check_company=True,
    )

    def _prepare_invoice_line(self):
        res = super()._prepare_invoice_line()
        res["sale_line_ids"] = [Command.link(self.sale_order_line_id.id)]
        return res
