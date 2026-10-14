from odoo import models, fields, Command, api


class MusicSchoolExam(models.Model):
    _name = 'music.school.exam'
    _description = 'Music School Exam'

    name = fields.Char(string='Exam Name', required=True)
    course_id = fields.Many2one(comodel_name='music.school.course', string='Course', required=True)
    date = fields.Datetime(string='Exam Date', required=True)
    instrument_id = fields.Many2one(
        comodel_name='music.school.instrument', 
        string='Instrument', 
        related='course_id.instrument_id',
        store=True,
    )
    min_score = fields.Float(string='Min Score')
    max_score = fields.Float(string='Max Score')
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('scheduled', 'Scheduled'),
            ('finished', 'Finished'),
        ],
        string="State",
        default='draft',
        group_expand=True,
    )

    teacher_id = fields.Many2one(
        comodel_name='music.school.teacher', 
        string='Teacher', 
        required=True,
    )

    result_ids = fields.One2many(
        comodel_name='music.school.exam.result',
        inverse_name='exam_id', 
        string='Results'
    )

    color = fields.Integer(string="Color")

    course_level = fields.Selection(related='course_id.level')

    @api.onchange('course_id')
    def _onchange_course_id(self):
        self.teacher_id = self.course_id.teacher_id

    def action_draft(self):
        for record in self:
            record.state = 'draft'

    def action_scheduled(self):
        for record in self:
            record.state = 'scheduled'

    def action_finish(self):
        for record in self:
            record.state = 'finished'


    def action_result(self):
        for record in self:            
            students = record.course_id.student_ids
            existing = record.result_ids.student_id
            missing = students - existing
            record.result_ids = [
                Command.create({'student_id': student.id}) 
                for student in missing
            ]

            