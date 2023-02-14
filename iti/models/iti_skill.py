from odoo import fields,models


class ItiSkill(models.Model):
    _name = "iti.skill"
    
    name = fields.Char()