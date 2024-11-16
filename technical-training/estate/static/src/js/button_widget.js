odoo.define("button_widget", function (require) {
    "use strict";

    var ListController = require("web.ListController");
    var ListView = require("web.ListView");
    var viewRegistry = require("web.view_registry");
    var core = require("web.core");
    var _t = core._t;

    // TreeViewButtonController: Điều khiển hành vi của Tree View khi có nút "Click Me"
    var TreeViewButtonController = ListController.extend({
        // Hàm render lại các nút
        renderButtons: function ($node) {
            this._super.apply(this, arguments);  // Gọi hàm renderButtons mặc định

            // Kiểm tra và thêm nút "Click Me" vào thanh công cụ của Tree View
            if (this.$buttons) {
                var $button = $("<button>", {
                    type: "button",
                    class: "btn btn-primary",  // Class của nút
                    text: _t("Click Me"),  // Văn bản của nút
                }).on("click", this._onButtonClick.bind(this));  // Gắn sự kiện click

                // Thêm nút vào đầu của các nút trong Tree View
                this.$buttons.prepend($button);
            }
        },

        // Hàm xử lý sự kiện khi nhấn nút
        _onButtonClick: function () {
            this.do_notify(
                _t("'Inventory Overview' added to dashboard"),  // Tiêu đề thông báo
                _t("Please refresh your browser for the changes to take effect")  // Nội dung thông báo
            );
        },
    });

    // Định nghĩa một List View mới sử dụng controller tùy chỉnh
    var TreeViewButtonListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TreeViewButtonController,  // Sử dụng controller mới
        }),
    });

    // Đăng ký view này vào hệ thống Odoo
    viewRegistry.add("button_widget", TreeViewButtonListView);
});
