import { Mutex } from "@web/core/utils/concurrency";
import { markRaw, reactive } from "@odoo/owl";
import { roundPrecision as round_pr, floatIsZero } from "@web/core/utils/numbers";
import { registry } from "@web/core/registry";
import { Reactive } from "@web/core/utils/reactive";
import { memoize } from "@web/core/utils/functions";
import { ConnectionLostError } from "@web/core/network/rpc_service";
import { renderToString } from "@web/core/utils/render";
import { batched } from "@web/core/utils/timing";
import { EditListPopup } from "./select_lot_popup/select_lot_popup";


export class KitchenDisplay extends Reactive{
    mainScreen = { name: null, component: null};
    
    static serviceDependencies = [
        "orm",
        "ui"
    ];

    constructor() {
        super();
        this.ready = this.setup(...arguments).then(() => this);
    }

    async setup(env, { orm, ui }) {
        this.env = env;
        this.orm = orm;
        this.ui = ui;

        this.ready = new Promise((resolve) => {
            this.markReady = resolve;
        });
    }

    async load_server_tickets() {
        const loadedData = await this.orm.silent.call("kitchen.display", "get_tickets",[""]);
        await this._processData(loadedData);
    }    

    _load_tickets() {
        var jsons = this.db.get_tickets();
        var tickets = [];
        var not_loaded_count = 0;

        for (var i =0; i< jsons.length; i++) {
            var json = jsons[i];
            tickets.push(this.createReactiveTicket(json));
        }

        if(tickets.length) {
            this.tickets.add(tickets);
        }
    }

    async closeDisplay() {
        const syncSuccess = await this.push_updates_at_close();
        if (syncSuccess) {
            this.redirectToBackend();
        }
    }

    redirectToBackend() {
        window.location = "/web#action=pos_custom_kitchen_display.kitchen_display_action";
    }





}

export const kitchenDisplayService = {
    dependencies: KitchenDisplay.serviceDependencies,
    async start(env, deps) {
        return new KitchenDisplay(env, deps).ready;
    }
};

registry.category("services").add("kd_service", kitchenDisplayService);

