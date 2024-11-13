from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyReportWizard(models.TransientModel):
    _name = "estate.property.report.wizard"
    _description = "Estate Property Report Wizard"

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    buyer_ids = fields.Many2many("res.partner", string="Buyers")

    def action_export_xlsx(self):
        # Kiểm tra ngày bắt đầu và ngày kết thúc
        # if self.start_date > self.end_date:
        #     raise UserError("Start Date must be before End Date!")

        # start_date = self.start_date
        # end_date = self.end_date
        # # buyer_id = self.buyer_id.id if self.buyer_id else None  
        # # buyer_ids = ','.join(map(str, self.buyer_id.ids))
        # buyer_ids = ','.join(map(str, self.buyer_ids.ids)) if self.buyer_ids else ''

        # if buyer_ids:
        #     url = f'/estate/property_report_xlsx?start_date={start_date}&end_date={end_date}&buyer_id={buyer_ids}'
        # else:
        #     url = f'/estate/property_report_xlsx?start_date={start_date}&end_date={end_date}'

        # return {
        #     'type': 'ir.actions.act_url',
        #     'url': url,
        #     'target': 'self',  
        # }
        # Gọi controller để xuất báo cáo
        buyer_ids = ','.join(map(str, self.buyer_ids.ids)) if self.buyer_ids else ''
        return {
            'type': 'ir.actions.act_url',
            'url': f'/estate/property_report_xlsx?start_date={self.start_date}&end_date={self.end_date}&buyer_ids={buyer_ids}',
            'target': 'self',
        }
