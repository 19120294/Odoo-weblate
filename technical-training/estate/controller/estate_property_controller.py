from datetime import datetime

from odoo import http
from odoo.http import request, Response
import json


class EstatePropertyController(http.Controller):

    @http.route("/estate_property", auth="public", type="http", website=True)
    def list_estate_property(self, page=1, search="", **kwargs):
        """Hiển thị danh sách bất động sản với tìm kiếm và phân trang"""
        # Số lượng bản ghi mỗi trang
        estates_per_page = 12

        # Xử lý tham số
        try:
            page = max(int(page), 1)  # Đảm bảo page >= 1
        except ValueError:
            page = 1
        search = str(search).strip()

        # Lấy các bất động sản từ cơ sở dữ liệu
        domain = []
        if search:
            domain = [("name", "ilike", search)]

        total_estates = request.env["estate.property"].sudo().search_count(domain)
        estates = (
            request.env["estate.property"]
            .sudo()
            .search(
                domain, offset=(page - 1) * estates_per_page, limit=estates_per_page
            )
        )

        # Render trang
        return request.render(
            "estate.estate_pages",
            {
                "estates": estates,
                "total_estates": total_estates,
                "page": page,
                "estates_per_page": estates_per_page,
                "search": search,
            },
        )

    @http.route("/estates/<int:estate_id>", type="http", auth="public", website=True)
    def estate_details(self, estate_id, **kwargs):
        """Hiển thị chi tiết một bất động sản"""
        # Lấy bản ghi theo ID
        estate = request.env["estate.property"].sudo().browse(estate_id)

        # Kiểm tra nếu không tồn tại
        if not estate.exists():
            return request.render(
                "website.404", {}
            )  # Trả về trang lỗi 404 nếu không tìm thấy

        # Hiển thị chi tiết
        return request.render(
            "estate.estate_details",
            {
                "estate": estate,
            },
        )


class EstateApi(http.Controller):

    @http.route("/api/estates", type="http", auth="public", methods=["GET"], csrf=False)
    def get_estates(self, **kwargs):
        estates = (
            request.env["estate.property"].sudo().search([])
        )  # Sử dụng .sudo() khi truy vấn dữ liệu
        estate_data = []
        for estate in estates:
            # Chuyển đổi date_availability thành chuỗi định dạng "YYYY-MM-DD"
            date_availability = (
                estate.date_availability.strftime("%Y-%m-%d")
                if estate.date_availability
                else None
            )
            estate_data.append(
                {
                    "id": estate.id,
                    "name": estate.name,
                    "description": estate.description,
                    "expected_price": estate.expected_price,
                    "selling_price": estate.selling_price,
                    "bedrooms": estate.bedrooms,
                    "living_area": estate.living_area,
                    "facades": estate.facades,
                    "garden": estate.garden,
                    "date_availability": date_availability,  # Đảm bảo là chuỗi
                    "state": estate.state,
                }
            )

        # Trả về dữ liệu JSON
        return Response(
            json.dumps(estate_data), content_type="application/json", status=200
        )

    @http.route(
        "/api/estates", type="json", auth="public", methods=["POST"], csrf=False
    )
    def create_estate(self, **kwargs):
        data = request.jsonrequest
        try:
            # Sử dụng .sudo() để đảm bảo người dùng có thể tạo bản ghi mà không bị giới hạn quyền
            estate = (
                request.env["estate.property"]
                .sudo()
                .create(
                    {
                        "name": data.get("name"),
                        "description": data.get("description"),
                        "expected_price": data.get("expected_price"),
                        "bedrooms": data.get("bedrooms"),
                        "living_area": data.get("living_area"),
                        "facades": data.get("facades"),
                        "garden": data.get("garden"),
                        "date_availability": data.get("date_availability"),
                        "state": data.get("state", "new"),
                    }
                )
            )
            return Response(
                json.dumps({"status": "success", "id": estate.id}),
                content_type="application/json",
                status=201,
            )
        except Exception as e:
            return Response(
                json.dumps({"status": "error", "message": str(e)}),
                content_type="application/json",
                status=400,
            )

    @http.route(
        "/api/estates/<int:estate_id>",
        type="json",
        auth="public",
        methods=["PUT"],
        csrf=False,
    )
    def update_estate(self, estate_id, **kwargs):
        data = request.jsonrequest
        estate = (
            request.env["estate.property"].sudo().browse(estate_id)
        )  # Sử dụng .sudo() để đảm bảo quyền truy cập bản ghi
        if not estate:
            return Response(
                json.dumps({"status": "error", "message": "Estate not found"}),
                content_type="application/json",
                status=404,
            )

        try:
            estate.write(
                {
                    "name": data.get("name", estate.name),
                    "description": data.get("description", estate.description),
                    "expected_price": data.get("expected_price", estate.expected_price),
                    "bedrooms": data.get("bedrooms", estate.bedrooms),
                    "living_area": data.get("living_area", estate.living_area),
                    "facades": data.get("facades", estate.facades),
                    "garden": data.get("garden", estate.garden),
                    "date_availability": data.get(
                        "date_availability", estate.date_availability
                    ),
                    "state": data.get("state", estate.state),
                }
            )
            return Response(
                json.dumps({"status": "success", "id": estate.id}),
                content_type="application/json",
                status=200,
            )
        except Exception as e:
            return Response(
                json.dumps({"status": "error", "message": str(e)}),
                content_type="application/json",
                status=400,
            )

    @http.route(
        "/api/estates/<int:estate_id>",
        type="json",
        auth="public",
        methods=["PATCH"],
        csrf=False,
    )
    def patch_estate(self, estate_id, **kwargs):
        data = request.jsonrequest
        estate = (
            request.env["estate.property"].sudo().browse(estate_id)
        )  # Sử dụng .sudo() để đảm bảo quyền truy cập bản ghi
        if not estate:
            return Response(
                json.dumps({"status": "error", "message": "Estate not found"}),
                content_type="application/json",
                status=404,
            )

        try:
            estate.write(
                {
                    "name": data.get("name", estate.name),
                    "description": data.get("description", estate.description),
                    "expected_price": data.get("expected_price", estate.expected_price),
                    "bedrooms": data.get("bedrooms", estate.bedrooms),
                    "living_area": data.get("living_area", estate.living_area),
                    "facades": data.get("facades", estate.facades),
                    "garden": data.get("garden", estate.garden),
                    "date_availability": data.get(
                        "date_availability", estate.date_availability
                    ),
                    "state": data.get("state", estate.state),
                }
            )
            return Response(
                json.dumps({"status": "success", "id": estate.id}),
                content_type="application/json",
                status=200,
            )
        except Exception as e:
            return Response(
                json.dumps({"status": "error", "message": str(e)}),
                content_type="application/json",
                status=400,
            )

    @http.route(
        "/api/estates/<int:estate_id>",
        type="http",
        auth="public",
        methods=["DELETE"],
        csrf=False,
    )
    def delete_estate(self, estate_id, **kwargs):
        estate = (
            request.env["estate.property"].sudo().browse(estate_id)
        )  # Sử dụng .sudo() khi thao tác với bản ghi
        if not estate:
            return Response(
                json.dumps({"status": "error", "message": "Estate not found"}),
                content_type="application/json",
                status=404,
            )

        try:
            estate.unlink()
            return Response(
                json.dumps(
                    {"status": "success", "message": "Estate deleted successfully"}
                ),
                content_type="application/json",
                status=200,
            )
        except Exception as e:
            return Response(
                json.dumps({"status": "error", "message": str(e)}),
                content_type="application/json",
                status=400,
            )
