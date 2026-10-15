from odoo import models, fields

class MusicSchoolRoom(models.Model):
    _name = "music.school.room"
    _description = "Rooms"

    name = fields.Char(string="Name", required=True)
    capacity = fields.Integer(
        string="Capacity",
        help="Maximum number of students that can fit in the room"
    )
    location = fields.Char(
        string="Location",
        help="Physical location of the room within the school"
    )

    # _sql_constrains nombre habitación que sea unico
    _name_unique = models.Constraint('unique(name)','The room name must be unique.')