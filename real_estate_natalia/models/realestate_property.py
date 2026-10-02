from odoo import models, fields, api

class RealEstateProperty(models.Model):
    _name = "realestate.property"
    _description = "Property"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")

    price = fields.Monetary(string="Price", currency_field='currency_id')
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        default = lambda self: self.env.company.currency_id.id
    )

    reference = fields.Char(string="Reference", copy=False)
    availability = fields.Boolean(string="Availability", default=True)
    active = fields.Boolean(string="Active", default=True)    

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        # La propiedad cuando se cree que tenga un usuario asignado
        default= lambda self: self.env.user.id
    )
    category_id = fields.Many2one(
        comodel_name="realestate.category",
        string="Category",
    )
    
    tag_ids= fields.Many2many(
        comodel_name="realestate.property.tag",
        string="Tags",
        relation="realestate_property_realestate_property_tag_rel",
        column1="realestate_property_id",
        column2="realestate_property_tag_id"    
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
    
    contract_ids = fields.One2many(
        comodel_name = "realestate.contract", 
        inverse_name = "property_id", 
        string = "Contracts"
    )

    next_visit_date = fields.Datetime(
        string ="Next Visit Date",
        compute="_compute_next_visit_date",
        inverse = "_inverse_next_visit_date",
        store = True
    )

    color = fields.Integer(string="Color")

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default= lambda self: self.env.company.id
    )

    internal_note = fields.Text(string="Internal Note", company_dependent=True)
    
    # Añade restricción SQL en la que la referencia de la propiedad sea única.
    _reference_unique = models.Constraint(
        'unique(reference)',
        'The property reference must be unique.'
    )

    # Hacer un smartbutton para que abra los contratos de esa propiedad
    contract_count = fields.Integer(string = "Contract Count", compute="_compute_contract_count")

    # Hacer un smartbutton para que en la propiedad aparezcan las visitas asociadas a esa propiedad.
    visit_count = fields.Integer(string ="Visit Count", compute="_compute_visit_count")

    # Hacer un smartbutton para que en la propiedad aparezcan las incidencias asociadas.
    incident_count = fields.Integer(string="Incident Count", compute="_compute_incident_count")

    @api.depends('visit_ids') 
    def _compute_visit_count(self):
        for record in  self:
            record.visit_count = len(record.visit_ids)

    @api.depends('contract_ids')
    def _compute_contract_count(self):
        for record in self:
            record.contract_count = len(record.contract_ids)
    
    def action_view_visits(self):
        self.ensure_one()
        return{
            'type': 'ir.actions.act_window',
            'name': 'Visits',
            'res_model': 'realestate.visit',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id}
        }

    def action_view_contracts(self):
        self.ensure_one()
        return{
            'type': 'ir.actions.act_window',
            'name': 'Contracts',
            'res_model': 'realestate.contract',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id}
        }

    @api.depends('incident_ids')
    def _compute_incident_count(self):
        for record in self:
            record.incident_count = len(record.incident_ids)
    
    def action_view_incidents(self):
        self.ensure_one()
        return{
            'type': 'ir.actions.act_window',
            'name': 'Incidents',
            'res_model': 'realestate.property.incident',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id}
        }
      

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
        for record in self:
            visits = record.visit_ids.filtered(
                lambda visit: visit.state == 'confirmed'
                and visit.date
                and visit.date > fields.Datetime.now()
            )
            visit_dates = visits.mapped('date')
            record.next_visit_date = min(visit_dates) if visit_dates else False
    
    def _inverse_next_visit_date(self):
        for record in self:
            if record.next_visit_date:
                confirmed_visits = record.visit_ids.filtered(
                    lambda v: v.state == 'confirmed')
                if confirmed_visits:
                    confirmed_visits[0].date=record.next_visit_date

    # Botón que cancele todas las visitas en borrador o planificadas
    def action_cancel_visits(self):     
        visits = self.env["realestate.visit"].search([
            ("property_id", "in", self.ids),
            ("state", "in", ["draft", "confirmed"]),
        ])
        visits.write({"state": "cancelled"})

        #Otra forma de hacerlo:
        """for record in self:
            for visit in record.visit_ids:
                if visit.state in ("draft", "confirmed"):
                    visit.action_cancel()"""
        
    # Para poner un botón de imprimir
    # def action_print_property(self):
    #     return self.env.ref('real_estate_natalia.action_report_realestate_property').report_action(self.ids)

          
