/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
    //@override
    async transferTable(table) {
        await super.transferTable(...arguments);
        await this.orm.call(
            "pos.order",
            "update_transfer_table",
            [this.selectedOrder.name, table.id]
        );
    }
});