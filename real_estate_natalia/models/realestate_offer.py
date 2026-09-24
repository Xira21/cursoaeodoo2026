from odoo import models, fields

class RealEstateOffer(models.Model):
    _name = "realestate.offer"
    _description = "Offer"
    _rec_name = "property_id"

    property_id = fields.Many2one(
        comodel_name = "realestate.property",
        string="Property",
        required=True,
    )
    partner_id = fields.Many2one(
        comodel_name = "res.partner",
        string = "Buyer",        
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

    category_id = fields.Many2one(
        comodel_name = "realestate.category",
        string = "Category",
        related='property_id.category_id',
        readonly=True
    )

    notes = fields.Text(string = "Notes")
    color = fields.Integer(string="Color")
    # Tambien podria ser
    # notes = fields.Html(string = "Notes")

    def action_send(self):
        self.state = "sent"

    def action_accept(self):        
        self.state = "accepted"
        self.property_id.action_reserve()

    def action_reject(self):
        self.state = "rejected"

    def action_draft(self):
        self.state = "draft"

    def action_create_contract(self):
        for offer in self:
            self.env["realestate.contract"].create({
                'property_id': offer.property_id.id,
                'partner_id': offer.partner_id.id,
                'contract_type': "sale",
                'start_date': fields.Date.today(),
            })
                
            
                
            
            

 



  
