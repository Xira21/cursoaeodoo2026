from odoo import models, fields

class RealEstateProperty(models.Model):
    _name = "realestate.property"
    _description = "Property"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
