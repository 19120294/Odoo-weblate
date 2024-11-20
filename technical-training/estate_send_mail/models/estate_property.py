# models/estate_property.py
import re

from odoo import _,  models, fields, api
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    buyer_email = fields.Char(
        string="Buyer Email",
        help="Buyer email",
        required=False
    )
    user_sold = fields.Many2one(
        'res.users',
        string="User Sold",
        readonly=True,
    )

    @api.onchange('buyer_id')
    def _load_buyer_email(self):
        for record in self:
            if record.buyer_id:
                record.buyer_email = record.buyer_id.email


    def send_mail_to_buyer(self):
        for record in self:
            if record.state == 'sold':
                mail_template = self.env.ref('estate_send_mail.email_template_property_sold')
                mail_template.sudo().send_mail(record.id, force_send=True)

    def action_sold(self):
        super(EstateProperty, self).action_sold()
        self.user_sold = self.env.user
        self.send_mail_to_buyer

    @api.constrains('buyer_email')
    def _check_buyer_email(self):
        for record in self:
            # Kiểm tra nếu buyer_email không rỗng và có định dạng email hợp lệ hay không
            if record.buyer_email:
                # Biểu thức chính quy dùng để kiểm tra email có hợp lệ không
                # ^[^@]+: Phần tên người dùng không chứa ký tự '@'
                # @[^@]+: Sau dấu '@' không chứa ký tự '@' và tiếp theo là domain
                # \.[^@]+$: Kết thúc bằng dấu '.' và domain sau đó không chứa ký tự '@'
                email_regex = r"[^@]+@[^@]+\.[^@]+"

                # Sử dụng re.match để kiểm tra xem buyer_email có khớp với biểu thức chính quy không
                if not re.match(email_regex, record.buyer_email):
                    # Nếu không hợp lệ, ném ra một ValidationError với thông báo lỗi
                    raise ValidationError(_("The email address provided for the buyer is not in a valid format. Please enter a valid email address"))