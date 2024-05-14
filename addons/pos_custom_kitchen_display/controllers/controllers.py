from odoo import http
from odoo.http import request, route

class KitchenDisplay(http.Controller):

    @http.route(['/kdisplay'], type="http", auth='public')
    def show_kitchen_display(self):
        
        return request.render('pos_custom_kitchen_display.wrapper')