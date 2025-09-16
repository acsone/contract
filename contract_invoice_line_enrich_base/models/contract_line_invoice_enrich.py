# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ContractLineInvoiceEnrich(models.Model):
    _name = "contract.line.invoice.enrich"
    _description = "Contract Line Enrich Invoice"

    # Reference fields
    contract_line_id = fields.Many2one("contract.line")
    ref = fields.Char("Reference", help="Reference to match a contract line")
    # Modules can add types to manage various use-cases, eg Timesheets
    line_type = fields.Selection([], help="Type of invoice line")

    # Enrichment fields
    name = fields.Char(help="Title of invoice line")
    quantity = fields.Float()
    product_uom_id = fields.product_uom_id = fields.Many2one(comodel_name="uom.uom")
    discount = fields.Float()
    price_unit = fields.Float(digits="Product Price")
    product_id = fields.Many2one(comodel_name="product.product")

    def write(self, vals):
        if ref := vals.get("ref"):
            if contract_line := self.env["contract.line"].search(
                [
                    ("invoice_enrich_ref", "=", ref),
                ],
                limit=1,
            ):
                vals["contract_line_id"] = contract_line.id
        return super().write(vals)

    def enrich_invoice_vals(self, invoice_vals):
        """
        Use the current record self to enrich invoice vals
        """
        self.ensure_one()
        return invoice_vals.update(
            {
                "name": self.name,
            }
        )
