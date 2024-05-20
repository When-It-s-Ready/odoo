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
        
        this.disp = this.get_displ_id(); 
        this.orm = useService("orm");
        this.state = useState({
            tickets: []
        });
        this.orm.call("kitchen.display", "start_ticket_polling",["",this.disp]).then((result) => {
            this.state.tickets = result["tickets"];
        });
        const poll = this.polling_tickets.bind(this);
        poll();
    }

    polling_tickets() {
        this.orm.call("kitchen.display", "get_next_tickets",["",this.disp]).then((result) => {
            this.state.tickets = result["tickets"].concat(this.state.tickets);
            setTimeout(this.polling_tickets.bind(this), 5000);
        });
    }


    get_displ_id(){
        let params = new URLSearchParams(window.location.search);
        return params.get('disp_id');
    }

    updateTicketStatus(id){
        console.log("update ticket with id", id);
        this.orm.call("kitchen.ticket", "update_status_ui", ["",id]).then((result) => { 
            if (result['status'] != 'error'){
                for (var ticket of this.state.tickets){
                    if (ticket.id == id){
                        ticket.ticket_status = result['status'];
                        break;
                    }
                }
            }
        });
    }
}