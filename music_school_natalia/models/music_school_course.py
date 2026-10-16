from odoo import models, fields, api, Command, _
from odoo.exceptions import ValidationError

class MusicSchoolCourse(models.Model):
    _name = "music.school.course"
    _description = "Courses"

    name = fields.Char(string="Name", copy=False)
    # Restriccion con _sql_constraints
    _name_unique = models.Constraint('UNIQUE(name)','The name must be unique.')
    active = fields.Boolean(string="Active", default=True)

    description = fields.Text(string="Description", company_dependent=True)
    state = fields.Selection(
        selection=[
            ('draft','Draft'),
            ('progress','In Progress'),
            ('finished','Finished'),
            ('cancelled','Cancelled'),
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

    company_id = fields.Many2one(
        comodel_name='res.company',
        string="Company",
        default=lambda self: self.env.company
    )

    code = fields.Char(string="Code", readonly=True, copy=False)

    # Campo calculado para smartbutton de ver los examenes de ese curso.
    exam_count = fields.Integer(string="Exams Count", compute="_compute_exam_count")

    # Campo calculado para smartbutton de ver las lecciones asociadas.
    lesson_count = fields.Integer(string="Lesson Count", compute="_compute_lesson_count")

    def _compute_exam_count(self):
        for record in self:
            record.exam_count = self.env['music.school.exam'].search_count([
                ('course_id','=', record.id)
            ])

    def _compute_lesson_count(self):
        for record in self:
            record.lesson_count = self.env['music.school.lesson'].search_count([
                ('course_id', '=', record.id)
            ])

    def action_view_exams(self):
        return{
            'type': 'ir.actions.act_window',
            'name': _('Exams'),
            'res_model': 'music.school.exam',
            'view_mode': 'kanban,list,form',
            'domain': [('course_id', '=', self.id)],
            'context': {'default_course_id': self.id}
        }

    def action_view_lessons(self):
        return{
            'type': 'ir.actions.act_window',
            'name': _('Lessons'),
            'res_model': 'music.school.lesson',
            'view_mode': 'kanban,list,form,pivot,graph,calendar',
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

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'


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

    # Constrains -> fecha fin no puede ser anterior a la de inicio
    @api.constrains('start_date', 'end_date')
    def _check_end_date(self):
        for record in self:
            if record.start_date and record.end_date and record.end_date < record.start_date:
                raise ValidationError(_("The end date cannot be before start date"))
            
    # Metodo para el cron
    def _cron_finished_courses(self):
        courses = self.env['music.school.course'].search([
            ('state', '=', 'progress'),
            ('end_date', '<', fields.Date.context_today(self)),
        ])
        courses.action_finish()

    # Heredar el Metodo crear añadiendo una secuencia a los cursos
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code('music.school.course')
        return super().create(vals_list)