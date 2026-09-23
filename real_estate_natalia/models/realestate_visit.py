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
        group_expand="_group_expand_state"
    )

    color = fields.Integer(string="Color")

    phone = fields.Char(string="Phone", related='partner_id.phone', readonly=False, store=True)
    personal_email = fields.Char(string="Personal Email", related='partner_id.email', readonly=False, store=True)

    def _group_expand_state(self, states, domain):
        return ["draft", "confirmed", "done", "cancelled"]

    def action_confirm(self):
        #self.ensure_one()
        self.state = "confirmed"

    def action_done(self):
        #self.ensure_one()
        self.state = "done"

    def action_cancel(self):
        #self.ensure_one()
        self.state = "cancelled"

    def action_draft(self):
        #self.ensure_one()
        self.state = "draft"