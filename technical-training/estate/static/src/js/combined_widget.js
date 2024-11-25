// odoo.define("combined_widget", function (require) {
//     "use strict";

//     var ListController = require("web.ListController");
//     var ListView = require("web.ListView");
//     var viewRegistry = require("web.view_registry");
//     var core = require("web.core");
//     var _t = core._t;

//     // Kế thừa ListController từ cả hai widget
//     var CombinedWidgetController = ListController.extend({
//         // Hàm render lại các nút
//         renderButtons: function ($node) {
//             // Gọi hàm renderButtons mặc định của cả hai lớp
//             this._super.apply(this, arguments);

//             // Thêm nút "Click Me" từ button_widget
//             if (this.$buttons) {
//                 var $button = $("<button>", {
//                     type: "button",
//                     class: "btn btn-primary",
//                     text: _t("Click Me"),
//                 }).on("click", this._onButtonClick.bind(this));  // Gắn sự kiện click

//                 // Thêm nút vào đầu của các nút trong Tree View
//                 this.$buttons.prepend($button);
//             }

//             // Thêm checkbox "Hide Color" và "Hide Date" từ checkbox_widget
//             var $hideColorCheckbox = $("<label>", { class: "checkbox-inline" }).append(
//                 $("<input>", { type: "checkbox", id: "hide_color" }),
//                 _t(" Hide Color")
//             );

//             var $hideDateCheckbox = $("<label>", { class: "checkbox-inline" }).append(
//                 $("<input>", { type: "checkbox", id: "hide_date" }),
//                 _t(" Hide Date")
//             );

//             // Tạo nút Apply
//             var $applyButton = $("<button>", { 
//                 type: "button", 
//                 class: "btn btn-success apply-btn", 
//                 text: _t("Apply") 
//             }).on("click", this._onApplyClick.bind(this)).hide();

//             // Tạo nút Clear
//             var $clearButton = $("<button>", { 
//                 type: "button", 
//                 class: "btn btn-danger clear-btn", 
//                 text: _t("Clear") 
//             }).on("click", this._onClearClick.bind(this)).hide();

//             // Thêm các phần tử vào thanh công cụ
//             this.$buttons.prepend($clearButton);
//             this.$buttons.prepend($applyButton);
//             this.$buttons.prepend($hideDateCheckbox);
//             this.$buttons.prepend($hideColorCheckbox);

//             // Gắn sự kiện cho các checkbox
//             this.$buttons.find("input[type='checkbox']").on("change", this._onCheckboxChange.bind(this));
//         },

//         // Xử lý sự kiện khi nút "Click Me" được nhấn
//         _onButtonClick: function () {
//             this.do_notify(
//                 _t("'Inventory Overview' added to dashboard"),
//                 _t("Please refresh your browser for the changes to take effect")
//             );
//         },

//         // Xử lý sự kiện khi checkbox thay đổi
//         _onCheckboxChange: function () {
//             var hideColorChecked = this.$buttons.find("#hide_color").prop("checked");
//             var hideDateChecked = this.$buttons.find("#hide_date").prop("checked");

//             // Hiện nút Apply và Clear nếu có ít nhất một checkbox được chọn
//             this.$buttons.find(".apply-btn").toggle(hideColorChecked || hideDateChecked);
//             this.$buttons.find(".clear-btn").toggle(hideColorChecked || hideDateChecked);
//         },

//         // Xử lý sự kiện khi nhấn nút Apply
//         _onApplyClick: function () {
//             var hideColorChecked = this.$buttons.find("#hide_color").prop("checked");
//             var hideDateChecked = this.$buttons.find("#hide_date").prop("checked");

//             // Ẩn các cột tương ứng
//             if (hideColorChecked) {
//                 this.hideField("color");
//             }
//             if (hideDateChecked) {
//                 this.hideField("date");
//             }
//         },

//         // Xử lý sự kiện khi nhấn nút Clear
//         _onClearClick: function () {
//             // Hiện lại tất cả các cột
//             this.showField("color");
//             this.showField("date");

//             // Bỏ chọn tất cả checkbox và ẩn các nút Apply và Clear
//             this.$buttons.find("input[type='checkbox']").prop("checked", false);
//             this.$buttons.find(".apply-btn").hide();
//             this.$buttons.find(".clear-btn").hide();
//         },

//         // Hàm ẩn cột
//         hideField: function (fieldName) {
//             this.renderer.arch.children.forEach((child) => {
//                 if (child.tag === "field" && child.attrs.name === fieldName) {
//                     child.attrs.modifiers = Object.assign({}, child.attrs.modifiers, {
//                         column_invisible: true,
//                     });
//                 }

//                 if (child.tag === "label" && child.attrs.for === fieldName) {
//                     child.attrs.modifiers = Object.assign({}, child.attrs.modifiers, {
//                         column_invisible: true,
//                     });
//                 }
//             });
//             this.reload();
//         },

//         // Hàm hiện cột
//         showField: function (fieldName) {
//             this.renderer.arch.children.forEach((child) => {
//                 if (child.tag === "field" && child.attrs.name === fieldName) {
//                     if (child.attrs.modifiers && child.attrs.modifiers.column_invisible) {
//                         delete child.attrs.modifiers.column_invisible;
//                     }
//                 }

//                 if (child.tag === "label" && child.attrs.for === fieldName) {
//                     if (child.attrs.modifiers && child.attrs.modifiers.column_invisible) {
//                         delete child.attrs.modifiers.column_invisible;
//                     }
//                 }
//             });
//             this.reload();
//         },
//     });

//     // Định nghĩa một List View mới sử dụng controller kết hợp
//     var CombinedWidgetListView = ListView.extend({
//         config: _.extend({}, ListView.prototype.config, {
//             Controller: CombinedWidgetController,
//         }),
//     });

