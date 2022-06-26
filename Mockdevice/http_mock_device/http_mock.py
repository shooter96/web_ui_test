import hashlib
import struct
import requests
import time, random
import json
from threading import Thread
from Mockdevice.http_mock_device import http_config as hc
import inspect
import ctypes

timestamp = int(time.time() * 1000)


class HttpMock():
    def __init__(self):
        self.host = hc.host
        self.port = hc.port
        self.secret = hc.secret
        self.pk = hc.pk
        self.dev_id = hc.dev_id
        self.up = self.host + '/up/dev'
        self.stop = False

    def get_token(self):
        headers = {'Content-Type': 'application/json'}
        plaintext = self.pk + '&' + self.secret + '&' + self.dev_id + '&' + str(timestamp)
        sign = hashlib.sha256(plaintext.encode('utf-8')).hexdigest()
        data = {'devId': self.dev_id, 'timestamp': timestamp, "sign": sign}
        url = self.host + '/device/auth'
        response = requests.post(url, json=data, headers=headers)
        try:
            response = response.json()
            token = response.get('data').get('token')
            return token
        except:
            return

    def push_data_to_topic(self, tag=1):
        """
        :param dev_id:
        :param pk:
        :param secret:
        :param tag: 协议类型  私有和ilink,默认1为官方
        :return:
        """
        n = 0
        # token = get_token(dev_id, pk, secret)
        # headers = {'Content-Type': 'application/json', 'X-Isyscore-Iot-Token': token}
        # headers1 = {'X-Isyscore-Iot-Token': token}
        if tag != 1:
            while not self.stop:
                token = self.get_token()
                headers1 = {'X-Isyscore-Iot-Token': token}
                timestamp = int(time.time() * 1000)
                n = n + 10
                if n > 99:
                    n = 0
                if n < 30:
                    data = self.get_struct_event(timestamp)
                else:
                    data = self.get_struct_list(timestamp, n, random.randint(0, 100))
                byte_array = bytearray()
                for i in data:
                    byte_array.append(i)
                time.sleep(2)
                # 私有协议需要传字节数组过去
                print('头部信息{}'.format(headers1))
                print('参数{}'.format(byte_array))
                re = requests.post(self.up, data=byte_array, headers=headers1)
                try:
                    json_data = re.json()
                    print('接口响应{}'.format(json_data))
                except:
                    pass
        else:
            while not self.stop:
                token = self.get_token()
                headers = {'Content-Type': 'application/json', 'X-Isyscore-Iot-Token': token}
                timestamp = int(time.time() * 1000)
                raw_data = {
                    "operate": "ATTR_UP",
                    "operateId": 1,
                    "data": [{
                        "pk": self.pk,
                        "devId": self.dev_id,
                        "time": timestamp,
                        "params": {'temperature': n, 'humidity': random.randint(0, 100)}}]
                }
                lowPower_data = {
                    "operate": "EVENT_UP",
                    "operateId": 1,
                    "data": [{
                        "pk": self.pk,
                        "devId": self.dev_id,
                        "identifier": "lowPower",
                        "time": timestamp,
                        "params": {'temperature': n, 'humidity': random.randint(0, 100)}}]
                }
                n = n + 10
                if n > 99:
                    n = 0
                if n < 30:
                    data = lowPower_data
                else:
                    data = raw_data
                time.sleep(2)
                print('头部信息{}'.format(headers))
                print('参数{}'.format(data))
                re = requests.post(self.up, data=json.dumps(data), headers=headers)
                try:
                    json_data = re.json()
                    print(json_data)
                except:
                    pass

    # 私有协议--- 属性上报
    def get_struct_list(self, timestamp, temperature, humidity):
        mesage_id = timestamp
        type1 = b'0x01'
        bytestr = struct.pack('>q', mesage_id)
        bytestr2 = struct.pack('>q ', timestamp)
        bytestr3 = struct.pack('>b', temperature)
        bytestr4 = struct.pack('>b', humidity)
        result = list(bytestr) + list(bytestr2) + [int(type1, 16)] + list(bytestr3) + list(bytestr4)
        return result

    # 私有协议--- 事件上报
    def get_struct_event(self, timestamp):
        mesage_id = timestamp
        type1 = b'0x02'
        event_data = 'lowPower'.encode()
        bytes_list = []
        for i in bytearray(event_data):
            bytes_list.append(i)
        bytestr = struct.pack('>q', mesage_id)
        bytestr2 = struct.pack('>q ', timestamp)
        result = list(bytestr) + list(bytestr2) + [int(type1, 16)] + bytes_list
        return result

    def do_mock(self, tag=1):
        self.t1 = Thread(target=self.push_data_to_topic, args=(tag,))
        self.t2 = Thread(target=self.push_data_to_topic, args=(tag,))
        self.t1.start()

    def stop_mock(self):
        try:
            self.stop = True
            self.stop_thread(self.t1)
            self.stop_thread(self.t2)
        except:
            pass

    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)


if __name__ == '__main__':
    from threading import Thread

    Hm = HttpMock()
    Hm.do_mock()
    # 多个设备调用函数多次就行，只需要修改dev_id,pk,secret
    # pk1 = "C2TZSDyY1Aw"
    # dev_id1 = "http_private_001"
    # secret1 = "LYl1qRWSzEAkI7ME"
    # tag2 = 2
    # t2 = Thread(target=push_data_to_topic, args=(dev_id1, pk1, secret1, tag2))
    # t2.start()
    time.sleep(3)
    Hm.stop_mock()
    # Hm.stop_mock()
