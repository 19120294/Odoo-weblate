# from odoo import http
# from odoo.http import request

# class FeedbackController(http.Controller):

#     @http.route('/feedback/submit', type='http', auth="public", methods=['POST'], csrf=False)
#     def submit_feedback(self, **kwargs):
#         feedback_description = kwargs.get('description')

#         if feedback_description:
#             # Lưu feedback vào database
#             request.env['website.user.feedback'].sudo().create({
#                 'description': feedback_description,
#             })
#             return request.redirect('/thank-you')  # Chuyển hướng đến trang cảm ơn

#         return request.redirect('/feedback-error')  # Chuyển hướng nếu xảy ra lỗi

#     @http.route('/thank-you', type='http', auth="public", website=True)
#     def thank_you(self, **kwargs):
#         return request.render('estate.thank_you_page')

from odoo import http
from odoo.http import request
from werkzeug.utils import redirect  # Import redirect từ werkzeug

class FeedbackController(http.Controller):

    @http.route('/feedback/submit', type='http', auth="public", methods=['POST'], csrf=False)
    def submit_feedback(self, **kwargs):
        feedback_description = kwargs.get('description')

        if feedback_description:
            # Lưu feedback vào database
            request.env['website.user.feedback'].sudo().create({
                'description': feedback_description,
            })
            return redirect('/thank-you')  # Chuyển hướng đến trang cảm ơn

        return redirect('/feedback-error')  # Chuyển hướng nếu xảy ra lỗi

    @http.route('/thank-you', type='http', auth="public", website=True)
    def thank_you(self, **kwargs):
        return request.render('estate.thank_you_page')

    @http.route('/feedback-error', type='http', auth="public", website=True)
    def feedback_error(self, **kwargs):
        return request.render('estate.feedback_error_page')

