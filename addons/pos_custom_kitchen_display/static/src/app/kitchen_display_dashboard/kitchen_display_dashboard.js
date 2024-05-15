/** @odoo-module **/

import { Component, useState } from  "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Notebook } from "@web/core/notebook/notebook";

export class KitchenDisplayDashboard extends Component {
    static template = "pos_custom_kitchen_display.KitchenDisplayDashboard";
    static components = { Notebook };
    
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            current_state : 'pending',
            tickets: []
        });
        var that = this;
        this.orm.call("kitchen.display", "get_tickets",[""]).then((result) => {
            that.state.tickets = result["tickets"];
            console.log(result['tickets']);
        });

    }


    set_state(stage) {
        this.state.current_state = stage;
    }
}