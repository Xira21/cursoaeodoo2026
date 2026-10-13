from odoo import models, fields

class MusicSchoolTeacher(models.Model):
    _name = "music.school.teacher"
    _description = "Teachers"

    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")

    level = fields.Selection(
        selection=[
            ('beginner','Beginner'),
            ('intermediate','Intermediate'),
            ('advanced','Advanced'),
        ],
        string="Level",
        default='beginner',
    )