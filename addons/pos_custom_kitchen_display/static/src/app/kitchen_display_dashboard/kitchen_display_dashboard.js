/** @odoo-module **/

import { Component, useState } from  "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Notebook } from "@web/core/notebook/notebook";


// The main component for the display screen
// requires the Notebook component for the different ticket statuses
// and the orm service to access the backend
export class KitchenDisplayDashboard extends Component {
    //references the template in ./kitchen_display_dashboard.xml
    static template = "pos_custom_kitchen_display.KitchenDisplayDashboard";
    static components = { Notebook };
    static serviceDependencies = [ "orm" ];
    
    setup() {

        this.disp = this.get_disp_info(); 
        this.orm = useService("orm");
        this.timeoffset = new Date().getTimezoneOffset();
        // tickets in the useState in order to refresh on any changes in the tickets
        this.state = useState({
            tickets: [],
            last_ticket: 0,
            failed_polls: 0
        });
        this.sound = new Audio('/pos_custom_kitchen_display/static/src/sound/notification.mp3');
        const poll = this.polling_tickets.bind(this);
        poll();
    }

    // on successful run, it will trigger itself after 5 seconds
    polling_tickets() {
        this.orm.call("kitchen.display", "ticket_polling",["",this.disp.id]).then(
            (result) => {
                this.state.tickets = result["tickets"];
                if(!!result["tickets"] && result["tickets"].length > 0){
                    if(result["tickets"][0]['id'] != this.state.last_ticket){
                        this.sound.play();
                        this.state.last_ticket = result["tickets"][0]['id'];
                    }
                }
                this.failed_polls = 0;
                setTimeout(this.polling_tickets.bind(this), 1000*this.disp.ps);
            },
            (reject)=> {
                this.failed_polls +=1;
                if (this.failed_polls >= this.disp.thr){
                    alert("Failed error request threshold, refresh page and check server status");
                }else {
                    setTimeout(this.polling_tickets.bind(this), 1000*this.disp.eps);
            }
        });
    }


    // get the display id from the url parameters
    get_disp_info(){
        let params = new URLSearchParams(window.location.search);
        return {
            'id': params.get('disp_id'),
            'ps': params.get('ps'),
            'eps': params.get('eps'),
            'thr': params.get('thr')
        };
    }

    // request ticket update from the backend for a specific ticket
    // used on pending tab to acknowledge the ticket
    // and on in-progress tab if all ticket lines are finished or canceled
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

    // used to check if updateTicketStatus() should be allowed in the in-progress tab
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

    // used in the in-progress tab to change the status of one line of a ticket
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

    // helper to get the proper classes that correspond to each line
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

    calc_time_offset(time){
        return new Date(Date.parse(time) - this.timeoffset * 60000).toLocaleTimeString("en-GB", {
            hour: '2-digit',
            minute:'2-digit'
          });
    }
}
