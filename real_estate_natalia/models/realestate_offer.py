from odoo import models, fields

class RealEstateOffer(models.Model):
    _name = "realestate.offer"
    _description = "Offer"

    property_id = fields.Many2one(
        comodel_name = "realestate.property",
        string="Property",
        required=True,
    )
    partner_id = fields.Many2one(
        comodel_name = "res.partner",
        string = "Buyer",
        required=True,
    )
    amount = fields.Float(string = "Amount")
    date = fields.Datetime(string = "Date")
    state = fields.Selection(
        selection=[
            ("draft","Draft"),
            ("sent", "Sent"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected")
        ],
        string = "State",
        default = "draft",
    )
    notes = fields.Text(string = "Notes")

    def action_send(self):
        self.state = "sent"

    def action_accept(self):        
        self.state = "accepted"
        self.property_id.action_reserve()

    def action_reject(self):
        self.state = "rejected"

    def action_draft(self):
        self.state = "draft"

  
