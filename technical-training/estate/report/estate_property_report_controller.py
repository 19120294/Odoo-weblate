from odoo import http
from odoo.http import request
import io
import xlsxwriter
from datetime import datetime


class EstatePropertyReportController(http.Controller):

    @http.route('/estate/property_report_xlsx', type="http", auth="user")
    def get_property_report_xlsx(self, **kw):
        # Lấy tham số từ URL (start_date, end_date, buyer_ids)
        start_date = kw.get("start_date")
        end_date = kw.get("end_date")
        buyer_id = kw.get("buyer_id") # Danh sách các buyer IDs

        report_model = request.env["estate.property_report_xlsx"]
        file_content = report_model.create_xlsx_report(start_date, end_date, buyer_id)

        headers = (
            [
                (
                    "Content-Type",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ),
                ('Content-Disposition', 'attachment; filename="Estate_Property_Report.xlsx"'),
            ],
        )
        
        return request.make_response(file_content, headers=headers)