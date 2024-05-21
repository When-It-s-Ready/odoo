/** @odoo-module **/

import { Component, useState, EventBus } from  "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Notebook } from "@web/core/notebook/notebook";

export class KitchenDisplayDashboard extends Component {
    static template = "pos_custom_kitchen_display.KitchenDisplayDashboard";
    static components = { Notebook };
    static serviceDependencies = ["pos", "orm", "bus_service"];
    
    setup() {

        this.disp = this.get_displ_id(); 
        this.orm = useService("orm");
        this.state = useState({
            tickets: []
        });
        const poll = this.polling_tickets.bind(this);
        poll();
    }

    polling_tickets() {
        this.orm.call("kitchen.display", "ticket_polling",["",this.disp]).then((result) => {
            this.state.tickets = result["tickets"];
            setTimeout(this.polling_tickets.bind(this), 5000);
        });
    }


    get_displ_id(){
        let params = new URLSearchParams(window.location.search);
        return params.get('disp_id');
    }

    updateTicketStatus(id){
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

    checkLinesStatus(id){
        for(var ticket of this.state.tickets){
            if(ticket.id == id){
                for(var line of ticket.lines){
                    if(line.line_status == 'pending' || line.line_status =='attention'){
                        return false;
                    }
                }
                return true;
            }
        }
    }

    updateLineStatus(id, line_id){
        this.orm.call("kitchen.ticket.line", "update_line_status_ui", ["",line_id]).then((result) => { 
            if (result['status'] != 'error'){
                for (var ticket of this.state.tickets){
                    if(ticket.id == id){
                        for(var line of ticket.lines){
                            if(line.id == line_id){
                                line.line_status = result['status'];
                                break;
                            }
                        }
                    }
                }
            }
        });
    }

    get_line_status_class(status){
        if (status == 'done'){
            return ' list-group-item-success';
        }
        if (status == 'cancel'){
            return ' list-group-item-danger';
        }
        if (status == 'attention'){
            return ' list-group-item-warning';
        }
        if (status == 'att_done'){
            return ' list-group-item-info';
        }
        return ''
    }
}