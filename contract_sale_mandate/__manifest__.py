# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Contract Sale Mandate',
    'summary': """
        This addon manages the banking mandate from the sale order to the
        contract.""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'ACSONE SA/NV,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/contract',
    'depends': [
        # OCA/bank-payment
        'account_banking_mandate',
        'account_banking_mandate_sale',
        # OCA/contract
        'contract',
        'contract_mandate',
    ],
    'data': [
    ],
    'demo': [
    ],
}
