from odoo import fields, models, tools
import logging

_logger = logging.getLogger(__name__)


class EstatePropertyReport(models.Model):
    _name = "estate.property.report"
    _description = "Property Buyers Report"
    _auto = False  # Đặt _auto thành False để cho biết đây là bảng view SQL

    # Các trường trong view
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    property_count = fields.Integer(string="Property Count", readonly=True)
    offer_accepted_count = fields.Integer(string="Accepted Offers", readonly=True)
    offer_rejected_count = fields.Integer(string="Rejected Offers", readonly=True)
    max_price = fields.Float(string="Max Offer Price", readonly=True)
    min_price = fields.Float(string="Min Offer Price", readonly=True)

    ## thêm điều kiện để không xuất hiện dòng trắng
    def init(self):
        tools.drop_view_if_exists(self._cr, "estate_property_report")
        self._cr.execute(
            """
            CREATE VIEW estate_property_report AS (
                SELECT
                    row_number() OVER () AS id,
                    rp.id AS buyer_id,
                    COUNT(ep.id) AS property_count,
                    SUM(CASE WHEN eo.status = 'accepted' THEN 1 ELSE 0 END) AS offer_accepted_count,
                    SUM(CASE WHEN eo.status = 'refused' THEN 1 ELSE 0 END) AS offer_rejected_count,
                    MAX(eo.price) AS max_price,
                    MIN(eo.price) AS min_price
                FROM
                    estate_property AS ep
                LEFT JOIN
                    estate_property_offer AS eo ON ep.id = eo.property_id
                LEFT JOIN
                    res_partner AS rp ON eo.partner_id = rp.id
                WHERE
                    rp.id IS NOT NULL
                GROUP BY
                    rp.id
            )
        """
        )

    def _get_sql_statement(self, start_date=False, end_date=False, buyer_id=False):
        sql_primary = f"""
                row_number() OVER () as id,
                p.buyer_id,
                COUNT(DISTINCT CASE WHEN p.state = 'offer_accepted' THEN p.id END) as count_property_accepted,
                COUNT(DISTINCT CASE WHEN p.state = 'sold' THEN p.id END) as count_property_sold,
                COUNT(DISTINCT CASE WHEN p.state = 'canceled' THEN p.id END) as count_property_canceled,
                COUNT(DISTINCT CASE WHEN o.status = 'accepted' THEN o.id END) as count_offer_accepted,
                COUNT(DISTINCT CASE WHEN o.status = 'refused' THEN o.id END) as count_offer_refused,
                MAX(o.price) as max_offer_price,
                MIN(o.price) as min_offer_price
            FROM estate_property p
            LEFT JOIN estate_property_offer o ON p.id = o.property_id
        """
        if start_date and end_date:
            sql_statement = f"AND p.date_availability >= '{start_date}' AND p.date_availability <= '{end_date}'"
            if buyer_id:
                sql_statement += f" AND p.buyer_id IN ({buyer_id})"
                _logger.info(sql_statement)
            return f"""
                SELECT
                    rp.name as buyer_name,
                    rp.email as buyer_email,
                    {sql_primary}
                LEFT JOIN res_partner rp ON p.buyer_id = rp.id
                WHERE p.buyer_id IS NOT NULL
                {sql_statement}
                GROUP BY p.buyer_id, rp.name, rp.email
            """
        else:
            return f"""
                CREATE OR REPLACE VIEW estate_property_buyer AS (
                    SELECT
                       {sql_primary}
                    WHERE p.buyer_id IS NOT NULL
                    GROUP BY p.buyer_id
                )
            """


    def query_buyer_offer_with_dates(self, start_date=None, end_date=None, buyer_id=None):
        sql_statement = self._get_sql_statement(start_date, end_date,buyer_id)
        self._cr.execute(sql_statement)
        result = self._cr.dictfetchall()
        return result
    
    # def init(self):
    #     tools.drop_view_if_exists(self._cr, "estate_property_report")
    #     self._cr.execute(
    #         """
    #         CREATE VIEW estate_property_report AS (
    #             SELECT
    #                 row_number() OVER () AS id,
    #                 rp.id AS buyer_id,
    #                 COUNT(ep.id) AS property_count,
    #                 SUM(CASE WHEN eo.status = 'accepted' THEN 1 ELSE 0 END) AS offer_accepted_count,
    #                 SUM(CASE WHEN eo.status = 'refused' THEN 1 ELSE 0 END) AS offer_rejected_count,
    #                 MAX(eo.price) AS max_price,
    #                 MIN(eo.price) AS min_price
    #             FROM
    #                 estate_property AS ep
    #             LEFT JOIN
    #                 estate_property_offer AS eo ON ep.id = eo.property_id
    #             LEFT JOIN
    #                 res_partner AS rp ON eo.partner_id = rp.id
    #             GROUP BY
    #                 rp.id
    #         )
    #     """
    #     )
