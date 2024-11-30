from odoo import models, fields

class WebsiteUserFeedback(models.Model):
    _name = "website.user.feedback"
    _description = "User Feedback"

    description = fields.Text(string="Feedback Description", required=True)
    create_datetime = fields.Datetime(string="Submitted On", default=fields.Datetime.now)
