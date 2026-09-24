from odoo import models, fields

class RealEstatePropertyIncident(models.Model):
    _name = "realestate.property.incident"
    _description = "Property Incident"

    sequence = fields.Integer(string="Sequence", default=10)
    name = fields.Char(string="Name")
    description = fields.Text(string="Description")

    property_id = fields.Many2one(
        comodel_name = "realestate.property",
        string = "Property",
        ondelete = "cascade"
    )

    priority = fields.Selection(
        selection = [
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Very High')
    ], string="Priority", default='0')

    state = fields.Selection(
        selection = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('cancelled', 'Cancelled')
    ], string="State", default = 'new')

    date = fields.Datetime(string="Date", default=fields.Datetime.now)

    user_id = fields.Many2one(
        comodel_name = "res.users",
        string = "User"
    )
   
