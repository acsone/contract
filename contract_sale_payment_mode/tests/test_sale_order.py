# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestContractPaymentMode(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Ensure that the 'manual' payment method does not already exist
        cls.payment_method = cls.env["account.payment.method"].search(
            [("code", "=", "manual"), ("payment_type", "=", "inbound")], limit=1
        )

        # If the payment method doesn't exist, create it
        if not cls.payment_method:
            cls.payment_method = cls.env["account.payment.method"].create(
                {
                    "name": "Manual",
                    "code": "manual",
                    "payment_type": "inbound",
                }
            )

        # Create customer payment mode
        cls.customer_payment_mode = cls.env["account.payment.mode"].create(
            {
                "name": "Customer Mode",
                "payment_method_id": cls.payment_method.id,
                "show_bank_account": "full",
                "company_id": cls.env.company.id,
                "bank_account_link": False,
            }
        )

        # Create contract payment mode
        cls.contract_payment_mode = cls.env["account.payment.mode"].create(
            {
                "name": "Contract Mode",
                "payment_method_id": cls.payment_method.id,
                "show_bank_account": "full",
                "company_id": cls.env.company.id,
                "bank_account_link": False,
            }
        )

        # Create customer and assign the customer payment mode
        cls.customer = cls.env["res.partner"].create(
            {
                "name": "Test Customer",
                "payment_mode_id": cls.customer_payment_mode.id,
            }
        )

        # Create contract and assign the contract payment mode
        cls.contract = cls.env["contract.contract"].create(
            {
                "name": "Test Contract",
                "partner_id": cls.customer.id,
                "payment_mode_id": cls.contract_payment_mode.id,
            }
        )

    def test_action_confirm_with_customer_payment_mode(self):
        """Test confirming sale order with customer's payment mode"""
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.customer.id,
                "contract_id": False,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": "Service",
                            "product_id": self.env.ref("product.product_product_1").id,
                            "product_uom_qty": 1,
                            "price_unit": 100.0,
                            "product_uom": self.env.ref("uom.product_uom_unit").id,
                        },
                    )
                ],
            }
        )

        sale_order.action_confirm()
        _logger.info("Payment Mode: %s", sale_order.payment_mode_id.name)
        self.assertEqual(
            sale_order.payment_mode_id,
            self.customer_payment_mode,
            "Should use customer's payment mode",
        )

    def test_action_confirm_with_contract_payment_mode(self):
        """Test confirming sale order with contract's payment mode"""
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.customer.id,
                "contract_id": self.contract.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": "Service",
                            "product_id": self.env.ref("product.product_product_1").id,
                            "product_uom_qty": 1,
                            "price_unit": 100.0,
                            "product_uom": self.env.ref("uom.product_uom_unit").id,
                        },
                    )
                ],
            }
        )

        sale_order.action_confirm()
        _logger.info("Payment Mode: %s", sale_order.payment_mode_id.name)
        self.assertEqual(
            sale_order.payment_mode_id,
            self.contract_payment_mode,
            "Should use contract's payment mode",
        )
