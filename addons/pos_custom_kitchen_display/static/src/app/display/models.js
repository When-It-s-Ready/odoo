/** @odoo-module */

import { parseFloat as oParseFloat } from "@web/views/fields/parsers";
import {
    formatDate,
    formatDateTime,
    serializeDateTime,
    deserializeDate,
    deserializeDateTime,
} from "@web/core/l10n/dates";
import {
    formatFloat,
    roundDecimals as round_di,
    roundPrecision as round_pr,
    floatIsZero,
} from "@web/core/utils/numbers";

import { PosCollection } from "@point_of_sale/app/store/models";

const { DateTime } = luxon;

let nextId = 0;
class BaseKDModel {

    constructor() {
        this.setup(...arguments);
    }

    setup(defaultObj) {
        defaultObj = defaultObj || {};
        if(!defaultObj.cid) {
            defaultObj.cid = this._getCID(defaultObj);
        }
        Object.assign(this, defaultObj);
    }

    _getCID(obj) {
        if (obj.id) {
            if (typeof obj.id == "string") {
                return obj.id;
            } else if (typeof obj.id == "number") {
                return `c${obj.id}`;
            }
        }
        return `c${nextId++}`;
    }
}

class KDCollection extends PosCollection {

    fromList(list) {
        for (const entry of list) {
            this.add(entry);
        }
    }
}


export class Ticketline extends BaseKDModel {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.ticket_id = options.ticket_id;
        this.product_id = options.product_id;
        this.name = options.name;
        this.qty = options.qty;
        this.note = options.note;
        this.line_status = options.line_status;
    }

    moveStatus(){
        if (!this.line_status) {
            this.line_status = "pending";
        } else if (this.line_status == "pending"){
            this.line_status = "done";
        }
    }

    cancelStatus() {
        this.line_status =  "cancel";
    }
}

export class Ticket extends BaseKDModel {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.order = options.order;
        this.ticket_status = options.ticket_status;
        this.lines = new KDCollection().fromList(options.lines);
        this.table = options.order;
        this.create_time = options.create_time;
    }

    checkLines() {
        for (const line of this.lines){
            if( line.line_status == "pending" ){
                return false;
            }
        }
        return true;
    }

    moveStatus() {
        if(!this.ticket_status) {
            this.ticket_status = "pending";
        } else if (this.ticket_status == "pending") {
            this.ticket_status = "ack";
        } else if (this.ticket_status == "ack") {
            if (checkLines()){
                this.ticket_status == "done"
            }
        }
    }
}