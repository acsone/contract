# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from psycopg2.extensions import AsIs

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    first_contract_line_start_date = fields.Date(
        string="First Contract Date",
        compute="_compute_contract_anniversary_date",
    )
    contract_anniversary_date = fields.Date(
        compute="_compute_contract_anniversary_date",
        search="_search_contract_anniversary_date",
    )

    def _compute_contract_anniversary_date(self):
        self.update(
            {
                "first_contract_line_start_date": False,
                "contract_anniversary_date": False,
            }
        )
        if self.ids:
            self.env.cr.execute(
                """
                SELECT
                    partner.id,
                    Min(contract_line.date_start),
                    Concat(
                        Date_part('year', current_date),
                        '-', Date_part('month', Min(contract_line.date_start)),
                        '-' ,
                        CASE WHEN
                            Date_part('day', Min(contract_line.date_start)) = 29
                            AND Date_part('month', Min(contract_line.date_start)) = 2
                        THEN
                            28
                        ELSE  Date_part('day', Min(contract_line.date_start))
                        END) :: date AS contract_anniversary_date
                FROM       contract_line AS contract_line
                INNER JOIN contract_contract      AS contract
                ON         contract.id=contract_line.contract_id
                INNER JOIN res_partner AS partner
                ON         contract.partner_id=partner.id
                AND        partner.id IN %s
                WHERE contract_line.is_canceled != True
                GROUP BY   partner.id
                """,
                (tuple(self.ids),),
            )
            rows = self.env.cr.fetchall()
            for row in rows:
                self.browse(row[0]).update(
                    {
                        "first_contract_line_start_date": row[1],
                        "contract_anniversary_date": row[2],
                    }
                )

    def _search_contract_anniversary_date(self, operator, value):
        if not value:
            value = None
            if operator == "=":
                operator = "is"
            elif operator == "!=":
                operator = "is not"

        self.env.cr.execute(
            """
            SELECT query.partner_id
                FROM   (SELECT partner.id   AS partner_id,
                       Min(contract_line.date_start),
                       CASE WHEN Min(contract_line.date_start) IS NOT NULL THEN
                       Concat(Date_part('year', current_date), '-',
                       Date_part('month', Min(contract_line.date_start)),
                       '-', CASE  WHEN
                       Date_part('day', Min(contract_line.date_start)) = 29
                       AND
                       Date_part('month', Min(contract_line.date_start)) = 2
                       THEN 28
                       ELSE Date_part('day', Min(contract_line.date_start))
                       END) :: DATE ELSE NULL END AS contract_anniversary_date
                    FROM   contract_line AS contract_line
                           inner join contract_contract AS contract
                                   ON contract.id = contract_line.contract_id
                           full join res_partner AS partner
                                   ON contract.partner_id = partner.id
                    WHERE contract_line.is_canceled != True
                    GROUP  BY partner.id) AS query
            WHERE  query.contract_anniversary_date %s %s""",
            (AsIs(operator), value),
        )
        rows = self.env.cr.fetchall()
        return [("id", "in", [row[0] for row in rows])]
