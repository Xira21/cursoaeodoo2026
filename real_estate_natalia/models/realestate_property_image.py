from odoo import models, fields

class RealEstatePropertyImage(models.Model):
    _name = "realestate.property.image"
    _description = "Property Image"

    name = fields.Char(string = "Name")
    sequence = fields.Integer(string="Sequence", default=10)
    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
        ondelete="cascade",
    )
    image = fields.Binary(string="Image")