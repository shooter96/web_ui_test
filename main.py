from Mockdevice.mqtt_mock_device.device_mock import *
mock = DeviceMock()
mock.do_mock()
time.sleep(3)
mock.stop_mock()
