/** @odoo-module */

import { useService } from "@web/core/utils/hooks";
import { Transition } from "@web/core/transition";
import { MainComponentsContainer } from "@web/core/main_components_container";
import { ErrorHandler } from "@web/core/utils/components";
import { reactive, Component, onMounted, onWillStart } from "@odoo/owl";


export class KitchenDisplayWrapper extends Component {
    static template = "kitchen_display.Wrapper";
    static components = { Transition, MainComponentsContainer, ErrorHandler };

    setup() {
        this.disp = useState(useService("kd_service"));
        const reactiveDisp = reactive(this.disp);
        window.dispmodel = reactiveDisp;

        // prevent backspace from performing a 'back' navigation
        document.addEventListener("keydown", (ev) => {
            if (ev.key === "Backspace" && !ev.target.matches("input, textarea")) {
                ev.preventDefault();
            }
        });
    }

}