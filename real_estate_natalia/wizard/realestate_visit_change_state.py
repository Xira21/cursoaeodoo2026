from odoo import models, fields

class RealEstateVisitChangeState(models.TransientModel):
    _name = "realestate.visit.change.state"
    _description = "Change Visit State"

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("done", "Done"),
            ("cancelled", "Cancelled")
        ],
        string="State",
        required=True
    )

    def action_change_state(self):
        active_ids = self.env.context.get('active_ids')
        # active_ids = self.env.context.get('active_ids',[]) -> Hacerlo asi para que si no encuentra ninguno ponga vacio
        visits = self.env['realestate.visit'].browse(active_ids)
        visits.write({'state': self.state})
        return{
            'type': 'ir.actions.act_window',
            'name': 'Change State',
            'res_model': 'realestate.visit',
            'view_mode': 'list,form',
            'domain': [('id', 'in', active_ids)],
        }