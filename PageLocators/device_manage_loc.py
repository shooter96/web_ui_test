from selenium.webdriver.common.by import By
from TestDatas import device_datas as dd


class DeviceManagePageLoc:
    # 左面应用菜单获取
    desktop_menu_loc = (By.XPATH, '//a[text()="应用"]')
    # 设备管理模块相关元素
    iframe_element = (By.XPATH, '//iframe')
    device_manage_menu_loc = (By.XPATH, '//span[text()="设备管理"]')

    # ---------------设备类最外层-------------------
    product_menu_loc = (By.XPATH, '//li[text()=" 设备类 " ]')
    add_product_button_loc = (By.XPATH, '//button//span[text()="新增设备类"]')
    # 新增/编辑页面，设备类名称文本框
    product_name_loc = (By.XPATH, '//input[@placeholder="请输入设备类名称"]')
    # 新增/编辑页面，pk文本框
    pk_input_loc = (By.XPATH, '//input[@id="productKeyInput"]')
    # 设备类型-直连设备
    device_type_loc = (By.XPATH, '//div[@class="isc-form-item__content"]//span[text()=" 直连设备 "]')
    # 通讯协议
    coap_commuincation_radio = (By.XPATH, '//label[@ id="communicationTypeRadioCOAP"]')
    http_commuincation_radio = (By.XPATH, '//label[@ id="communicationTypeRadioHTTP"]')

    # 提交设备类，确认按钮
    product_confirm_button_loc = (By.XPATH, '//button//span[text()=" 确认 "]')
    change_select_condition_loc = (By.XPATH, '//div[@class="isc-input-group__prepend"]')
    select_condition_pk_loc = (By.XPATH, '//span[text()="设备类Key"]')
    product_select_condition_input_loc = (By.XPATH, '//input[@placeholder="请输入"]')
    # 设备类新增后，跳转至新页面（流程提示页面）
    tsl_config_button_loc = (By.XPATH, '//span[text()="定义物模型"]')

    # ------------------------功能定义页面-----------------------------
    edit_tsl_button_loc = (By.XPATH, '//button//span[text()="编辑功能"]')
    add_tsl_button_loc = (By.XPATH, '//button//span[text()="自定义功能"]')
    tsl_identifier_input_loc = (By.XPATH, '//form//div[2]//input[@placeholder="请输入"]')
    tsl_name_input_loc = (By.XPATH, '//form//div[3]//input[@placeholder="请输入"]')
    tsl_datatype_select_loc = (By.XPATH, '//form//div[4]//input[@placeholder="请选择"]')
    tsl_select_type_double_loc = (By.XPATH, '//span[text()="double(双精度浮点型)"]')
    tsl_min_value_loc = (By.XPATH, '//input[@id="numberRangeInputMin"]')
    tsl_max_value_loc = (By.XPATH, '//input[@id="numberRangeInputMax"]')
    tsl_step_loc = (By.XPATH, '//div[@id="numberStepInpu"]//input')
    tsl_accessMode_loc = (By.XPATH, '//div[@id="accessModeRadioGroup"]//span[text()="读写"]')
    tsl_confirm_button_loc = (By.XPATH, '//span[text()="确定"]')
    save_and_publish_model_button_loc = (By.XPATH, '//button//span[text()="保存并发布"]')
    confirm_model_button_loc = (By.XPATH, '//div[@class="isc-dialog__footer"]//span[text()=" 确认 "]')

    # --------------------------设备最外层----------------------------
    # 设备列表页
    device_menu_loc = (By.XPATH, '//li[text()=" 设备 " ]')
    product_manage_device = (By.XPATH, '//tbody//td[8]//span[text()=" 管理设备 "]')
    add_device_button = (By.XPATH, '//span[text()="新增设备"]')
    select_by_name = (By.XPATH, '//input[@placeholder="请输入"]')
    device_online_status = (By.XPATH, '//tr/td[7]')
    device_id_text = (By.XPATH, '//tr/td[3]')
    device_check_label = (By.XPATH, '//span[text()=" 查看 "]')

    # 新增设备页面
    device_id_input = (By.XPATH, '//input[@placeholder="请输入设备 ID"]')
    device_name_input = (By.XPATH, '//input[@placeholder="请输入设备名称"]')
    device_secret_input = (By.XPATH, '//input[@placeholder="设备密钥"]')
    device_add_confirm_button = (By.XPATH, '//span[text()=" 确认 "]')

    # 流程页
    return_device_list = (By.XPATH, '//span[text()="返回设备列表"]')
    # -------------------------设备详情页-------------------------------
    mqtt_device_detail_status_loc = (
        By.XPATH, '//span[text()=" {} "]/../div'.format(dd.mqtt_direct_device_data["devName"]))
    http_device_detail_status_loc = (
        By.XPATH, '//span[text()=" {} "]/../div'.format(dd.http_direct_device_data["devName"]))
    coap_device_detail_status_loc = (
        By.XPATH, '//span[text()=" {} "]/../div'.format(dd.coap_direct_device_data["devName"]))
    device_function_monitor_loc = (By.XPATH, '//div[@class="page-header__tabs"]//div[text()="功能监测"]')
    device_real_value_text_loc = (By.XPATH, '//div[@table-row-key="identifier"]//tbody//tr[1]//td[6]//div')
    device_value_write_label_loc = (By.XPATH, '//tbody//tr[1]/td[7]//span[text()=" 写入 "]')
    device_vlaue_write_input_loc = (By.XPATH, '//input[@id="attrNumberWriteInputtemperature"]')
    device_value_write_confirm_loc = (By.XPATH, '//button[@id="attrNumberWriteConfirmtemperature"]')
    # 通用
    delete_label = (By.XPATH, '//a//span[text()=" 删除 "]')
    delete_confirm_button = (By.XPATH, '//div[@class="isc-message-box__btns"]//button')[0]