//     // Đăng ký view này vào hệ thống Odoo
//     viewRegistry.add("combined_widget", CombinedWidgetListView);
// });
odoo.define("combined_widget", function (require) {
    "use strict";

    var ListController = require("web.ListController");
    var ListView = require("web.ListView");
    var viewRegistry = require("web.view_registry");
    var core = require("web.core");
    var _t = core._t;

    // Kế thừa ListController từ cả hai widget
    var CombinedWidgetController = ListController.extend({
        // Hàm render lại các nút
        renderButtons: function ($node) {
            // Gọi hàm renderButtons mặc định của cả hai lớp
            this._super.apply(this, arguments);

            if (this.$buttons) {
                // Thêm nút "Click Me"
                var $button = $("<button>", {
                    type: "button",
                    class: "btn btn-primary",
                    text: _t("Click Me"),
                }).on("click", this._onButtonClick.bind(this));

                this.$buttons.prepend($button);

                // Thêm checkbox "Hide Color" và "Hide Date"
                var $hideColorCheckbox = $("<label>", { class: "checkbox-inline" }).append(
                    $("<input>", { type: "checkbox", id: "hide_color" }),
                    _t(" Hide Color")
                );

                var $hideDateCheckbox = $("<label>", { class: "checkbox-inline" }).append(
                    $("<input>", { type: "checkbox", id: "hide_date" }),
                    _t(" Hide Date")
                );

                // Tạo nút Apply
                var $applyButton = $("<button>", {
                    type: "button",
                    class: "btn btn-success apply-btn",
                    text: _t("Apply"),
                }).on("click", this._onApplyClick.bind(this)).hide();

                // Tạo nút Clear
                var $clearButton = $("<button>", {
                    type: "button",
                    class: "btn btn-danger clear-btn",
                    text: _t("Clear"),
                }).on("click", this._onClearClick.bind(this)).hide();

                // Thêm các phần tử vào thanh công cụ
                this.$buttons.prepend($clearButton);
                this.$buttons.prepend($applyButton);
                this.$buttons.prepend($hideDateCheckbox);
                this.$buttons.prepend($hideColorCheckbox);

                // Gắn sự kiện cho các checkbox
                this.$buttons.find("input[type='checkbox']").on("change", this._onCheckboxChange.bind(this));
            }
        },

        // Xử lý sự kiện khi nút "Click Me" được nhấn
        _onButtonClick: function () {
            this.do_notify(
                _t("'Inventory Overview' added to dashboard"),
                _t("Please refresh your browser for the changes to take effect")
            );
        },

        // Xử lý sự kiện khi checkbox thay đổi
        _onCheckboxChange: function () {
            var hideColorChecked = this.$buttons.find("#hide_color").prop("checked");
            var hideDateChecked = this.$buttons.find("#hide_date").prop("checked");

            // Hiện nút Apply và Clear nếu có ít nhất một checkbox được chọn
            this.$buttons.find(".apply-btn").toggle(hideColorChecked || hideDateChecked);
            this.$buttons.find(".clear-btn").toggle(hideColorChecked || hideDateChecked);

            // Disable checkbox đã được chọn
            if (hideColorChecked) {
                this.$buttons.find("#hide_color").prop("disabled", true);
            }
            if (hideDateChecked) {
                this.$buttons.find("#hide_date").prop("disabled", true);
            }
        },

        // Xử lý sự kiện khi nhấn nút Apply
        _onApplyClick: function () {
            var hideColorChecked = this.$buttons.find("#hide_color").prop("checked");
            var hideDateChecked = this.$buttons.find("#hide_date").prop("checked");

            // Ẩn các cột tương ứng
            if (hideColorChecked) {
                this.hideField("color");
            }
            if (hideDateChecked) {
                this.hideField("date");
            }
        },

        // Xử lý sự kiện khi nhấn nút Clear
        _onClearClick: function () {
            // Hiện lại tất cả các cột
            this.showField("color");
            this.showField("date");

            // Bỏ chọn tất cả checkbox và enable lại
            this.$buttons.find("input[type='checkbox']")
                .prop("checked", false)
                .prop("disabled", false);

            // Ẩn các nút Apply và Clear
            this.$buttons.find(".apply-btn").hide();
            this.$buttons.find(".clear-btn").hide();
        },

        // Hàm ẩn cột
        hideField: function (fieldName) {
            this.renderer.arch.children.forEach((child) => {
                if (child.tag === "field" && child.attrs.name === fieldName) {
                    child.attrs.modifiers = Object.assign({}, child.attrs.modifiers, {
                        column_invisible: true,
                    });
                }

                if (child.tag === "label" && child.attrs.for === fieldName) {
                    child.attrs.modifiers = Object.assign({}, child.attrs.modifiers, {
                        column_invisible: true,
                    });
                }
            });
            this.reload();
        },

        // Hàm hiện cột
        showField: function (fieldName) {
            this.renderer.arch.children.forEach((child) => {
                if (child.tag === "field" && child.attrs.name === fieldName) {
                    if (child.attrs.modifiers && child.attrs.modifiers.column_invisible) {
                        delete child.attrs.modifiers.column_invisible;
                    }
                }

                if (child.tag === "label" && child.attrs.for === fieldName) {
                    if (child.attrs.modifiers && child.attrs.modifiers.column_invisible) {
                        delete child.attrs.modifiers.column_invisible;
                    }
                }
            });
            this.reload();
        },
    });

    // Định nghĩa một List View mới sử dụng controller kết hợp
    var CombinedWidgetListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: CombinedWidgetController,
        }),
    });

    // Đăng ký view này vào hệ thống Odoo
    viewRegistry.add("combined_widget", CombinedWidgetListView);
});
