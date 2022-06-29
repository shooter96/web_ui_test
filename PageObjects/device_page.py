# @author: wy
# @project:web_ui_test
from Common.basepage import BasePage
from selenium.webdriver.common.keys import Keys
from PageLocators.device_manage_loc import DeviceManagePageLoc as DML
import time
from Common.JS import addAttribute


class DevicePage(BasePage):
    def switch_into_iframe(self):
        iframe_element = self.get_element(DML.iframe_element,"查找iframe元素")
        addAttribute(self.driver, iframe_element, 'name', 'auto_into_iframe')
        time.sleep(1)
        self.driver.switch_to.frame('auto_into_iframe')

    def add_device(self, devId, devName, secret, pk=None, groupName="默认分组"):
        self.click_element(DML.product_menu_loc, "进入设备类模块")
        time.sleep(1)
        self.click_element(DML.product_manage_device, "点击管理设备")
        self.click_element(DML.add_device_button, "点击新增按钮")
        self.input_text(DML.device_name_input, devName, "输入设备名称")
        self.input_text(DML.device_id_input, devId, "输入设备Id")
        self.clear_content(DML.device_secret_input, "清空密钥")
        self.input_text(DML.device_secret_input, secret, "输入密钥")
        time.sleep(3)
        self.click_element(DML.device_add_confirm_button, "点击确认按钮提交表单")
        self.click_element(DML.return_device_list, "返回设备列表")
        self.input_text(DML.select_by_name, devName, "根据设备名称查询")
        self.input_text(DML.select_by_name, Keys.ENTER, "控制键盘，回车查询")
        device_name = self.get_element_text(DML.device_id_text, "获取设备Id")
        return device_name

    def get_device_online_status(self, devName):
        # 获取设备在设备列表展示的在线状态#
        # self.input_text(DML.select_by_name, devName, "根据设备名称查询")
        # self.input_text(DML.select_by_name, Keys.ENTER, "控制键盘，回车查询")
        online_status = self.get_element_text(DML.device_online_status, "获取设备在线状态")
        return online_status

    def device_to_device_detail(self):
        self.click_element(DML.device_check_label, "点击查看进入设备详情页")

    def get_device_detail_status(self, device_type):
        status_loc = None
        if device_type == "MQTT":
            status_loc = DML.mqtt_device_detail_status_loc
        elif device_type == "CoAP":
            status_loc = DML.coap_device_detail_status_loc
        elif device_type == "HTTP":
            status_loc = DML.http_device_detail_status_loc
        device_status = self.get_element_text(status_loc, "获取设备详情页的设备状态")
        return device_status

    def switch_to_function_tab(self):
        self.click_element(DML.device_function_monitor_loc, "进入功能监测tab页")
        time.sleep(1)

    def get_device_value(self):
        # 获取设备实时值
        real_value = self.get_element_text(DML.device_real_value_text_loc, "获取实时值")
        return real_value

    def write_device_value(self, value):
        self.click_element(DML.device_value_write_label_loc, "点击写入标签")
        self.input_text(DML.device_vlaue_write_input_loc, value, "写属性")
        self.click_element(DML.device_value_write_confirm_loc, "点击确认")
        time.sleep(5)

    def switch_to_device_menu(self):
        self.click_element(DML.device_menu_loc, "进入设备管理-设备模块")

    def switch_to_product_menu(self):
        self.click_element(DML.product_menu_loc, "进入设备管理-设备类模块")

    def delete_data(self):
        self.click_element(DML.delete_label, '点击删除标签')
        self.click_element(DML.delete_confirm_button, "点击确认按钮")
