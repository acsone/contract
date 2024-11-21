# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    qty_type = fields.Selection(
        selection=[
            ("fixed", "Fixed quantity"),
            ("variable", "Variable quantity"),
        ],
        required=False,
        default="fixed",
        string="Qty. type",
    )
    qty_formula_id = fields.Many2one(
        comodel_name="contract.line.qty.formula", string="Qty. formula"
    )
