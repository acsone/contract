# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests import new_test_user

from .test_contract import TestContractBase


class TestContractSecurity(TestContractBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.other_company = cls.env["res.company"].create({"name": "Other company"})
        cls.env.user.company_ids |= cls.other_company
        cls.portal_user = new_test_user(
            cls.env,
            login="portal_contract_follower",
            groups="base.group_portal",
        )
        cls.invoice_user = new_test_user(
            cls.env,
            login="contract_invoice_user",
            groups="account.group_account_invoice",
        )
        cls.manager_user = new_test_user(
            cls.env,
            login="contract_manager_user",
            groups="account.group_account_manager",
        )
        cls.followed_contract = cls._create_contract("Followed contract")
        cls.followed_contract.message_subscribe(
            partner_ids=cls.portal_user.partner_id.ids
        )
        cls.unfollowed_contract = cls._create_contract("Unfollowed contract")
        cls.other_company_contract = cls._create_contract(
            "Other company contract", company=cls.other_company
        )

    @classmethod
    def _create_contract(cls, name, company=None, user=None):
        contract = cls.env["contract.contract"].with_context(
            skip_modification_mail=True
        )
        if company:
            contract = contract.with_company(company)
        if user:
            contract = contract.with_user(user)
        return contract.create(
            {
                "name": name,
                "partner_id": cls.partner.id,
                "pricelist_id": cls.partner.property_product_pricelist.id,
                "line_recurrence": True,
                "company_id": (company or cls.env.company).id,
                "contract_line_ids": [
                    Command.create(
                        {
                            "product_id": cls.product_1.id,
                            "name": f"Line of {name}",
                            "quantity": 1,
                            "uom_id": cls.product_1.uom_id.id,
                            "price_unit": 100,
                            "recurring_rule_type": "monthly",
                            "recurring_interval": 1,
                            "date_start": "2018-02-15",
                            "recurring_next_date": "2018-02-22",
                        },
                    )
                ],
                "modification_ids": [
                    Command.create(
                        {"date": "2018-03-01", "description": f"Mod of {name}"}
                    )
                ],
            }
        )

    def test_portal_rules_limited_to_followed_contract(self):
        self.assertTrue(self.unfollowed_contract.contract_line_ids)
        self.assertTrue(self.unfollowed_contract.modification_ids)
        lines = self.env["contract.line"].with_user(self.portal_user).search([])
        modifications = (
            self.env["contract.modification"].with_user(self.portal_user).search([])
        )
        self.assertEqual(
            set(lines.ids), set(self.followed_contract.contract_line_ids.ids)
        )
        self.assertEqual(
            set(modifications.ids), set(self.followed_contract.modification_ids.ids)
        )

    def test_manager_contract_creation_cascades_to_modifications(self):
        contract = self._create_contract("Manager contract", user=self.manager_user)
        self.assertTrue(contract.modification_ids)
        self.assertTrue(all(contract.modification_ids.mapped("sent")))

    def test_modification_rule_limited_to_allowed_companies(self):
        other_modifications = self.other_company_contract.modification_ids
        self.assertTrue(other_modifications)
        visible = (
            self.env["contract.modification"].with_user(self.invoice_user).search([])
        )
        self.assertFalse(set(other_modifications.ids) & set(visible.ids))
