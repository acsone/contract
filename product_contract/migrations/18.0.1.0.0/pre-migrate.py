# Copyright 2025 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from openupgradelib import openupgrade


def migrate(cr, version):
    openupgrade.rename_fields(
        cr,
        [
            (
                "product.template",
                "product_template",
                "default_qty",
                "recurrence_number",
            )
        ],
    )
