from odoo import models, fields

class MusicSchoolInstrument(models.Model):
    _name = "music.school.instrument"
    _description = "Instruments"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    inspection_date = fields.Date(string="Date Inspection")

    family_id = fields.Many2one(
        comodel_name="music.school.instrument.family",
        string="Family",
        help="Family of the instrument",
    )

    def add_inspection_date(self):
        for record in self:
            record.inspection_date=fields.Date.context_today(record)