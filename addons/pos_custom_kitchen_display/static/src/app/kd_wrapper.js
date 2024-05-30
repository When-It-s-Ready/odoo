/** @odoo-module */
// code from the playground tutorial

import { Component } from "@odoo/owl";
import { KitchenDisplayDashboard } from "./kitchen_display_dashboard/kitchen_display_dashboard"


export class KitchenDisplayWrapper extends Component {
    // references the template in ./kd_wrapper.xml
    static template = "pos_custom_kitchen_display.wrapper";
    static components = { KitchenDisplayDashboard };
    static props = {};

    setup() {
        // prevent backspace from performing a 'back' navigation
        document.addEventListener("keydown", (ev) => {
            if (ev.key === "Backspace" && !ev.target.matches("input, textarea")) {
                ev.preventDefault();
            }
        });
    }

}