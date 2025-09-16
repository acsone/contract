# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    is_invoice_enrich = fields.Boolean(
        "Enrich Invoice",
        help="Enrichment lines that are linked via the Reference will be exploded "
        "into multiple invoice lines",
    )
    invoice_enrich_ref = fields.Char("Invoice Enrichment Reference")

    _sql_constraints = [
        (
            "invoice_enrich_ref_unique",
            "unique(invoice_enrich_ref)",
            "This Enrich Ref already exists",
        )
    ]
