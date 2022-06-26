import struct
from threading import Thread

from paho.mqtt.client import Client
import json
import hashlib
import time
import random
from configparser import ConfigParser
import os
from argparse import ArgumentParser


class DeviceMock:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(__file__), "config.ini")
        self.cfg = ConfigParser()
        self.cfg.read(self.path)
        self.host = self.cfg.get("conf", "host")
        self.port = int(self.cfg.get("conf", "port"))
        self.temperature = int(self.cfg.get("args", "temperature"))
        self.humidity = int(self.cfg.get("args", "humidity"))
        self.step = int(self.cfg.get("args", "step"))
        self.interval = int(self.cfg.get("args", "interval"))
        self.protocol = self.cfg.get("args", "protocol")
        self.pk = self.cfg.get("auth", "pk")
        self.dev_id = self.cfg.get("auth", "dev_id")
        self.secret = self.cfg.get("auth", "secret")
        self.if_reconnect = self.cfg.get("conf", "reconnect")

        self.passwd = self.pk + self.dev_id + self.secret
        self.user = self.pk + '@' + self.dev_id
        self.sha256_passwd = hashlib.sha256(self.passwd.encode('utf-8')).hexdigest()
        self.postfix = self.pk + '/{}'.format(self.dev_id)
        self.down = 'down/dev/' + self.postfix
        self.up = 'up/dev/' + self.postfix
        self.flag = 0
        self.stop = False

    def on_connect(self, client, userdata, flags, rc):
        print('mqtt connected')
        client.subscribe([(self.down, 0)])

    def on_message(self, client, userdata, msg):
        print('收到消息 {}: {}'.format(msg.topic, msg.payload))
        pl = msg.payload
        global temperature
        try:
            data = json.loads(pl)
            operate = data.get('operate')
            if operate == 'ATTR_WRITE':
                if data.get("data").get("params").get("temperature") < 100:
                    self.temperature = data.get("data").get("params").get("temperature") + 10
                else:
                    self.temperature = 0
                # data["data"]["params"]["temperature"] = self.temperature
                data['code'] = 0
                data['operate'] = 'ATTR_WRITE_RES'
                client.publish(self.up, json.dumps(data))

                print('属性下发回应:{}'.format(data))
            if operate == 'SERVICE_DOWN':
                temperature += 2
                data['code'] = 0
                data['operate'] = 'SERVICE_DOWN_RES'
                client.publish(self.up, json.dumps(data))
                print('服务下发回应:{}'.format(data))
        except Exception as e:
            raise e
            # tup, hex_msg = self.byte_to_hex(pl)
            # if tup[2] == 3:
            #     temperature = tup[-1] + 10
            # if tup[2] == 4:
            #     temperature += 2

    def byte_to_hex(self, b):
        if len(b) == 19:
            tup = struct.unpack("!qqbbb", b)
            m_id = '{:016x}'.format(tup[0])
            m_time = m_id
            m_type = '0{}'.format(tup[2])
            m_temp = '{:02x}'.format(tup[3])
            m_hum = '{:02x}'.format(tup[4])
            return tup, m_id + m_time + m_type + m_temp + m_hum
        else:
            tup = struct.unpack("!qqb{}b".format(len(b) - 17), b)
            m_id = '{:016x}'.format(tup[0])
            m_time = m_id
            m_type = '0{}'.format(tup[2])
            return tup, m_id + m_time + m_type + hex(tup[3])

    def on_disconnect(self, client, userdata, rc):
        if self.if_reconnect == "True":
            client.reconnect()
        else:
            print("mqtt断开连接")

    def push_data(self):
        client = Client(client_id=self.user, clean_session=False)
        client.username_pw_set(self.user, self.sha256_passwd)

        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(self.host, self.port)
        client.loop_start()

        if self.protocol.lower() == 'ilink':
            while not self.stop:
                status_payload = {"devId": self.dev_id, "online": 1, "time": 1650962002261}
                client.publish(self.up, json.dumps(status_payload))
                print('状态上报:{}'.format(status_payload))

                payload = {"operate": "ATTR_UP", "operateId": 1, "data": [
                    {"pk": self.pk, "devId": self.dev_id, "time": int(time.time() * 1000),
                     "params": {"temperature": self.temperature, "humidity": self.humidity}}]}

                client.publish(self.up, json.dumps(payload))
                print('属性上报:{}'.format(payload))
                if self.temperature < 30 and self.flag == 1:
                    event = {"operate": "EVENT_UP", "operateId": 1, "data": [
                        {"pk": self.pk, "devId": self.dev_id, "identifier": 'lowPower', "time": int(time.time() * 1000),
                         "params": {"temperature": self.temperature}}]}
                    client.publish(self.up, json.dumps(event))
                    print('事件上报:{}'.format(event))
                if self.temperature < 100:
                    self.temperature += self.step
                else:
                    self.temperature = 0
                self.humidity = random.randint(0, 100)
                # if self.temperature > 100:
                #     self.temperature = 0
                flag = 1
                time.sleep(self.interval)
        elif self.protocol.lower() == 'custom':
            while not self.stop:
                t = int(time.time() * 1000)
                msg_id = struct.pack(">q", t)
                msg_time = msg_id
                msg_type = struct.pack(">b", 1)
                temp = struct.pack(">b", self.temperature)
                hum = struct.pack(">b", self.humidity)
                message = msg_id + msg_time + msg_type + temp + hum
                client.publish(self.up, message)
                print("属性上报:{}".format(self.byte_to_hex(message)[1]))
                if self.temperature < 30 and self.flag == 1:
                    event_t = int(time.time() * 1000)
                    event_id = struct.pack(">q", event_t)
                    event_time = event_id
                    event_type = struct.pack(">b", 2)
                    event_name = 'lowPower'
                    event = event_id + event_time + event_type + event_name.encode()
                    client.publish(self.up, event)
                    print('事件上报:{}'.format(self.byte_to_hex(event)[1]))
                if self.temperature < 100:
                    self.temperature += self.step
                else:
                    self.temperature = 0
                self.humidity = random.randint(0, 100)
                # if self.temperature > 100:
                #     self.temperature = 0
                flag = 1
                time.sleep(self.interval)

    def do_mock(self):
        t1 = Thread(target=self.push_data)
        t1.start()

    def stop_mock(self):
        self.stop = True


if __name__ == '__main__':
    device_mock = DeviceMock()
    device_mock.do_mock()
