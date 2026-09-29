from odoo import models, fields, api

class RealEstateVisit(models.Model):
    _name = "realestate.visit"
    _description = "Visit"
    _rec_name = "property_id"

    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
        required=True,
    )
    # Cuando se cree una visita, que la fecha por defecto sea la de ahora  
    date = fields.Datetime(string="Visit Date", default=fields.Datetime.now)

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

    phone = fields.Char(string="Phone")
    personal_email = fields.Char(string="Personal Email")

    # En la visita, cambiar el teléfono y el email: quitar el related 
    # y añadir un onchange para que cuando se cambie el contacto se traigan el teléfono y el email.

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.phone = self.partner_id.phone
            self.personal_email = self.partner_id.email
        else:
            self.phone = False
            self.personal_email = False


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
    
    # para el cron
    @api.model
    def _cron_done_visits(self):
        visits = self.env['realestate.visit'].search(
            [('date', '<', fields.Datetime.now()),
            ('state', '=', 'confirmed')])
        
        visits.action_done()
