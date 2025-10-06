# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import timedelta

from odoo.exceptions import ValidationError

from odoo.addons.contract.tests.test_contract import (
    TestContractBase,
)


class TestContractRefund(TestContractBase):
    def _get_contract_invoices(self):
        return self.env["account.move"].search(
            [("line_ids.contract_line_id", "in", self.contract.contract_line_ids.ids)]
        )

    def test_0(self):
        """
        standard behavior
        stop before last date invoiced, company setting disabled, validationError raises
        """
        self.contract.recurring_create_invoice()
        with self.assertRaisesRegex(
            ValidationError,
            "You can't have the end date before the date of last invoice",
        ):
            self.acct_line.stop(self.acct_line.last_date_invoiced - timedelta(days=1))

    def test_1(self):
        """
        stop create a refund for the invoiced period
        if the company setting is enabled and the stop is before the last date invoiced
        a refund is created
        """
        self.contract.company_id.enable_contract_line_refund_on_stop = True
        self.contract.recurring_create_invoice()
        self.assertEqual(len(self._get_contract_invoices()), 1)
        self.acct_line.stop(self.acct_line.last_date_invoiced - timedelta(days=1))
        self.assertEqual(len(self._get_contract_invoices()), 2)
        refund = self._get_contract_invoices().filtered(
            lambda m: m.move_type == "out_refund"
        )
        self.assertTrue(refund)
        refund_line = refund.invoice_line_ids
        self.assertEqual(refund_line.product_id, self.acct_line.product_id)
        self.assertEqual(refund_line.quantity, 1)
        self.assertEqual(refund_line.name, "Refund for period 02/13/2018 02/14/2018")

    def test_2(self):
        """
        no refund if the stop is after the last date invoiced
        """
        self.contract.company_id.enable_contract_line_refund_on_stop = True
        self.contract.recurring_create_invoice()
        self.assertEqual(len(self._get_contract_invoices()), 1)
        self.acct_line.stop(self.acct_line.last_date_invoiced + timedelta(days=1))
        self.assertEqual(len(self._get_contract_invoices()), 1)
