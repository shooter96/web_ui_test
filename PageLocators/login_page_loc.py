from selenium.webdriver.common.by import By

class LoginPageLoc:

    # 登录名输入框
    user_loc = (By.XPATH, '//input[@placeholder="登录名"]')
    # 密码输入框
    passwd_loc = (By.XPATH, '//input[@placeholder="密码"]')
    # 登陆按钮
    login_button_loc = (By.TAG_NAME, "button")