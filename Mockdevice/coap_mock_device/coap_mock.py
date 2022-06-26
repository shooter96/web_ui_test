import hashlib
import json
import random
import sys
import time
from threading import Thread
from coapthon import defines
from coapthon.client.helperclient import HelperClient
from coapthon.messages.request import Request
from queue import Queue
from Mockdevice.coap_mock_device import coap_config as cc
import inspect
import ctypes



class CoapMock():

    def __init__(self):
        self.step = 10
        self.q = Queue()
        self.qq = Queue()
        self.host = cc.host
        self.port = cc.port
        self.secret = cc.secret
        self.pk = cc.pk
        self.dev_id = cc.dev_id
        self.user = self.pk + '@' + self.dev_id
        self.passwd = self.pk + self.dev_id + self.secret
        self.password = hashlib.sha256(self.passwd.encode('utf-8')).hexdigest()
        self.client_id = self.pk + '@' + self.dev_id
        self.up = '/mqtt/up/dev/{}/{}?c={}&u={}&p={}'.format(self.pk, self.dev_id, self.client_id, self.user,
                                                             self.password)
        self.down = '/mqtt/down/dev/{}/{}?c={}&u={}&p={}'.format(self.pk, self.dev_id, self.client_id, self.user,
                                                                 self.password)
        self.stop = False

    # 上报
    def push_data(self):
        client = HelperClient(server=(self.host, self.port))
        n = 0
        # params = ''
        while not self.stop:
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

            lowPower_data = {"operate": "EVENT_UP", "operateId": 1509045769326297088, "data": [
                {"pk": self.pk, "devId": self.dev_id, "identifier": "lowPower", "time": timestamp, "params": {}}]}
            n = n + self.step
            if n > 99:
                n = 0
            if n < 30:
                # lowPower_data.get('data')[0].get('params').update(params)
                data = lowPower_data
            else:
                # raw_data.get('data')[0].get('params').update(params)
                data = raw_data
            print('上报数据为{}'.format(data))
            # data = json.dumps(raw_data, ensure_ascii=False, sort_keys=False)
            data = json.dumps(data, ensure_ascii=False, sort_keys=False)
            response = client.put(self.up, data, timeout=3)
            time.sleep(1)

    # 订阅
    def subscribe_data(self):
        client = HelperClient(server=(self.host, self.port))
        request = Request()
        request.code = defines.Codes.GET.number
        request.type = defines.Types['NON']
        request.destination = (self.host, self.port)
        request.uri_path = self.down
        request.observe = 0
        request.content_type = defines.Content_types["application/json"]
        # request.payload = '<value>"+str(payload)+"</value>'
        while not self.stop:
            response = client.send_request(request)
            data = response.payload
            if data:
                json_data = json.loads(data.decode())
                a = json_data.copy()
                self.qq.put(a)
                self.q.put(json_data)

    # 上报温度属性回应
    def attr_write_res(self):
        client = HelperClient(server=(self.host, self.port))
        while not self.stop:
            json_data = get_que_data(self.q)
            timestamp = int(time.time() * 1000)
            try:
                if json_data.get('data').get('params').get('temperature') < 100:
                    temperature = json_data.get('data').get('params').get('temperature') + 10
                else:
                    temperature = 0
            except:
                pass
            else:
                if temperature:
                    data = {
                        "operate": "ATTR_WRITE_RES",
                        "operateId": 1,
                        "data": {
                            "pk": self.pk,
                            "devId": self.dev_id,
                            "time": timestamp,
                            "params": {
                                "temperature": "{}".format(temperature),
                            }
                        },
                        "code": 0
                    }
                    data = json.dumps(data, ensure_ascii=False, sort_keys=False)
                    response = client.put(self.up, data)

    def do_mock(self):
        self.t1 = Thread(target=self.attr_write_res)
        self.t2 = Thread(target=self.push_data)
        self.t3 = Thread(target=self.subscribe_data)
        self.t1.start()
        self.t2.start()
        # self.t3.start()

    def stop_mock(self):
        try:
            self.stop = True
            self.stop_thread(self.t1)
            self.stop_thread(self.t2)
            self.stop_thread(self.t3)
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


def get_que_data(que: Queue):
    try:
        time.sleep(1)
        data = que.get_nowait()
    except:
        pass

    else:
        return data


if __name__ == '__main__':
    cm = CoapMock()
    cm.do_mock()
    time.sleep(10)
    cm.stop_mock()
