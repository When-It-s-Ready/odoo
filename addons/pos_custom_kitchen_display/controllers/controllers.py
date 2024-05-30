from odoo import http
from odoo.http import request, route

# Setup the controller route that the kitchen screen will be displayed
# pos_custom_kitchen_display.wrapper references the wrapper in static/src/app/kd_wrapper.xml
class KitchenDisplay(http.Controller):

    @http.route(['/kdisplay'], type="http", auth='user')
    def show_kitchen_display(self):
        
        return request.render('pos_custom_kitchen_display.wrapper')