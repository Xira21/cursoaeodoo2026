from odoo import models, fields

class MusicSchoolLessonAttendance(models.Model):
    _name = "music.school.lesson.attendance"
    _description = "Attendance for Music School Lessons"
    _rec_name = "student_id"
    _order = "sequence, id"

    sequence = fields.Integer(string="Sequence", default=10)
    student_id = fields.Many2one(
        comodel_name="music.school.student",
        string="Student",
        required=True,
        help="Student attending the lesson"
    )

    attended = fields.Boolean(string="Attended", default=True)
    date = fields.Datetime(string="Date")

    lesson_id = fields.Many2one(
        comodel_name="music.school.lesson",
        string="Lesson",
        ondelete="cascade",
    )