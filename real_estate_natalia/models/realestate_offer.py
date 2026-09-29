from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

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
    amount = fields.Monetary(string = "Amount", currency_field='currency_id')

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related= 'property_id.currency_id'
    )
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
        store=True,
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
                'name': f"Contrato {offer.property_id.name}",
            })
            
    # Añadir una constrain en la oferta para que el importe no pueda ser negativo             
    @api.constrains('amount')
    def _check_amount(self):
        for offer in self:
            if offer.amount < 0:
                raise ValidationError(_("The offer amount cannot be negative"))
            
                
            
            

 



  
