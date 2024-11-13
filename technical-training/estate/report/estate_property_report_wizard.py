# from odoo import fields, models, api
# from odoo.exceptions import UserError


# class EstatePropertyReportWizard(models.TransientModel):
#     _name = "estate.property.report.wizard"
#     _description = "Estate Property Report Wizard"

#     start_date = fields.Date(string="Start Date", required=True)
#     end_date = fields.Date(string="End Date", required=True)
#     buyer_ids = fields.Many2many("res.partner", string="Buyers")

#     @api.model
#     def default_get(self, fields):
#         res = super(EstatePropertyReportWizard, self).default_get(fields)
#         return res

#     def action_export_xlsx(self):
#         # Validate date range
#         if self.start_date > self.end_date:
#             raise UserError("Start Date must be before End Date!")

#         # Prepare the domain for filtering the properties
#         domain = [
#             ('offer_ids.date_deadline', '>=', self.start_date),
#             ('offer_ids.date_deadline', '<=', self.end_date)
#         ]

#         if self.buyer_ids:
#             domain.append(('buyer_id', 'in', self.buyer_ids.ids))

#         # Fetch filtered properties based on the criteria
#         properties = self.env['estate.property'].search(domain)

#         if not properties:
#             raise UserError("No data found for the selected criteria.")

#         # Generate XLSX report (ensure the report action exists)
#         return self.env.ref('estate.action_property_report_xlsx').report_action(self, data={
#             'properties': properties,
#             'start_date': self.start_date,
#             'end_date': self.end_date
#         })

#     # def action_export_xlsx(self):
#     #     # Kiểm tra ngày bắt đầu và ngày kết thúc
#     #     if self.start_date > self.end_date:
#     #         raise UserError("Start Date must be before End Date!")

#     #     # Trả về hành động URL để gọi controller
#     #     return {
#     #         "type": "ir.actions.act_url",
#     #         "url": f"/estate/buyer_offer_report_xlsx?start_date={self.start_date}&end_date={self.end_date}&buyer_ids={self.buyer_id.id}",
#     #         "target": "self",
#     #     }

#     def action_cancel(self):
#         # Close the wizard without doing anything
#         return {"type": "ir.actions.act_window_close"}

from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyReportWizard(models.TransientModel):
    _name = "estate.property.report.wizard"
    _description = "Estate Property Report Wizard"

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    buyer_id = fields.Many2one("res.partner", string="Buyers", required=True)

    def action_export_xlsx(self):
        # Kiểm tra ngày bắt đầu và ngày kết thúc
        if self.start_date > self.end_date:
            raise UserError("Start Date must be before End Date!")

        start_date = self.start_date
        end_date = self.end_date
        buyer_id = self.buyer_id.id if self.buyer_id else None  
        # buyer_ids = ','.join(map(str, self.buyer_id.ids))
        
        if buyer_id:
            url = f'/estate/property_report_xlsx?start_date={start_date}&end_date={end_date}&buyer_id={buyer_id}'
        else:
            url = f'/estate/property_report_xlsx?start_date={start_date}&end_date={end_date}'

        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',  
        }
        # Trả về hành động URL để gọi controller
        # return {
        #     "type": "ir.actions.act_url",
        #     "url": f"/estate/property_report_xlsx?start_date={self.start_date}&end_date={self.end_date}&buyer_id={buyer_ids}",
        #     "target": "self",
        # }
