from odoo import fields, models, tools
# import logging

# _logger = logging.getLogger(__name__)


class EstatePropertyReport(models.Model):
    _name = "estate.property.report"
    _description = "Property Buyers Report"
    _auto = False  # Đặt _auto thành False để cho biết đây là bảng view SQL

    # Các trường trong view
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    property_count = fields.Integer(string="Property Count", readonly=True)
    properties_accepted = fields.Integer(string='Accepted Properties')
    properties_sold = fields.Integer(string='Sold Properties')
    properties_canceled = fields.Integer(string='Canceled Properties')
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
