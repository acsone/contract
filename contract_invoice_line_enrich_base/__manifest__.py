# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Contract Invoice Line Enrich Base",
    "summary": "Base module for detailed invoice lines coming from one contract line",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/contract",
    "depends": [
        "contract",
    ],
    "data": [
        "security/contract_line_invoice_enrich.xml",
        "views/contract_line_invoice_enrich.xml",
    ],
    "demo": [],
}
