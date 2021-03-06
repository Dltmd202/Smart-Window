import time

import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
gpio.setwarnings(False)
import json


class Lock:
    def __init__(self, ip="localhost"):
        self._client = None
        self.ip = ip
        self.mpin = 18
        self.servo_pwm = None

    @property
    def client(self):
        if self._client:
            return self._client
        else:
            client = mqtt.Client()

            def on_connect(client, userdata, flags, rc):
                print("Connected Lock_Control " + str(rc))
                client.subscribe("control/lock")

            def on_message(client, userdata, msg):
                print(f"[{msg.topic}] sub : {msg.payload}")
                self.control_lock(msg)

            client.on_connect = on_connect
            client.on_message = on_message
            self._client = client
            return client

    def init_pin(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(self.mpin, gpio.OUT)
        self.servo_pwm = gpio.PWM(self.mpin, 50)
        self.servo_pwm.start(0)

    def lock(self):
        self.servo_pwm.ChangeDutyCycle(6.5)
        time.sleep(0.5)

    def unlock(self):
        self.servo_pwm.ChangeDutyCycle(2)
        time.sleep(0.5)

    def control_lock(self, msg):
        state = json.loads(msg.payload)["is_lock"]
        if state == True:
            time.sleep(2)
            print("Lock!!!!")
            lock()
        else:
            print("unLock!!!!")
            unlock()

    def run(self):
        self.client.connect(self.ip)
        self.init_pin()
        try:
            self.client.loop_forever()
        except KeyboardInterrupt:
            print("Finished lock!")
            self.client.unsubscribe("control/lock")
            self.client.disconnect()
            gpio.cleanup()


if __name__ == "__main__":
    Lock_Control = Lock()
    Lock_Control.run()
