/** @odoo-module */

import { SplitBillScreen } from "@pos_restaurant/app/split_bill_screen/split_bill_screen";
import { patch } from "@web/core/utils/patch";

patch(SplitBillScreen.prototype, {

    proceed() {
        if (Object.keys(this.splitlines || {})?.length === 0) {
            // Splitlines is empty
            return;
        }

        this._isFinal = true;
        delete this.newOrder.temporary;
        console.log("from patch");

        if (!this._isFullPayOrder()) {
            this._setQuantityOnCurrentOrder();

            this.newOrder.set_screen_data({ name: "PaymentScreen" });

            // for the kitchen printer we assume that everything
            // has already been sent to the kitchen before splitting
            // the bill. So we save all changes both for the old
            // order and for the new one. This is not entirely correct
            // but avoids flooding the kitchen with unnecessary orders.
            // Not sure what to do in this case.
            if (this.pos.orderPreparationCategories.size) {
                this.currentOrder.updateLastOrderChange();
                this.newOrder.updateLastOrderChange();
            }

            this.newOrder.setCustomerCount(1);
            this.newOrder.originalSplittedOrder = this.currentOrder;

            // custom lines from pos_custom_kitchen_display
            this.newOrder.originalSplittedOrder.updateLastOrderChange();
            this.pos.orm.call(
                "pos.order",
                "update_split_order",
                [this.newOrder.originalSplittedOrder.export_as_JSON()]

            ).then((result) => {}, console.log)


            const newCustomerCount = this.currentOrder.getCustomerCount() - 1;
            this.currentOrder.setCustomerCount(newCustomerCount || 1);
            this.currentOrder.set_screen_data({ name: "ProductScreen" });

            const reactiveNewOrder = this.pos.makeOrderReactive(this.newOrder);
            this.pos.orders.add(reactiveNewOrder);
            this.pos.selectedOrder = reactiveNewOrder;
        }
        this.pos.showScreen("PaymentScreen");
    },
});