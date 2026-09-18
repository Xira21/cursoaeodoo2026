from odoo import models, fields

class RealEstateContract(models.Model):
    _name = "realestate.contract"
    _description = "Contract"

    name = fields.Char(string = "Name", required=True)
    type = fields.Selection(
        selection = [
            ("rental", "Rental"),
            ("sale", "Sale"),
        ],
        string = "Type",
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

    def action_start(self):
        self.state = "in_progress"

    def action_done(self):
        self.state = "done"

    def action_cancel(self):
        self.state = "cancelled"

    def action_draft(self):
        self.state = "draft"

