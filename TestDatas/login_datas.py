# 成功用例 - 数据
success_data = {"user": "admin", "passwd": "1Sysc0re!"}

# 用户名为空/密码为空/用户名格式不正确
wrong_datas = [
    {"user": "", "passwd": "python", "check": "请输入手机号"},
    {"user": "18684720553", "passwd": "", "check": "请输入密码"},
    {"user": "186847205", "passwd": "python", "check": "请输入正确的手机号"}
]

# 密码错误 / 用户名尚未注册
