from odoo import models, fields

class MusicSchoolLesson(models.Model):
    _name = "music.school.lesson"
    _description = "Lessons"
    _rec_name = "course_id"

    teacher_id = fields.Many2one(
        comodel_name="music.school.teacher",
        string="Teacher",
        help="Teacher responsible for the lesson"
    )

    course_id = fields.Many2one(
        comodel_name="music.school.course",
        string="Course",
        required=True,
        help="Course associated with the lesson"
    )

    room_id = fields.Many2one(
        comodel_name="music.school.room",
        string="Room",
        help="Room where the lesson takes place"
    )

    date = fields.Datetime(string="Date", help="Date and time when the lesson takes place")
    duration = fields.Float(string="Duration", help="Duration of the lesson in hours")
    notes = fields.Text(string="Notes", help="Additional notes about the lesson")

    state = fields.Selection(
        selection=[
            ('scheduled','Scheduled'),
            ('done','Done'),
            ('cancelled','Cancelled'),
        ],
        string="State",
        default="scheduled",
        group_expand=True,
    )

    color = fields.Integer(string="Color")