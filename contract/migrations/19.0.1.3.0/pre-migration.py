# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tools import parse_version


def migrate(cr, version):
    # fields exist since this version
    if parse_version(version) < parse_version("19.0.1.0.6"):
        return
    cr.execute(
        """
        ALTER TABLE contract_contract
        RENAME COLUMN invoice_generation_error TO last_generation_error
        """
    )
    cr.execute(
        """
        ALTER TABLE contract_contract
        RENAME COLUMN invoice_generation_error_date TO last_generation_error_date
        """
    )
