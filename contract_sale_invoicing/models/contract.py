# Copyright 2018 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.osv import expression


class ContractContract(models.Model):
    _inherit = "contract.contract"

    invoicing_sales = fields.Boolean(
        string="Invoice Pending Sales Orders",
        help="If checked include sales with same analytic account to invoice "
        "in contract invoice creation.",
    )

    def _get_invoiceable_sales_domain(self):
        self.ensure_one()
        return [
            (
                "order_line.distribution_analytic_account_ids",
                "in",
                self.group_id.ids,
            ),
            (
                "partner_invoice_id",
                "child_of",
                self.partner_id.commercial_partner_id.ids,
            ),
            ("invoice_status", "=", "to invoice"),
            (
                "date_order",
                "<=",
                f"{self.recurring_next_date} 23:59:59",
            ),
        ]

    def _get_matching_analytic_account_sales(self, possible_sales):
        """
        Only match Sales with exact analytic account: 100% distribution on all lines
        """
        self.ensure_one()
        return possible_sales.filtered(
            lambda order, analytic_account_id=str(self.group_id.id): all(
                line.analytic_distribution == {analytic_account_id: 100.0}
                for line in order.order_line
            )
        )

    def _recurring_create_invoice(self, date_ref=False):
        """
        When creating invoices, add pending Sale Orders with same Analytic Account
        """
        invoices = super()._recurring_create_invoice(date_ref)
        affected_contracts = self.filtered(
            lambda c: c.invoicing_sales and c.recurring_next_date
        )
        sale_domain = expression.OR(
            [c._get_invoiceable_sales_domain() for c in affected_contracts]
        )
        all_sales = self.env["sale.order"].search(sale_domain)
        for contract in affected_contracts:
            possible_sales = all_sales.filtered_domain(
                contract._get_invoiceable_sales_domain()
            )
            sales = contract._get_matching_analytic_account_sales(possible_sales)
            if sales:
                invoices |= sales._create_invoices()
        return invoices
