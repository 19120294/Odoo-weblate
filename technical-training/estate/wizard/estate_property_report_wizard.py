from odoo import models, fields
from odoo.exceptions import UserError


class EstatePropertyReportWizard(models.TransientModel):
    _name = "estate.property.report.wizard"
    _description = "Estate Property Report Wizard"

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    buyer_ids = fields.Many2many("res.partner", string="Buyers")

    def action_export_xlsx(self):
        # Kiểm tra ngày bắt đầu và ngày kết thúc
        if self.start_date > self.end_date:
            raise UserError("Start Date must be before End Date!")

        start_date = self.start_date
        end_date = self.end_date
        buyer_ids = ','.join(map(str, self.buyer_ids.ids)) if self.buyer_ids else ''
        return {
            'type': 'ir.actions.act_url',
            'url': f'/estate/property_report_xlsx?start_date={self.start_date}&end_date={self.end_date}&buyer_ids={buyer_ids}',
            'target': 'self',
        }
