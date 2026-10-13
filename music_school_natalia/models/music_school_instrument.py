from odoo import models, fields, api

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

    is_repaired = fields.Boolean(string="Is Repaired", compute="_compute_is_repaired")

    def add_inspection_date(self):
        for record in self:
            record.inspection_date=fields.Date.context_today(record)

    @api.depends('inspection_date')
    def _compute_is_repaired(self):
        for record in self:
            record.is_repaired = bool(record.inspection_date)
            # if record.inspection_date:
            #     record.is_repaired=True
            # else:
            #     record.is_repaired=False