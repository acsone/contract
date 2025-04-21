# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ContractContract(models.Model):
    _inherit = "contract.contract"

    def _recurring_create_invoice(self, date_ref=False):
        res = self.env["account.move"]
        if len(self) > 1:
            for rec in self:
                rec.with_delay()._recurring_create_invoice(date_ref=date_ref)
            return res
        return super()._recurring_create_invoice(date_ref=date_ref)
