from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class RealEstateContract(models.Model):
    _name = "realestate.contract"
    _description = "Contract"

    name = fields.Char(string = "Name", copy=False)
    contract_type = fields.Selection(
        selection = [
            ("rental", "Rental"),
            ("sale", "Sale"),
        ],
        string = "Contract Type",
        required = True,
    )

    property_id = fields.Many2one(
        comodel_name = "realestate.property",
        string = "Property",
        required=True,
    )

    partner_id = fields.Many2one(
        comodel_name = "res.partner",
        string = "Tenant",
        required=True,
    )

    # Restricción SQL en el nombre del contrato, que sea único.
    _name_unique = models.Constraint(
        'unique(name)',
        'The contract name must be unique.'
    )

    # Cuando se cree un contrato que se ponga la fecha de hoy como fecha de inicio.
    start_date = fields.Date(string ="Start Date", default= fields.Date.context_today)
    end_date = fields.Date(string ="End Date")

    rent = fields.Monetary(string="Rent", currency_field='currency_id')
    deposit = fields.Monetary(string="Deposit", currency_field='currency_id')

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related= 'property_id.currency_id'
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string = "State",
        default = "draft",
    )

    has_deposit = fields.Boolean(string="Has Deposit", compute="_compute_has_deposit", store=True)

    duration_days = fields.Integer(string="Duration (Days)",
        compute="_compute_duration_days",
        store=True)

    days_to_end = fields.Integer(string="Days to End",
        compute="_compute_days_to_end")

    days_in_progress = fields.Integer(
        string="Days in Progress",
        compute="_compute_days_in_progress"
    )    

    def _compute_days_in_progress(self):
        for record in self:
            if record.start_date and record.state == 'in_progress':
                record.days_in_progress = (fields.Date.today() - record.start_date).days
            else:
                record.days_in_progress = 0

    @api.depends('deposit')
    def _compute_has_deposit(self):
        for record in self:
            record.has_deposit = record.deposit > 0   
             

    @api.depends('start_date', 'end_date')
    def _compute_duration_days(self):
        for record in self:
            if record.start_date and record.end_date:
                record.duration_days = (record.end_date - record.start_date).days
            else:
                record.duration_days = 0

    def _compute_days_to_end(self):
        for record in self:
            # Punto de ruptura para ver cómo se para la vista porque está calculando ese campo
            # import pdb;pdb.set_trace()
            if record.end_date:
                record.days_to_end = (record.end_date - fields.Date.today()).days
            else:
                record.days_to_end = 0

    def action_start(self):
        self.state = "in_progress"

    def action_done(self):
        self.state = "done"

    def action_cancel(self):
        self.state = "cancelled"

    def action_draft(self):
        self.state = "draft"

    # para el cron
    @api.model
    def _cron_finish_contracts(self):
        contracts = self.env['realestate.contract'].search(
            [('end_date', '<', fields.Date.today()),
            ('state', '=', 'in_progress')])
        
        #contracts.write({'state': 'done'})
        contracts.action_done()

    # Añadir una constraint en el contrato que impida que la fecha de fin
    # sea anterior a la fecha de inicio

    @api.constrains('end_date', 'start_date')
    def _check_end_date(self):
        for record in self:
            if record.end_date and record.start_date and record.end_date < record.start_date:
                raise ValidationError(_("The end date cannot be earlier than the start date."))

    # Un onchange en el contrato, al elegir la propiedad, que el alquiler
    # se rellene con el precio de la propiedad.

    @api.onchange('property_id')
    def _onchange_property_id(self):
        if self.property_id:            
            self.rent = self.property_id.price
        else:
            self.rent = 0


