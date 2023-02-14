from odoo import models,fields,api

class HrEmployeeInherit(models.Model):

    _inherit = "hr.employee"
    
    military_certificate = fields.Binary()
    
    # @api.model
    # def create(self):
    #     pass