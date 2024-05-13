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

import { PosCollection as KDCollection } from "@point_of_sale/app/store/models";

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
            this.line_status = "";
        }
    }
}