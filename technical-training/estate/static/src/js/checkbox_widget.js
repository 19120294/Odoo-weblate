// odoo.define("checkbox_widget", function (require) {
//     "use strict";

//     var ListController = require("web.ListController");
//     var ListView = require("web.ListView");
//     var viewRegistry = require("web.view_registry");
//     var core = require("web.core");
//     var _t = core._t;

//     // Tùy chỉnh ListController
//     var CheckboxWidgetController = ListController.extend({
//         renderButtons: function ($node) {
//             this._super.apply(this, arguments);

//             if (this.$buttons) {
//                 // Tạo checkbox "Hide Color"
//                 var $hideColorCheckbox = $("<label>", {
//                     class: "checkbox-inline",
//                 }).append(
//                     $("<input>", { type: "checkbox", id: "hide_color" }),
//                     _t(" Hide Color")
//                 );

//                 // Tạo checkbox "Hide Date"
//                 var $hideDateCheckbox = $("<label>", {
//                     class: "checkbox-inline",
//                 }).append(
//                     $("<input>", { type: "checkbox", id: "hide_date" }),
//                     _t(" Hide Date")
//                 );

//                 // Tạo nút Apply
//                 var $applyButton = $("<button>", {
//                     type: "button",
//                     class: "btn btn-success apply-btn",
//                     text: _t("Apply"),
//                 })
//                     .on("click", this._onApplyClick.bind(this))
//                     .hide();

//                 // Tạo nút Clear
//                 var $clearButton = $("<button>", {
//                     type: "button",
//                     class: "btn btn-danger clear-btn",
//                     text: _t("Clear"),
//                 })
//                     .on("click", this._onClearClick.bind(this))
//                     .hide();

//                 // Thêm các phần tử vào thanh công cụ
//                 this.$buttons.prepend($clearButton);
//                 this.$buttons.prepend($applyButton);
//                 this.$buttons.prepend($hideDateCheckbox);
//                 this.$buttons.prepend($hideColorCheckbox);

//                 // Gắn sự kiện khi checkbox thay đổi
//                 this.$buttons.find("input[type='checkbox']").on(
//                     "change",
//                     this._onCheckboxChange.bind(this)
//                 );
//             }
//         },

//         // Sự kiện khi checkbox thay đổi
//         _onCheckboxChange: function () {
//             var hideColorChecked = this.$buttons
//                 .find("#hide_color")
//                 .prop("checked");
//             var hideDateChecked = this.$buttons
//                 .find("#hide_date")
//                 .prop("checked");

//             // Hiện nút Apply nếu có ít nhất 1 checkbox được chọn
//             this.$buttons.find(".apply-btn").toggle(hideColorChecked || hideDateChecked);

//             // Hiện nút Clear nếu có checkbox được tick
//             this.$buttons.find(".clear-btn").toggle(hideColorChecked || hideDateChecked);
//         },

//         // Sự kiện khi nhấn Apply
//         _onApplyClick: function () {
//             var hideColorChecked = this.$buttons
//                 .find("#hide_color")
//                 .prop("checked");
//             var hideDateChecked = this.$buttons
//                 .find("#hide_date")
//                 .prop("checked");

//             // Ẩn các cột tương ứng
//             if (hideColorChecked) {
//                 this.hideField("color");
//             }
//             if (hideDateChecked) {
//                 this.hideField("date");
//             }
//         },

//         // Sự kiện khi nhấn Clear
//         _onClearClick: function () {
//             // Hiện lại tất cả các cột
//             this.showField("color");
//             this.showField("date");

//             // Bỏ chọn tất cả checkbox
//             this.$buttons.find("input[type='checkbox']").prop("checked", false);

//             // Ẩn nút Apply và Clear
//             this.$buttons.find(".apply-btn").hide();
//             this.$buttons.find(".clear-btn").hide();
//         },

//         // Hàm ẩn cột (bao gồm cả tiêu đề cột và dữ liệu)
//         hideField: function (fieldName) {
//             this.renderer.arch.children.forEach((child) => {
//                 // Ẩn dữ liệu (field)
//                 if (child.tag === "field" && child.attrs.name === fieldName) {
//                     child.attrs.modifiers = Object.assign({}, child.attrs.modifiers, {
//                         column_invisible: true,
//                     });
//                 }

//                 // Ẩn tiêu đề cột (label) bằng cách sử dụng column_invisible
//                 if (child.tag === "label" && child.attrs.for === fieldName) {
//                     child.attrs.modifiers = Object.assign({}, child.attrs.modifiers, {
//                         column_invisible: true,
//                     });
//                 }
//             });
//             this.reload();
//         },

//         // Hàm hiện cột (bao gồm cả tên cột và dữ liệu)
//         showField: function (fieldName) {
//             this.renderer.arch.children.forEach((child) => {
//                 // Hiện dữ liệu (field)
//                 if (child.tag === "field" && child.attrs.name === fieldName) {
//                     if (child.attrs.modifiers && child.attrs.modifiers.column_invisible) {
//                         delete child.attrs.modifiers.column_invisible;
//                     }
//                 }

//                 // Hiện tiêu đề cột (label)
//                 if (child.tag === "label" && child.attrs.for === fieldName) {
//                     if (child.attrs.modifiers && child.attrs.modifiers.column_invisible) {
//                         delete child.attrs.modifiers.column_invisible;
//                     }
//                 }
//             });
//             this.reload();
//         },
//     });

