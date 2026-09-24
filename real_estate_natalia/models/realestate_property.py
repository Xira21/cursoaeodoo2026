from odoo import models, fields, api

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

    image_ids = fields.One2many(
        comodel_name ="realestate.property.image",
        inverse_name ="property_id",
        string="Images"
    )

    visit_ids = fields.One2many(
        comodel_name="realestate.visit",
        inverse_name="property_id",
        string="Visits"
    )

    incident_ids = fields.One2many(
        comodel_name = "realestate.property.incident",
        inverse_name = "property_id",
        string = "Incidents"
    )

    offer_ids = fields.One2many(
        comodel_name = "realestate.offer",
        inverse_name = "property_id",
        string = "Offers"
    )

    next_visit_date = fields.Datetime(
        string ="Next Visit Date",
        compute="_compute_next_visit_date"
    )

    color = fields.Integer(string="Color")
    
    def action_reserve(self):
        self.availability = False
        
    def _read_group_stage_ids(self, stages, domain):
        return self.env['realestate.property.stage'].search([], order='sequence')
    
    # Botón para crear una visita (que luego hay que añadir el botón en la vista)
    def action_create_visit(self):
        vals = {
            'property_id': self.id,
            'date' : fields.Datetime.now(),
            'user_id' : self.user_id.id # hace referencia al user que tiene la propiedad
            # asi hace referencia al usuario que le está dando al botón:
            # 'user_id': self.env.user.id
        }
        self.env['realestate.visit'].create(vals)

    # Botón Nos busca la mejor oferta que en el estado ponga enviada
    def action_accept_best_offer(self):
        best_offer = self.env['realestate.offer'].search([('property_id', '=', self.id),('state','=','sent')], order='amount desc', limit=1)
        if best_offer:
            best_offer.action_accept()

    # Botón Nos elimina las ofertas que han sido rechazadas
    def action_delete_refused_offers(self):
        refused_offers = self.env['realestate.offer'].search([('property_id','=',self.id),('state','=','rejected')])
        refused_offers.unlink()

    # Botón que crea una oferta de una propiedad y la pone como enviada
    def action_create_offer(self):
        vals = {
            'property_id': self.id,
            'amount': self.price            
        }
        offer = self.env['realestate.offer'].create(vals)
        offer.action_send()
    
    @api.depends("visit_ids.date", "visit_ids.state")
    def _compute_next_visit_date(self):
        for property in self:
            visits = property.visit_ids.filtered(
                lambda visit: visit.state == 'confirmed'
                and visit.date > fields.Datetime.now()
            ).sorted(key=lambda v: v.date)
            property.next_visit_date = visits[0].date if visits else False

    # Botón que cancele todas las visitas en borrador o planificadas
    def action_cancel_visits(self):     
        visits = self.env["realestate.visit"].search([
            ("property_id", "in", self.ids),
            ("state", "in", ["draft", "confirmed"]),
        ])
        visits.write({"state": "cancelled"})

        #Otra forma de hacerlo:
        """for property in self:
            for visit in property.visit_ids:
                if visit.state in ("draft", "confirmed"):
                    visit.action_cancel()"""
        
    

          
