from odoo import models, fields, api
from odoo import Command

class MusicSchoolCourse(models.Model):
    _name = "music.school.course"
    _description = "Courses"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    state = fields.Selection(
        selection=[
            ('draft','Draft'),
            ('progress','In Progress'),
            ('finished','Finished'),
        ],
        string="State",
        default='draft',
        group_expand=True,
    )

    teacher_id = fields.Many2one(
        comodel_name="music.school.teacher",
        string="Teacher",
        help="Teacher responsible for the course"
    )

    instrument_id = fields.Many2one(
        comodel_name="music.school.instrument",
        string="Instrument",
        help="Instrument associated with the course"
    )

    level = fields.Selection(
        selection=[
            ('beginner','Beginner'),
            ('intermediate','Intermediate'),
            ('advanced','Advanced'),
        ],
        string="Level",
        default='beginner',
    )

    start_date = fields.Date(string="Start Date", help="Date when the course starts")
    end_date = fields.Date(string="End Date", help="Date when the course ends")

    capacity = fields.Integer(string="Capacity", help="Maximum number of students allowed in the course")

    color = fields.Integer(string="Color", help="Color of the course card in kanban view")

    duration_days = fields.Integer(string="Duration Days", compute="_compute_duration_days", store=True)

    student_ids = fields.Many2many(
        comodel_name="music.school.student",
        string="Students",
        relation="music_school_course_music_school_student",
        column1="music_school_course_id",
        column2="music_school_student_id"
    )

    # Asignar alumnos al curso
    def assign_students(self):
        for record in self:
            students = self.env['music.school.student'].search([], limit=record.capacity)
            record.student_ids = [Command.link(a.id) for a in students]

    # Crear lección
    def create_lesson(self):
        for record in self:
            self.env['music.school.lesson'].create(
                {
                    'course_id': record.id,
                    'teacher_id': record.teacher_id.id,
                }
            )

    def action_draft(self):
        for record in self:
            record.state = 'draft'

    def action_progress(self):
        for record in self:
            record.state = 'progress'

    def action_finish(self):
        for record in self:
            record.state = 'finished'
            lessons = self.env['music.school.lesson'].search([('course_id','=',record.id), ('state', '!=', 'cancelled')])
            lessons.write({'state': 'done'})


    # Calcular la duracion del curso
    @api.depends('start_date', 'end_date')
    def _compute_duration_days(self):
        for record in self:
            if record.start_date and record.end_date and record.end_date > record.start_date:
                record.duration_days = (record.end_date - record.start_date).days
            else:
                record.duration_days = 0
                