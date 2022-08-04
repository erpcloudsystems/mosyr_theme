frappe.views.BaseList.prototype.setup_paging_area = function () {
    const paging_values = [20, 100, 500];
    this.$paging_area = $(
        `<div class="list-paging-area level">
            <div class="level-left">
                <div class="btn-group">
                    ${paging_values.map((value) => `
                        <button type="button" class="btn btn-default btn-sm btn-paging"
                            data-value="${value}">
                            ${value}
                        </button>
                    `).join("")}
                </div>
            </div>
            <div class="level-right">
                <button class="btn btn-default btn-more btn-sm">
                    ${__("Load More")}
                </button>
            </div>
        </div>`
    ).hide();
    this.$frappe_list.append(this.$paging_area);

    // set default paging btn active
    this.$paging_area
        .find(`.btn-paging[data-value="${this.page_length}"]`)
        .addClass("btn-info active-paging");

    this.$paging_area.on("click", ".btn-paging, .btn-more", (e) => {
        const $this = $(e.currentTarget);

        if ($this.is(".btn-paging")) {
            // set active button
            this.$paging_area.find(".btn-paging").removeClass("btn-info active-paging");
            $this.addClass("btn-info active-paging");

            this.start = 0;
            this.page_length = this.selected_page_count = $this.data().value;
        } else if ($this.is(".btn-more")) {
            this.start = this.start + this.page_length;
            this.page_length = this.selected_page_count || 20;
        }
        this.refresh();
    });
}