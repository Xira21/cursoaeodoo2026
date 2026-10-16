from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    course_id = fields.Many2one(
        comodel_name="music.school.course",
        string="Course",
    )