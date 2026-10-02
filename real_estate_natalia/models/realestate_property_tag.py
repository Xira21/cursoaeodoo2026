from odoo import models, fields

class RealEstatePropertyTag(models.Model):
    _name = "realestate.property.tag"
    _description = "Property Tag"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")

    property_ids = fields.Many2many(
        comodel_name = "realestate.property",
        relation = "realestate_property_realestate_property_tag_rel",
        column1 = "realestate_property_tag_id",
        column2 = "realestate_property_id",
        string = "Properties"
    )