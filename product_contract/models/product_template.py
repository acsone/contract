# Copyright 2017 LasLabs Inc.
# Copyright 2018 ACSONE SA/NV.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_contract = fields.Boolean('Is a contract')
    contract_template_id = fields.Many2one(
        comodel_name='account.analytic.contract', string='Contract Template'
    )

    recurring_rule_type = fields.Selection(
        [
            ('daily', 'Day(s)'),
            ('weekly', 'Week(s)'),
            ('monthly', 'Month(s)'),
            ('monthlylastday', 'Month(s) last day'),
            ('yearly', 'Year(s)'),
        ],
        default='monthly',
        string='Recurrence',
        help="Specify Interval for automatic invoice generation.",
    )
    recurring_invoicing_type = fields.Selection(
        [('pre-paid', 'Pre-paid'), ('post-paid', 'Post-paid')],
        default='pre-paid',
        string='Invoicing type',
        help="Specify if process date is 'from' or 'to' invoicing date",
    )
    recurring_interval = fields.Integer(
        default=1,
        string='Repeat Every',
        help="Repeat every (Days/Week/Month/Year)",
    )
    is_auto_renew = fields.Boolean(string="Auto Renew", default=False)
    auto_renew_interval = fields.Integer(
        default=1,
        string='Renew Every',
        help="Renew every (Days/Week/Month/Year)",
    )
    auto_renew_rule_type = fields.Selection(
        [('monthly', 'Month(s)'), ('yearly', 'Year(s)')],
        default='yearly',
        string='Renewal type',
        help="Specify Interval for automatic renewal.",
    )
    termination_notice_interval = fields.Integer(
        default=1, string='Termination Notice Before'
    )
    termination_notice_rule_type = fields.Selection(
        [('daily', 'Day(s)'), ('weekly', 'Week(s)'), ('monthly', 'Month(s)')],
        default='monthly',
        string='Termination Notice type',
    )

    @api.onchange('is_contract')
    def _change_is_contract(self):
        """ Clear the relation to contract_template_id when downgrading
        product from contract
        """
        if not self.is_contract:
            self.contract_template_id = False

    @api.constrains('is_contract', 'type')
    def _check_contract_product_type(self):
        """
        Contract product should be service type
        """
        if self.is_contract and self.type != 'service':
            raise ValidationError(_("Contract product should be service type"))
