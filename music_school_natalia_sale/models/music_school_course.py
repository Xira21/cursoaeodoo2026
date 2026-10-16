from odoo import models, fields, api

class MusicSchoolCourse(models.Model):
    _inherit = 'music.school.course'

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
    )

    price = fields.Float(string="Price")

    order_ids = fields.One2many(
        comodel_name="sale.order",
        string="Orders",
        inverse_name="course_id",
    )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.price = self.product_id.lst_price
        
