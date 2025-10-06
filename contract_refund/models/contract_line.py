# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, _, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    def stop(self, date_end, manual_renew_needed=False, post_message=True):
        for rec in self:
            if (
                not rec.company_id.enable_contract_line_refund_on_stop
                or not rec.last_date_invoiced
                or rec.last_date_invoiced <= date_end
            ):
                continue
            rec._create_refund(
                to_refund_start_date=date_end,
                to_refund_end_date=rec.last_date_invoiced,
            )
            rec.last_date_invoiced = date_end
        return super().stop(
            date_end, manual_renew_needed=manual_renew_needed, post_message=post_message
        )

    def _create_refund(self, to_refund_start_date, to_refund_end_date):
        invoice_vals = self.contract_id._prepare_invoice(to_refund_start_date)
        move_type = (
            "in_refund" if invoice_vals["move_type"] == "in_invoice" else "out_refund"
        )
        invoice_vals["move_type"] = move_type
        invoice_vals["invoice_line_ids"] = [
            Command.create(
                self._prepare_refund_line(to_refund_start_date, to_refund_end_date)
            )
        ]
        self.env["account.move"].create(invoice_vals)

    def _prepare_refund_vals(self, to_refund_start_date, to_refund_end_date):
        refund_vals = self.contract_id._prepare_invoice(to_refund_start_date)
        move_type = (
            "in_refund" if refund_vals["move_type"] == "in_invoice" else "out_refund"
        )
        refund_vals["move_type"] = move_type
        refund_vals["invoice_line_ids"] = [
            Command.create(
                self._prepare_refund_line(to_refund_start_date, to_refund_end_date)
            )
        ]
        return refund_vals

    def _prepare_refund_line(self, to_refund_start_date, to_refund_end_date):
        line_vals = self._prepare_invoice_line()
        line_vals["name"] = self._get_refund_line_name(
            to_refund_start_date, to_refund_end_date
        )
        return line_vals

    def _get_refund_line_name(self, to_refund_start_date, to_refund_end_date):
        lang = self.env["res.lang"].search(
            [("code", "=", self.contract_id.partner_id.lang)]
        )
        date_format = lang.date_format or "%m/%d/%Y"
        return _(
            "Refund for period %(to_refund_start_date)s %(to_refund_end_date)s"
        ) % (
            dict(
                to_refund_start_date=to_refund_start_date.strftime(date_format),
                to_refund_end_date=to_refund_end_date.strftime(date_format),
            )
        )
