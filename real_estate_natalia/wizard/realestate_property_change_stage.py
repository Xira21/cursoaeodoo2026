from odoo import models, fields

class RealEstatePropertyChangeStage(models.TransientModel):
    _name = "realestate.property.change.stage"
    _description = "Change Property Stage"

    stage_id = fields.Many2one(
        comodel_name ="realestate.property.stage",
        string="Stage",
        required=True
    )

    def action_change_stage(self):
        active_ids = self.env.context.get('active_ids')
        properties = self.env['realestate.property'].browse(active_ids)
        properties.write({'stage_id': self.stage_id.id})
        return{
            'type': 'ir.actions.act_window',
            'name': 'Change Stage',
            'res_model': 'realestate.property',
            'view_mode': 'list,form',
            'domain': [('id', 'in', active_ids)],
        }