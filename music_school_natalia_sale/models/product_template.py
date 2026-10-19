from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Marca el producto como "curso": al confirmar un pedido que lo lleve, se crea un curso
    is_course = fields.Boolean(string="Is a Course")
