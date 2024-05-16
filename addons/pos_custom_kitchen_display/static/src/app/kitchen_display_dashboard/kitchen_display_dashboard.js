/** @odoo-module **/

import { Component, useState, EventBus } from  "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Notebook } from "@web/core/notebook/notebook";

export class KitchenDisplayDashboard extends Component {
    static template = "pos_custom_kitchen_display.KitchenDisplayDashboard";
    static components = { Notebook };
    static serviceDependencies = ["pos", "orm", "bus_service"];
    
    setup() {
        console.log(this.env.services);
        console.log(this.env.bus)
        this.orm = useService("orm");
        this.state = useState({
            current_state : 'pending',
            tickets: []
        });
        var that = this;
        this.orm.call("kitchen.display", "get_tickets",[""]).then((result) => {
            that.state.tickets = result["tickets"];
            // TODO: delete this
            console.log(result['tickets']);
        });
        this.bus = new EventBus();
        this.bus.addEventListener("new_ticket", (e) => this.new_ticket(e));

    }

    new_ticket(event){
        console.log(event);
    }


    set_state(stage) {
        this.state.current_state = stage;
    }
}