from selenium.webdriver.common.by import By


class DeskTopLoc:
    # 应用菜单
    menu_entrance_loc = (By.XPATH, '//a[text()="应用"]')
    device_application_loc = (By.XPATH, '//dd[text()=" 设备集成 "]')
