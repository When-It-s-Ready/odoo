/** @odoo-module */

import { Component } from "@odoo/owl";


export class KitchenDisplayWrapper extends Component {
    static template = "pos_custom_kitchen_display.wrapper";
    // static components = { KitchenDisplayDashboard, Navbar };

    setup() {
    //     // prevent backspace from performing a 'back' navigation
    //     document.addEventListener("keydown", (ev) => {
    //         if (ev.key === "Backspace" && !ev.target.matches("input, textarea")) {
    //             ev.preventDefault();
    //         }
    //     });
    }

}