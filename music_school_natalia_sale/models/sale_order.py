from odoo import models, fields, Command


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    course_id = fields.Many2one(
        comodel_name="music.school.course",
        string="Course",
    )

    # Botón Confirmar HEREDADO: si el pedido lleva un producto de tipo curso, se crea el curso
    def action_confirm(self):
        res = super().action_confirm()
        Course = self.env['music.school.course']
        Student = self.env['music.school.student']
        for order in self:
            # Los pedidos creados desde un curso (botón Create Orders) ya tienen curso
            if order.course_id:
                continue
            course_lines = order.order_line.filtered(lambda line: line.product_id.is_course)
            if not course_lines:
                continue

            # El cliente pasa a ser alumno del curso (se crea si todavía no existe)
            student = Student.search([('partner_id', '=', order.partner_id.id)], limit=1)
            if not student:
                student = Student.create({'partner_id': order.partner_id.id})

            for line in course_lines:
                course = Course.create({
                    'name': f"{line.product_id.name} - {order.name}",
                    'product_id': line.product_id.id,
                    'price': line.price_unit,
                    'company_id': order.company_id.id,
                    'student_ids': [Command.link(student.id)],
                })
                # El pedido queda enlazado al (primer) curso creado
                if not order.course_id:
                    order.course_id = course
        return res
