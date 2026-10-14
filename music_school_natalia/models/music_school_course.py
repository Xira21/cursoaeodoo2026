from odoo import models, fields, api, Command, _
from odoo.exceptions import ValidationError

class MusicSchoolCourse(models.Model):
    _name = "music.school.course"
    _description = "Courses"

    name = fields.Char(string="Name", required=True)
    # Restriccion con _sql_constraints
    _name_unique=models.Constraint('UNIQUE(name)','The name must be unique.')

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

    start_date = fields.Date(string="Start Date", default=fields.Date.context_today)

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

    # Campo calculado para smartbutton de ver los examenes de ese curso.
    exam_count = fields.Integer(string="Exams Count", compute="_compute_exam_count")

    def _compute_exam_count(self):
        for record in self:
            record.exam_count = self.env['music.school.exam'].search_count([
                ('course_id','=',record.id)
            ])

    def action_view_exams(self):
        return{
            'type': 'ir.actions.act_window',
            'name': 'Exams',
            'res_model': 'music.school.exam',
            'view_mode': 'kanban,list,form',
            'domain': [('course_id', '=', self.id)],
            'context': {'default_course_id': self.id}
        }


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

    # Constrains -> capacidad no negativa
    @api.constrains('capacity')
    def _check_capacity(self):
        for record in self:
            if record.capacity and record.capacity < 0:
                raise ValidationError(_("The capacity cannot be negative."))

  
                