# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ContractContract(models.Model):
    _inherit = "contract.contract"

    is_manually_invoiced = fields.Boolean(
        "Manually Invoiced",
        help="The contract will be excluded from the automated invoice creation. "
        "It can be invoiced manually via Accounting > Customers/Vendors > "
        "Manually Invoice Sale/Purchase Contracts",
    )

    def _get_contracts_to_invoice_domain(self, date_ref=None):
        """
        Exclude manually invoiced contracts
        """
        domain = super()._get_contracts_to_invoice_domain(date_ref)
        domain.extend([("is_manually_invoiced", "=", False)])
        return domain
