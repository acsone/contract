/** @odoo-module **/

import {registry} from "@web/core/registry";
import {redirect} from "@web/core/utils/urls";

registry.category("web_tour.tours").add("contract_portal_tour", {
    test: true,
    url: "/my",
    steps: () => [
        {
            content: "Go /my/contracts url",
            trigger: 'a[href*="/my/contracts"]',
            run: function () {
                redirect("/my/contracts");
            },
        },
        {
            content: "Go to Contract item",
            trigger: "a.tr_contract_link:eq(0)",
            run: "click",
        },
    ],
});
