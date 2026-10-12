from odoo import models, fields

class MusicSchoolStudent(models.Model):
    _name = "music.school.student"
    _description = "Students"
    _order = "sequence, name"

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    birthdate = fields.Date(string="Birthdate")
    age = fields.Integer(string="Age")
    notes = fields.Html(string="Notes", help="Additional notes about the student.")
    sequence = fields.Integer(string="Sequence", default=10)
    registration_date = fields.Date(string="Registration Date", default=fields.Date.context_today)

    user_id = fields.Many2one(
        comodel_name="res.users",
        string ="Responsible",
        help="Responsible user for this student",
        default=lambda self:self.env.user.id        
    )


    
    
    # instrument_id = fields.Many2one(
    #     comodel_name="music.school.instrument",
    #     string="Instrument"
    # )