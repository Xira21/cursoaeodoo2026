from odoo import models, fields

class RealEstateVisit(models.Model):
    _name = "realestate.visit"
    _description = "Visit"
    _rec_name = "property_id"

    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
        required=True,
    )
    date = fields.Datetime(string="Visit Date")

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Visitor",
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("done", "Done"),
            ("cancelled", "Cancelled")
        ],
        string="State",
        default="draft",
    )