from odoo import models, fields, _

class MusicSchoolTeacher(models.Model):
    _name = "music.school.teacher"
    _description = "Teachers"

    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")

    level = fields.Selection(
        selection=[
            ('beginner','Beginner'),
            ('intermediate','Intermediate'),
            ('advanced','Advanced'),
        ],
        string="Level",
        default='beginner',
    )

    # Smartbutton desde profesor nos lleve a los cursos que imparte
    course_count = fields.Integer(string="Courses", compute="_compute_course_count")

    def _compute_course_count(self):
        for record in self:
            record.course_count = self.env['music.school.course'].search_count([
                ('teacher_id', '=', record.id)
            ])

    def action_view_courses(self):
        return{
            'type': 'ir.actions.act_window',
            'name': _('Courses'),
            'res_model': 'music.school.course',
            'view_mode': 'kanban,list,form',
            'domain': [('teacher_id', '=', self.id)],
            'context': {'default_teacher_id': self.id}
        }