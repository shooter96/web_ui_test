from PageLocators.login_page_loc import LoginPageLoc as loc
from Common.basepage import BasePage


class LoginPage(BasePage):
    # 元素操作 # 登陆操作
    def login(self, username, passwd):
        self.input_text(loc.user_loc, username, "登录页面_登录名输入")
        self.input_text(loc.passwd_loc, passwd, "登录页面_密码输入")
        self.click_element(loc.login_button_loc, "登录页面_点击登录按钮")

    # # 获取提示信息
    # def get_error_msg(self):
    #     return self.get_element_text(loc.form_error_loc, "登陆页面_表单区域错误提示")
    #
    # # 获取页面中的错误提示信息
    # def get_error_msg_from_dialog(self):
    #     return self.get_element_text(loc.dialog_error_loc, "登陆页面_页面中间toast错误提示")
