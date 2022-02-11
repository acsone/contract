# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    partner_delivery_zone_id = fields.Many2one(
        comodel_name="partner.delivery.zone",
        related="partner_id.delivery_zone_id",
        store=True,
        readonly=False,
        index=True,
        help="This is the partner delivery zone. If you modify this here, it"
        "will be modified on partner too.",
    )
