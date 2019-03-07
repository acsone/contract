# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.addons import decimal_precision as dp


class ContractLineForecastPeriod(models.Model):

    _name = "contract.line.forecast.period"
    _description = "Contract Line Forecast Period"
    _order = "date_invoice, sequence"

    name = fields.Char(string="Name", required=True, readonly=True)
    sequence = fields.Integer(
        string="Sequence", related="contract_line_id.sequence", store=True
    )
    contract_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Contract",
        required=True,
        readonly=True,
        ondelete="cascade",
        related="contract_line_id.contract_id",
        store=True,
        index=True,
    )
    contract_line_id = fields.Many2one(
        comodel_name="account.analytic.invoice.line",
        string="Contract Line",
        required=True,
        readonly=True,
        ondelete="cascade",
        index=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True,
        readonly=True,
        related="contract_line_id.product_id",
        store=True,
        index=True,
    )
    date_start = fields.Date(string="Date Start", required=True, readonly=True)
    date_end = fields.Date(string="Date End", required=True, readonly=True)
    date_invoice = fields.Date(
        string="Invoice Date", required=True, readonly=True
    )
    price_subtotal = fields.Float(
        digits=dp.get_precision("Account"),
        string="Amount Untaxed",
        related="contract_line_id.price_subtotal",
        store=True,
    )
    active = fields.Boolean(
        string="Active",
        related="contract_line_id.active",
        store=True,
        readonly=True,
        default=True,
    )
