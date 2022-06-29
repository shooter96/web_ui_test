import time

from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from Mockdevice.http_mock_device.http_mock import HttpMock
from TestDatas import Common_Datas as CD
from TestDatas import device_datas as dd
from PageObjects.login_page import LoginPage
from PageObjects.desktop_page import DeskTopPAge
from PageObjects.product_page import ProductPage
from PageObjects.device_page import DevicePage


class TestCoAPDevice:
    def setup_class(self):
        self.driver = webdriver.Chrome()
        # 打开登录页面
        self.driver.get(CD.base_url)
        self.driver.maximize_window()

        # 登录
        LoginPage(self.driver).login(CD.user, CD.password)

        # 进入设备集成应用
        DeskTopPAge(self.driver).into_dmc_application()
        self.driver.refresh()
        # 模拟器对象
        self.mock = HttpMock()
        self.device_page = DevicePage(self.driver)

    def teardown_class(self):
        self.driver.quit()
        self.mock.stop_mock()

    def test_add_http_product(self):
        '''
        新增设备类和设备模型
        :return:
        '''
        self.driver.implicitly_wait(5)
        # 进入iframe
        self.device_page.switch_into_iframe()

        # 新增设备类
        product_page = ProductPage(self.driver)
        http_product_data = dd.http_product_data
        product_page.add_direct_product(http_product_data["ProductName"], http_product_data["pk"],
                                        http_product_data["communication_type"])
        time.sleep(1)

        # 新增设备模型
        product_page.add_tsl(identifier=dd.wsd_tsl_data[0]["identifier"], name=dd.wsd_tsl_data[0]["name"])
        result = product_page.add_device_model()
        assert result

    def test_add_direct_coap_device(self):
        # 点击设备类的设备管理进行设备新增

        device_data = dd.http_direct_device_data
        devName = device_data["devName"]
        dev_id = self.device_page.add_device(device_data["devId"], devName,
                                             device_data["secret"])
        online_status = self.device_page.get_device_online_status(devName)

        assert dev_id == device_data["devId"]
        assert online_status == "-"

    def test_device_online(self):
        try:
            # 进入详情页面
            self.device_page.device_to_device_detail()
            # 启动模拟器
            self.mock.do_mock()
            time.sleep(8)
            # 查看设备状态
            assert self.device_page.get_device_detail_status("HTTP") == "激活"
        except KeyboardInterrupt:
            print("quitting: KeyboardInterrupt")

    def test_device_read(self):

        self.device_page.switch_to_function_tab()
        real_value = self.device_page.get_device_value()
        assert int(real_value) in range(0, 110, 10)

    # def test_device_write(self):
    #     self.device_page.write_device_value(dd.device_write_attribute["data"])
    #     real_value = self.device_page.get_device_value()
    #
    #     assert int(real_value) in range(0, 50, 10)

    def test_delete_data(self):
        # self.device_page.switch_to_device_menu()
        # # 删除设备
        # self.device_page.delete_data()
        self.driver.find_element(By.XPATH, '//li[text()=" 设备 " ]').click()

        # 删除设备
        delete_ele = self.driver.find_element(By.XPATH, '//a//span[text()=" 删除 "]')
        delete_ele.click()
        self.driver.implicitly_wait(1)
        self.driver.find_elements(By.XPATH, '//div[@class="isc-message-box__btns"]//button')[0].click()
        # 删除设备类
        # self.device_page.switch_to_product_menu()
        # self.device_page.delete_data()
        self.driver.find_element(By.XPATH, '//li[text()=" 设备类 " ]').click()
        # 根据设备类PK查询
        self.driver.find_element(By.XPATH, '//div[@class="isc-input-group__prepend"]').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//span[text()="设备类Key"]').click()
        time.sleep(1)
        select_input = self.driver.find_element(By.XPATH, '//input[@placeholder="请输入"]')
        select_input.send_keys(dd.http_product_data["pk"])
        select_input.send_keys(Keys.ENTER)
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//a//span[text()=" 删除 "]').click()
        time.sleep(1)
        self.driver.find_elements(By.XPATH, '//div[@class="isc-message-box__btns"]//button')[0].click()


if __name__ == '__main__':
    pass
    # pytest.main(['-s', 'test_direct_mqtt.py::TestLogin::test_delete_data'])
