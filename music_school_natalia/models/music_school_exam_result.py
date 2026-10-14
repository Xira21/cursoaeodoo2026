from odoo import api, models, fields

class MusicSchoolExamResult(models.Model):
    _name = 'music.school.exam.result'
    _description = 'Exam Results'

    exam_id = fields.Many2one(
        comodel_name='music.school.exam',
        string='Exam',
        ondelete='cascade'
    )
    
    student_id = fields.Many2one(comodel_name='music.school.student', string='Student', required=True)
    score = fields.Float(string='Score')
    passed = fields.Boolean(string='Passed', compute='_compute_passed', store=True)
    comments = fields.Text(string='Comments') 

    student_ids = fields.Many2many(
        comodel_name='music.school.student',
        related='exam_id.course_id.student_ids',
        string='Students',
    )
    
    # Calcular si el alumno ha aprobado o no, en función de la nota mínima
    @api.depends('score', 'exam_id.min_score')
    def _compute_passed(self):
        for record in self:
            record.passed = record.score >= record.exam_id.min_score if record.exam_id else False