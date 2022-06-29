# Copyright (c) 2022, Mai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from mosyr_theme.utils import check_home_workspace


class SystemController(Document):
    def validate(self):
        self.enable = 1
        self.update_home_ws()

    def update_home_ws(self):
        ws = check_home_workspace()
        ws.charts = []
        ws.shortcuts = []
        ws.links = []
        for chart in self.charts:
            ws.append('charts', {
                'chart_name': chart.chart_name,
                'label': chart.label or chart.chart_name
            })

        for shortcut in self.shortcuts:
            ws.append('shortcuts', {
                'type': shortcut.type,
                'link_to': shortcut.link_to,
                'label': shortcut.label or shortcut.link_to,
                'icon': shortcut.icon,
                'color': shortcut.color,
                # 'background': shortcut.background
            })
        ws.is_standard = 0
        ws.save(ignore_permissions=True)
        frappe.db.commit()
