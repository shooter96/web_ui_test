# @author: wy
# @project:web_ui_test
from Common.basepage import BasePage
from PageLocators.desktop_pag_loc import DeskTopLoc as dtl


class DeskTopPAge(BasePage):
    def into_dmc_application(self):
        self.click_element(dtl.menu_entrance_loc, "点击应用")
        self.click_element(dtl.device_application_loc, "点击设备集成")
