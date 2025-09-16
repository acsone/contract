# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class Contract(models.Model):
    _inherit = "contract.contract"

    def _prepare_invoice_line_values(self, contract_lines):
        invoice_lines_vals = super()._prepare_invoice_line_values(contract_lines)
        enriched_invoice_line_vals = []
        sequence = 0
        for vals in invoice_lines_vals.sort(key=lambda v: v["sequence"]):
            sequence += 1
            enrich_lines = self.env["contract.line.invoice.enrich"].search(
                [("contract_line_id", "=", vals.get("contract_line_id"))]
            )
            if enrich_lines:
                # Create an invoice line for each enrich-record, taking the main
                # vals as base and add values
                for enrich_line in enrich_lines:
                    sequence += 1
                    enrich_vals = enrich_line.enrich_invoice_vals(vals)
                    enrich_vals["sequence"] = sequence
                    enriched_invoice_line_vals.append(enrich_vals)
            else:
                # Nothing to add, pass on origin vals
                vals["sequence"] = sequence
                enriched_invoice_line_vals.append(vals)

        return enriched_invoice_line_vals
