/** @odoo-module */

import { templates } from "@web/core/assets";
import { App, whenReady } from "@odoo/owl";
import { makeEnv, startServices } from "@web/env";
import { session } from "@web/session";
import { KitchenDisplayWrapper } from "@pos_custom_kitchen_display/app/kd_app";

(async function startKitchenDisplay() {
    odoo.info = {
        db: session.db,
    };

    const env = makeEnv();
    await startServices(env);

    await whenReady();
    const app = new App(KitchenDisplayWrapper, {
        name: "Kitchen Display",
        env,
        templates,
    });

    const root = await app.mount(document.body);
    const classList = document.body.classList;
    if (env.services.user.userId === 1) {
        classList.add("o_is_superuser");
    }
    if (env.debug) {
        classList.add("o_debug");
    }

})();