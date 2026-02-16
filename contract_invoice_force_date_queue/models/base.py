# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _job_prepare_context_before_enqueue_keys(self):
        """
        Keys to keep in context of stored jobs
        """
        return (
            *super()._job_prepare_context_before_enqueue_keys(),
            "invoice_date_forced",
        )
