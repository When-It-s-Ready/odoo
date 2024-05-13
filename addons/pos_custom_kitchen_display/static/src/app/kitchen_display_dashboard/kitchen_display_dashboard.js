/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from  "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class KitchenDisplayDashboard extends Component {
    
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            current_state : 'draft',
            tickets: []
        });
        var that = this;
        var test = this.orm.call("kitchen.display", "get_tickets",[""]);
        console.log(test);
        test.then((result) => {
            that.state.tickets = result["tickets"];
        });
    }


    set_state(e, stage) {
        this.current_state = state;
    }


}
KitchenDisplayDashboard.template = "kitchenDisplayDashboard";

// remember the tag name we put in the first step
registry.category("actions").add("kitchen_display_dashboard", KitchenDisplayDashboard);