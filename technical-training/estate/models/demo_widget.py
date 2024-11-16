import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class DemoWidget(models.Model):
    _name = "demo.widget"
    _description = "Demo Widget"

    name = fields.Char(string="Name")
    color = fields.Integer(string="Color")
    date = fields.Date(string="Date")

    @api.model
    def count_color(self):
        count_color = len(self.search([("color", "!=", 0)]))
        _logger.info("count_color" + str(count_color))
        return count_color
