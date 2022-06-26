# @author: wy
# @project:web_ui_test
from selenium.webdriver.common.by import By

from Common.basepage import BasePage
from PageLocators.device_manage_loc import DeviceManagePageLoc as DML
import time


class ProductPage(BasePage):
    def add_direct_product(self, name, pk, communication_type="MQTT"):
        # 进入设备类模块
        self.click_element(DML.device_manage_menu_loc, "menu点击设备管理模块")
        self.click_element(DML.product_menu_loc, "menu点击设备类模块")
        # 新增设备类
        self.click_element(DML.add_product_button_loc, "点击新增设备类按钮")
        self.input_text(DML.product_name_loc, name, "输入设备类名称")
        self.clear_content(DML.pk_input_loc, "清空默认生成的pk")
        self.input_text(DML.pk_input_loc, pk, "输入设备类的pk")
        self.click_element(DML.device_type_loc, "选择设备类类型为直连设备")
        if communication_type == "CoAP":
            self.click_element(DML.coap_commuincation_radio, "选择通讯协议为coap")

        elif communication_type == "HTTP":
            self.click_element(DML.http_commuincation_radio, "选择通讯协议为http")
        time.sleep(1)
        self.click_element(DML.product_confirm_button_loc, "点击确认按钮，提交设备类信息")

    def add_tsl(self, identifier=None, name=None, pk=None, min_start=0, max_end=999999):
        ''''
        新增TSL
        pk:为True则从左侧导航栏重新进入设备类列表,根据pk查找设备类进行tsl的心中那个；
        False则在当前页面找元素
        '''
        if not pk:
            self.click_element(DML.tsl_config_button_loc, "点击定义物模型，跳转至tsl定义页面")
            time.sleep(1)
        else:
            pass
        self.click_element(DML.edit_tsl_button_loc, "进入tsl编辑模式")
        self.click_element(DML.add_tsl_button_loc, "点击「自定义功能」按钮")
        self.input_text(DML.tsl_identifier_input_loc, identifier, "输入功能的标识符")
        self.input_text(DML.tsl_name_input_loc, name, "输入功能的名称")
        self.click_element(DML.tsl_datatype_select_loc, "点击展开下拉框数据类型")
        self.click_element(DML.tsl_select_type_double_loc, "选择数据类型为-double")
        self.input_text(DML.tsl_min_value_loc, min_start, "输入最小值")
        self.input_text(DML.tsl_max_value_loc, max_end, "输入最大值")
        self.input_text(DML.tsl_step_loc, 0, "设置步长为0")
        self.click_element(DML.tsl_accessMode_loc, "选择读写类型")
        # self.click_element(DML.tsl_confirm_button_loc, "点击确定按钮")
        self.driver.find_elements(By.XPATH, '//footer[@class="isc-drawer__footer"]//span[text()="确定"]')[1].click()

    def add_device_model(self):
        try:
            self.click_element(DML.save_and_publish_model_button_loc, "点击保存并发布按钮")
            self.click_element(DML.confirm_model_button_loc, "点击确认按钮，新增设备模型")
            time.sleep(3)
            return 1
        except Exception:
            return 0

    def edit_direct_mqtt_product(self, name, pk):
        # 进入设备类模块
        # 编辑设备类
        # 编辑TSL
        pass
