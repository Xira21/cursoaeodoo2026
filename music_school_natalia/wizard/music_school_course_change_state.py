from odoo import models, fields

class MusicSchoolCourseChangeState(models.TransientModel):
    _name = "music.school.course.change.state"
    _description = "Change Course State"

    state = fields.Selection(
        selection=[
            ('draft','Draft'),
            ('progress','In Progress'),
            ('finished','Finished'),
        ],
        string="State",
        required=True,
    )

    def action_change_state(self):
        courses = self.env['music.school.course'].browse(self.env.context.get('active_ids'))       
        if self.state == 'finished':
            courses.action_finish()
        else:
            courses.write({'state': self.state})
