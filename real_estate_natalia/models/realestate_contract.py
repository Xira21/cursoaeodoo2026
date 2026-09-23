from odoo import models, fields, api

class RealEstateContract(models.Model):
    _name = "realestate.contract"
    _description = "Contract"

    name = fields.Char(string = "Name", required=True)
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

    start_date = fields.Date(string ="Start Date")
    end_date = fields.Date(string ="End Date")

    rent = fields.Float(string="Rent")
    deposit = fields.Float(string="Deposit")

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

