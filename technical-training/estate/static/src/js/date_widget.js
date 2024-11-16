odoo.define("estate.date_widget", function (require) {
    "use strict";

    var FieldDate = require("web.basic_fields").FieldDate; // Kế thừa từ FieldDate
    var fieldRegistry = require("web.field_registry");
    var field_utils = require("web.field_utils"); // Dùng để xử lý dữ liệu ngày
    // var moment = require("moment"); // Thư viện xử lý ngày tháng

    var DateMMYYYYWidget = FieldDate.extend({
        supportedFieldTypes: ["date"],

        /**
         * Chuyển đổi ngày sang định dạng MM/YYYY
         */
        _formatDateMMYYYY: function (date) {
            if (!date) {
                return "";
            }
            var dateObj = field_utils.parse.date(date); // Chuyển từ chuỗi sang object date
            if (dateObj) {
                return moment(dateObj).format("MM/YYYY"); // Định dạng MM/YYYY
            }
            return "";
        },

        /**
         * Hiển thị chế độ readonly (MM/YYYY)
         */
        _renderReadonly: function () {
            this.$el.empty();
            var formattedDate = this._formatDateMMYYYY(this.value);
            this.$el.text(formattedDate || "MM/YYYY");
        },

        /**
         * Giữ nguyên logic chỉnh sửa (edit) từ FieldDate
         */
        _renderEdit: function () {
            // Hiển thị ngày gốc trong chế độ chỉnh sửa
            this._super.apply(this, arguments);
        },

        /**
         * Sử dụng FieldDate để hiển thị trong form.
         */
        start: function () {
            this._super.apply(this, arguments);
        },
    });

    // Đăng ký widget
    fieldRegistry.add("date_widget", DateMMYYYYWidget);

    return DateMMYYYYWidget;
});
