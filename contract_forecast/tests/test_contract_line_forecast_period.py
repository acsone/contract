# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo.addons.contract.tests.test_contract import TestContractBase
from odoo.fields import Date
from odoo.tools import mute_logger


class TestContractLineForecastPeriod(TestContractBase):
    @mute_logger("odoo.addons.queue_job.models.base")
    def setUp(self):
        self.env = self.env(
            context=dict(self.env.context, test_queue_job_no_delay=True)
        )
        super(TestContractLineForecastPeriod, self).setUp()
        self.line_vals["date_start"] = Date.context_today(self.acct_line)
        self.line_vals["recurring_next_date"] = Date.context_today(
            self.acct_line
        )
        self.acct_line = self.env["account.analytic.invoice.line"].create(
            self.line_vals
        )

    @mute_logger("odoo.addons.queue_job.models.base")
    def test_forecast_period_creation(self):
        self.assertTrue(self.acct_line.forecast_period_ids)
        self.assertEqual(len(self.acct_line.forecast_period_ids), 13)

    @mute_logger("odoo.addons.queue_job.models.base")
    def test_forecast_period_on_contract_line_update_1(self):
        self.acct_line.write({"recurring_rule_type": "yearly"})
        self.assertTrue(self.acct_line.forecast_period_ids)
        self.assertEqual(len(self.acct_line.forecast_period_ids), 2)

    @mute_logger("odoo.addons.queue_job.models.base")
    def test_forecast_period_on_contract_line_update_2(self):
        self.acct_line.stop(
            Date.context_today(self.acct_line) + relativedelta(months=6)
        )
        self.assertTrue(self.acct_line.forecast_period_ids)
        self.assertEqual(len(self.acct_line.forecast_period_ids), 7)

    @mute_logger("odoo.addons.queue_job.models.base")
    def test_forecast_period_on_contract_line_update_3(self):
        self.assertEqual(self.acct_line.price_subtotal, 50)
        self.acct_line.write({"price_unit": 50})
        self.assertEqual(self.acct_line.price_subtotal, 25)
        self.assertEqual(
            self.acct_line.forecast_period_ids[0].price_subtotal, 25
        )

    @mute_logger("odoo.addons.queue_job.models.base")
    def test_forecast_period_on_contract_line_update_4(self):
        self.assertEqual(self.acct_line.price_subtotal, 50)
        self.acct_line.write({"discount": 0})
        self.assertEqual(self.acct_line.price_subtotal, 100)
        self.assertEqual(
            self.acct_line.forecast_period_ids[0].price_subtotal, 100
        )

    @mute_logger("odoo.addons.queue_job.models.base")
    def test_forecast_period_on_contract_line_update_5(self):
        self.acct_line.cancel()
        self.assertFalse(self.acct_line.forecast_period_ids)