//     // Tùy chỉnh ListView
//     var CheckboxWidgetListView = ListView.extend({
//         config: _.extend({}, ListView.prototype.config, {
//             Controller: CheckboxWidgetController,
//         }),
//     });

//     // Đăng ký view
//     viewRegistry.add("checkbox_widget", CheckboxWidgetListView);
// });

odoo.define("checkbox_widget", function (require) {
    "use strict";

    var ListController = require("web.ListController");
    var ListView = require("web.ListView");
    var viewRegistry = require("web.view_registry");
    var core = require("web.core");
    var _t = core._t;

    var CheckboxWidgetController = ListController.extend({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);

            if (this.$buttons) {
                // Tạo checkbox "Hide Color"
                var $hideColorCheckbox = $("<label>", {
                    class: "checkbox-inline",
                }).append(
                    $("<input>", { type: "checkbox", id: "hide_color" }),
                    _t(" Hide Color")
                );

                // Tạo checkbox "Hide Date"
                var $hideDateCheckbox = $("<label>", {
                    class: "checkbox-inline",
                }).append(
                    $("<input>", { type: "checkbox", id: "hide_date" }),
                    _t(" Hide Date")
                );

                // Tạo nút Apply
                var $applyButton = $("<button>", {
                    type: "button",
                    class: "btn btn-success apply-btn",
                    text: _t("Apply"),
                })
                    .on("click", this._onApplyClick.bind(this))
                    .hide();

                // Tạo nút Clear
                var $clearButton = $("<button>", {
                    type: "button",
                    class: "btn btn-danger clear-btn",
                    text: _t("Clear"),
                })
                    .on("click", this._onClearClick.bind(this))
                    .hide();

                // Thêm các phần tử vào thanh công cụ
                this.$buttons.prepend($clearButton);
                this.$buttons.prepend($applyButton);
                this.$buttons.prepend($hideDateCheckbox);
                this.$buttons.prepend($hideColorCheckbox);

                // Gắn sự kiện khi checkbox thay đổi
                this.$buttons.find("input[type='checkbox']").on(
                    "change",
                    this._onCheckboxChange.bind(this)
                );
            }
        },

        // Sự kiện khi checkbox thay đổi
        _onCheckboxChange: function () {
            var hideColorChecked = this.$buttons
                .find("#hide_color")
                .prop("checked");
            var hideDateChecked = this.$buttons
                .find("#hide_date")
                .prop("checked");

            // Hiện nút Apply nếu có ít nhất 1 checkbox được chọn
            this.$buttons.find(".apply-btn").toggle(hideColorChecked || hideDateChecked);

            // Hiện nút Clear nếu có checkbox được tick
            this.$buttons.find(".clear-btn").toggle(hideColorChecked || hideDateChecked);

            // Disable checkbox đã được tick
            if (hideColorChecked) {
                this.$buttons.find("#hide_color").prop("disabled", true);
            }
            if (hideDateChecked) {
                this.$buttons.find("#hide_date").prop("disabled", true);
            }
        },

        // Sự kiện khi nhấn Apply
        _onApplyClick: function () {
            var hideColorChecked = this.$buttons
                .find("#hide_color")
                .prop("checked");
            var hideDateChecked = this.$buttons
                .find("#hide_date")
                .prop("checked");

            // Ẩn các cột tương ứng
            if (hideColorChecked) {
                this.hideField("color");
            }
            if (hideDateChecked) {
                this.hideField("date");
            }
        },

        // Sự kiện khi nhấn Clear
        _onClearClick: function () {
            // Hiện lại tất cả các cột
            this.showField("color");
            this.showField("date");

            // Bỏ chọn và enable tất cả checkbox
            this.$buttons.find("input[type='checkbox']").prop("checked", false).prop("disabled", false);

            // Ẩn nút Apply và Clear
            this.$buttons.find(".apply-btn").hide();
            this.$buttons.find(".clear-btn").hide();
        },

        // Hàm ẩn cột (bao gồm cả tiêu đề cột và dữ liệu)
        hideField: function (fieldName) {
            this.renderer.arch.children.forEach((child) => {
                // Ẩn dữ liệu (field)
                if (child.tag === "field" && child.attrs.name === fieldName) {
                    child.attrs.modifiers = Object.assign({}, child.attrs.modifiers, {
                        column_invisible: true,
                    });
                }

                // Ẩn tiêu đề cột (label) bằng cách sử dụng column_invisible
                if (child.tag === "label" && child.attrs.for === fieldName) {
                    child.attrs.modifiers = Object.assign({}, child.attrs.modifiers, {
                        column_invisible: true,
                    });
                }
            });
            this.reload();
        },

        // Hàm hiện cột (bao gồm cả tên cột và dữ liệu)
        showField: function (fieldName) {
            this.renderer.arch.children.forEach((child) => {
                // Hiện dữ liệu (field)
                if (child.tag === "field" && child.attrs.name === fieldName) {
                    if (child.attrs.modifiers && child.attrs.modifiers.column_invisible) {
                        delete child.attrs.modifiers.column_invisible;
                    }
                }

                // Hiện tiêu đề cột (label)
                if (child.tag === "label" && child.attrs.for === fieldName) {
                    if (child.attrs.modifiers && child.attrs.modifiers.column_invisible) {
                        delete child.attrs.modifiers.column_invisible;
                    }
                }
            });
            this.reload();
        },
    });

    var CheckboxWidgetListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: CheckboxWidgetController,
        }),
    });

    viewRegistry.add("checkbox_widget", CheckboxWidgetListView);
});
