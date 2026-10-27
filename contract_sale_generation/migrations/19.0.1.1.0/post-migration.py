# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    cr.execute(
        """
        UPDATE sale_order sale
           SET contract_id = contract_line.contract_id
          FROM sale_order_line sale_line
          JOIN contract_line ON contract_line.id = sale_line.contract_line_id
         WHERE sale_line.order_id = sale.id
        """
    )
