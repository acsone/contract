# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.contract.tests.test_contract import TestContractBase
from odoo.addons.queue_job.tests.common import trap_jobs


class TestContractQueueJob(TestContractBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["ir.config_parameter"].sudo().set_param("contract.queue.job", True)
        cls.contract3 = cls.contract2.copy()

    def _get_related_invoices(self, contracts):
        return (
            self.env["account.move.line"]
            .search([("contract_line_id", "in", contracts.contract_line_ids.ids)])
            .mapped("move_id")
        )

    def test_contract_queue_job(self):
        contracts = self.contract2 | self.contract3
        with trap_jobs() as trap:
            invoices = contracts._recurring_create_invoice()
            self.assertFalse(invoices)
            invoices = self._get_related_invoices(contracts)
            self.assertFalse(invoices)
            self.assertEqual(trap.jobs_count(), 2)
            trap.assert_enqueued_job(
                self.contract2._recurring_create_invoice, kwargs={"date_ref": False}
            )
            trap.assert_enqueued_job(
                self.contract3._recurring_create_invoice, kwargs={"date_ref": False}
            )
            trap.perform_enqueued_jobs()
            invoices = self._get_related_invoices(contracts)
            self.assertEqual(len(invoices), 2)

    def test_contract_queue_job_1(self):
        contracts = self.contract2
        with trap_jobs() as trap:
            invoices = contracts._recurring_create_invoice()
            self.assertEqual(trap.jobs_count(), 0)
            self.assertEqual(len(invoices), 1)
            invoices = self._get_related_invoices(contracts)
            self.assertEqual(len(invoices), 1)

    def test_contract_queue_job_2(self):
        contracts = self.contract2 | self.contract3
        wizard = self.env["contract.manually.create.invoice"].create(
            [{"invoice_date": self.today, "contract_type": "sale"}]
        )
        with trap_jobs() as trap:
            wizard.create_invoice_queued()
            invoices = contracts._recurring_create_invoice()
            self.assertFalse(invoices)
            invoices = self._get_related_invoices(contracts)
            self.assertFalse(invoices)
            trap.assert_enqueued_job(
                self.contract2._recurring_create_invoice, kwargs={"date_ref": False}
            )
            trap.assert_enqueued_job(
                self.contract3._recurring_create_invoice, kwargs={"date_ref": False}
            )
            trap.perform_enqueued_jobs()
            invoices = self._get_related_invoices(contracts)
            self.assertEqual(len(invoices), 2)

    def test_contract_queue_job_3(self):
        """wrong ir_config_parameter : no job"""
        self.env["ir.config_parameter"].sudo().set_param(
            "contract.queue.job", "wronginput"
        )
        contracts = self.contract2 | self.contract3
        job_counter = self.job_counter()
        contracts._recurring_create_invoice()
        self.assertEqual(job_counter.count_created(), 0)
