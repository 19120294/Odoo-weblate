from odoo import http
from odoo.http import request
from datetime import datetime


class EstatePropertyReportController(http.Controller):

    @http.route("/estate/property_report_xlsx", type="http", auth="user", csrf=False)
    def buyer_offer_report_xlsx(self, start_date, end_date, buyer_ids):
        # Capture the parameters from the URL
        # start_date = kwargs.get("start_date")
        # end_date = kwargs.get("end_date")
        # buyer_id = kwargs.get("buyer_id")

        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        buyer_ids = [int(bid) for bid in buyer_ids.split(",")] if buyer_ids else []

        # Generate the XLSX report
        report = request.env["estate.property_report_xlsx"]
        # file_content = report.create_xlsx_report(data)
        file_content = report.create_xlsx_report(start_date, end_date, buyer_ids)
        # Return the file as an attachment
        filename = "Buyer_Offer_Report.xlsx"
        headers = [
            (
                "Content-Type",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ),
            ("Content-Disposition", f"attachment; filename={filename}"),
        ]

        return request.make_response(file_content, headers=headers)
        # return response

