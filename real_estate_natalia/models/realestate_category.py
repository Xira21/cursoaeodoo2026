from odoo import models, fields

class RealEstateCategory(models.Model):
    _name = "realestate.category"
    _description = "Category"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    
   