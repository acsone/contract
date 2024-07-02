# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Contract Sale Order",
    "summary": """
        Link contracts to sale orders""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/contract",
    "depends": [
        "contract",
        "sale",
    ],
    "excludes": [
        # This module is actually a subset of product_contract. In the future we
        # may consider refactoring product_contract to depend on this module.
        "product_contract",
    ],
    "data": [
        "views/contract.xml",
        "views/contract_line.xml",
        "views/sale_order.xml",
    ],
    "demo": [],
}
