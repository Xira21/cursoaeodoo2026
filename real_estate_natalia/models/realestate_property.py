from odoo import models, fields

class RealEstateProperty(models.Model):
    _name = "realestate.property"
    _description = "Property"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    price = fields.Float(string="Price")
    reference = fields.Char(string="Reference")
    availability = fields.Boolean(string="Availability", default=True)
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
    )
    category_id = fields.Many2one(
        comodel_name="realestate.category",
        string="Category",
    )

    stage_id = fields.Many2one(
        comodel_name ="realestate.property.stage",
        string="Stage",
        group_expand="_read_group_stage_ids"
    )

    color = fields.Integer(string="Color")
    
    def action_reserve(self):
        self.availability = False
        
    def _read_group_stage_ids(self, stages, domain):
        return self.env['realestate.property.stage'].search([], order='sequence')
