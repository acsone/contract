# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ContractLine(models.Model):
    _inherit = "contract.line"

    def _prepare_sale_line_vals(self, dates, order_id=False):
        res = super()._prepare_sale_line_vals(dates=dates, order_id=order_id)
        res.update(
            {
                "show_details": self.show_details,
                "show_subtotal": self.show_subtotal,
                "show_line_amount": self.show_line_amount,
            }
        )
        return res
