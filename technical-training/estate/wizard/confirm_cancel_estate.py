from odoo import models, fields, api
from odoo.exceptions import UserError

class ConfirmCancelWizard(models.TransientModel):
    _name = 'confirm.cancel.wizard'
    _description = 'Confirm Cancel Wizard'

    reason_cancel = fields.Text(string="Reason for Cancellation", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)

    def confirm_cancel(self):
        if not self.reason_cancel:
            raise UserError("You must provide a reason for cancellation.")
        
        property_record = self.property_id
        property_record.state = 'canceled'
        property_record.reason_cancel = self.reason_cancel
        
        # Từ chối tất cả các offer liên quan
        for offer in property_record.offer_ids:
            offer.status = 'refused'
        
        return {'type': 'ir.actions.act_window_close'}
