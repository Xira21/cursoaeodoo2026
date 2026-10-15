from datetime import timedelta

from odoo import models, fields, _
from odoo.exceptions import UserError


class MusicSchoolLessonBatch(models.TransientModel):
    _name = "music.school.lesson.batch"
    _description = "Wizard to create a batch of lessons"

    course_id = fields.Many2one(
        comodel_name="music.school.course",
        string="Course",
        required=True,
    )
    start_date = fields.Datetime(
        string="Start Date",
        required=True,
        help="Date and time of the first possible lesson",
    )
    end_date = fields.Datetime(
        string="End Date",
        required=True,
        help="No lessons will be created after this date",
    )
    weekday = fields.Selection(
        selection=[
            ('0', 'Monday'),
            ('1', 'Tuesday'),
            ('2', 'Wednesday'),
            ('3', 'Thursday'),
            ('4', 'Friday'),
            ('5', 'Saturday'),
            ('6', 'Sunday'),
        ],
        string="Weekday",
        required=True,
    )
    duration = fields.Float(string="Duration", default=1.0)
    room_id = fields.Many2one(
        comodel_name="music.school.room",
        string="Room",
    )

    # Crear una lección cada semana, el día elegido, entre las dos fechas
    def action_create_lessons(self):
        self.ensure_one()
        if self.end_date < self.start_date:
            raise UserError(_("The end date cannot be before the start date."))

        vals_list = []
        current_date = self.start_date
        while current_date <= self.end_date:
            if current_date.weekday() == int(self.weekday):
                vals_list.append({
                    'course_id': self.course_id.id,
                    'teacher_id': self.course_id.teacher_id.id,
                    'room_id': self.room_id.id,
                    'date': current_date,
                    'duration': self.duration,
                })
            current_date += timedelta(days=1)

        if not vals_list:
            raise UserError(_("No lessons to create: the selected weekday is not in the date range."))

        lessons = self.env['music.school.lesson'].create(vals_list)

        # Abrir la lista con las lecciones creadas
        return {
            'type': 'ir.actions.act_window',
            'name': _('Lessons'),
            'res_model': 'music.school.lesson',
            'view_mode': 'list,form',
            'domain': [('id', 'in', lessons.ids)],
            'target': 'current',
        }
