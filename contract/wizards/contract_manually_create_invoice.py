# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ContractManuallyCreateInvoice(models.TransientModel):

    _name = 'contract.manually.create.invoice'
    _description = 'Contract Manually Create Invoice Wizard'

    invoice_date = fields.Date(string="Invoice Date", required=True)
    contract_to_invoice_count = fields.Integer(
        compute="_compute_contract_to_invoice_count"
    )

    @api.multi
    def action_show_contract_to_invoice(self):
        self.ensure_one()
        if not self.invoice_date:
            contract_to_invoice_domain = [('id', '=', False)]
        else:
            contract_to_invoice_domain = self.env[
                'contract.contract'
            ]._get_contracts_to_invoice_domain(self.invoice_date)

        return {
            "type": "ir.actions.act_window",
            "name": _("Contracts to invoice"),
            "res_model": "contract.contract",
            "domain": contract_to_invoice_domain,
            "view_mode": "tree,form",
            "context": self.env.context,
        }

    @api.depends('invoice_date')
    def _compute_contract_to_invoice_count(self):
        self.ensure_one()
        if not self.invoice_date:
            self.contract_to_invoice_count = 0
        else:
            contract_model = self.env['contract.contract']
            self.contract_to_invoice_count = contract_model.search_count(
                contract_model._get_contracts_to_invoice_domain(
                    self.invoice_date
                )
            )

    @api.multi
    def create_invoice(self):
        self.ensure_one()
        contract_model = self.env['contract.contract']
        contracts = contract_model.search(
            contract_model._get_contracts_to_invoice_domain(self.invoice_date)
        )
        invoices = contract_model.cron_recurring_create_invoice(
            self.invoice_date
        )
        for contract in contracts:
            contract.message_post(
                body=_("Manually invoiced. Invoice date: %s")
                % self.invoice_date
            )
        return {
            "type": "ir.actions.act_window",
            "name": _("Invoices"),
            "res_model": "account.invoice",
            "domain": [('id', 'in', invoices.ids)],
            "view_mode": "tree,form",
            "context": self.env.context,
        }
