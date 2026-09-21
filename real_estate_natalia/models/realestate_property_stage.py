from odoo import models, fields

class RealEstatePropertyStage(models.Model):
    _name = "realestate.property.stage"
    _description = "Real Estate Property Stage"

    name = fields.Char(string="Stage Name", required=True)
    sequence = fields.Integer(string = "Sequence", default=10)