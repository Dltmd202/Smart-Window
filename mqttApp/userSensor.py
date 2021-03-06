import time
import paho.mqtt.client as mqtt
import json
import os


class UserSensor:
    def __init__(self, topic="sensor/user", IP="172.20.10.8"):
        self._client = None
        self.IP = IP
        self.topic = topic

    @property
    def client(self):
        if self._client:
            return self._client
        else:
            client = mqtt.Client()

            def on_connect(client, userdata, flags, rc):
                print("Connected User Sensor" + str(rc))

            def on_publish(client, userdata, mid):
                msg_id = mid

            client.on_connect = on_connect
            client.on_publish = on_publish
            self._client = client
            return client

    def run(self, msg):
        self.client.connect(self.IP)
        self.client.loop_start()
        try:
            self.client.publish(self.topic, json.dumps(msg))
            print(f"publishing : {msg}")
        except KeyboardInterrupt:
            print("Finished")
            self.client.loop_stop()
            self.client.disconnect()


if __name__ == "__main__":
    pass
