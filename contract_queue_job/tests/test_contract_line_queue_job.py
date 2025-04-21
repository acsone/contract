# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields

from odoo.addons.contract.tests.test_contract import TestContractBase
from odoo.addons.queue_job.tests.common import JobMixin, trap_jobs


class TestContractLineQueueJob(TestContractBase, JobMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.contract3 = cls.contract2.copy()

    def test_contract_renew_queue_job_1(self):
        """Only one line, task is run without delay"""
        line = self.contract2.contract_line_ids
        line.date_end = fields.Date.today()
        with trap_jobs() as trap:
            line.renew()
            self.assertEqual(trap.jobs_count(), 0)
        self.assertNotEqual(line.date_end, fields.Date.today())

    def test_contract_renew_queue_job_2(self):
        """Two lines, two jobs are created."""
        contracts = self.contract2 | self.contract3
        lines = contracts.contract_line_ids
        with trap_jobs() as trap:
            lines.renew()
            self.assertEqual(trap.jobs_count(), 2)
            trap.assert_enqueued_job(lines[0].renew)
            trap.assert_enqueued_job(lines[1].renew)
