from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class MusicSchoolStudent(models.Model):
    _name = "music.school.student"
    _description = "Students"
    _order = "sequence, name"

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    birthdate = fields.Date(string="Birthdate")
    age = fields.Integer(string="Age", compute="_compute_age")
    notes = fields.Html(string="Notes", help="Additional notes about the student.")
    sequence = fields.Integer(string="Sequence", default=10)
    registration_date = fields.Date(string="Registration Date", default=fields.Date.context_today)

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible",
        help="Responsible user for this student",
        default=lambda self: self.env.user.id        
    )

    reference = fields.Char(
        string="Reference", 
        copy=False, 
        readonly=True
    )

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Contact",
    )

    def generate_reference(self):
        for record in self:
            record.reference="MAT-" + str(record.id)

    @api.depends('birthdate')
    def _compute_age(self):
        for record in self:
            if record.birthdate:                
                record.age=relativedelta(fields.Date.today(),record.birthdate).years
            else:
                record.age=0

    # Si cambia el contacto, se trae el telefono y el email
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.phone = self.partner_id.phone
            self.email = self.partner_id.email
        else:
            self.phone = False
            self.email = False
            