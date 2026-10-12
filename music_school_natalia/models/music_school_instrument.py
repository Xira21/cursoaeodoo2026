from odoo import models, fields

class MusicSchoolInstrument(models.Model):
    _name = "music.school.instrument"
    _description = "Instruments"

    name = fields.Char(string="Name", required=True)
    family = fields.Selection(
        selection=[
            ('string', 'String'),
            ('wind', 'Wind'),
            ('percussion', 'Percussion'),
            ('keyboard', 'Keyboard'),
            ('electronic', 'Electronic'),
        ],
        string="Family",
        required=True
    )

    description = fields.Text(string="Description")
    inspection_date = fields.Date(string="Date Inspection")

    def add_inspection_date(self):
        for record in self:
            record.inspection_date=fields.Date.context_today(record)