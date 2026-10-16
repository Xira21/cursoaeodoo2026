from odoo import models, fields, api, Command, _
from odoo.exceptions import UserError

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

    # Boton crea pedido de venta, tantos pedidos como estudiantes haya.
    def action_create_orders(self):
        for record in self:
            if not record.product_id: 
                raise UserError(_("Set a product on the course before creating orders."))
            
            partners = record.student_ids.partner_id - record.order_ids.partner_id
            for partner in partners:
                self.env['sale.order'].create({
                    'partner_id': partner.id,
                    'course_id': record.id,
                    'company_id': record.company_id.id,
                    'order_line': [Command.create({
                        'product_id': record.product_id.id,
                        'price_unit': record.price,
                        'product_uom_qty': 1,
                    })]
                })                                                             
                                            
                            
