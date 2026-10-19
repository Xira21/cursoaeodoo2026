from odoo import models, fields, api, Command, _
from odoo.exceptions import UserError

class MusicSchoolCourse(models.Model):
    _inherit = 'music.school.course'

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
    )

    # tracking=True: cada cambio de precio queda anotado en el chatter del curso
    price = fields.Float(string="Price", tracking=True)

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

    # Botón de cancelar el curso HEREDADO
    def action_cancel(self):
        res = super().action_cancel()
        self.order_ids.action_cancel()
        return res

    # Botón de confirmar la venta y facturar el pedido asociado
    def action_confirm_and_invoice(self):
        for record in self:
            # 1. Confirmar los presupuestos
            draft_orders = record.order_ids.filtered(lambda o: o.state in ('draft', 'sent'))
            draft_orders.action_confirm()

            # 2. Facturar lo pendiente
            to_invoice = record.order_ids.filtered(lambda o: o.invoice_status == 'to invoice')
            if to_invoice:
                to_invoice._create_invoices()
                
            # 3. Publicar las facturas en borrador
            draft_invoices = record.order_ids.invoice_ids.filtered(lambda i: i.state == 'draft')
            draft_invoices.action_post()



                            
