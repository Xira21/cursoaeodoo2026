from odoo import models, fields
from datetime import timedelta

class RealEstatePropertyConfirmedVisits(models.TransientModel):
    _name = "realestate.property.confirmed.visits"
    _description = "Confirmed Property Visits"

    start_date = fields.Datetime(string="Start Date", required=True)
    end_date = fields.Datetime(string="End Date", required=True)

    def action_create_visits(self):
        properties = self.env['realestate.property'].browse(self.env.context.get('active_ids'))
        vals_list=[]
        
        for real_property in properties:
            current_date = self.start_date
            while current_date <= self.end_date:
                vals_list.append({
                    'property_id':real_property.id,
                    'date': current_date,
                    'user_id': real_property.user_id.id,
                    'state': 'confirmed'
                })
                current_date += timedelta(days=1)

        visits = self.env['realestate.visit'].create(vals_list)
        return{
            'type': 'ir.actions.act_window',
            'name': 'Confirmed Visits',
            'res_model': 'realestate.visit',
            'view_mode': 'list,form',
            'domain': [('id', 'in', visits.ids)],
        }


    
    
