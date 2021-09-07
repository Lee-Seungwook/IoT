import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time


MQTT_Broker = "test.mosquitto.org"  # 자신의 pc(brker) ip


def on_connect(client, userdata, flags, rc):
    print("Connect with result code" + str(rc))
    client.subscribe("/CCL/IoTP-UP201636030")  # Topic #dht/CCL이라는 토픽을 가진 기기를 구독


def on_message(client, userdata, msg):  # 구독한 기기의 정보를 출력
    x = str(msg.payload.decode('utf-8'))  # dht 센서 데이터
    print(msg.topic + "" + x)
    if(x != "on" and x!= "off"):
        y = eval(x)

        if y["im"] == "201636030_LeeSeungwook":
            publish.single("/CCL/IoTP-DN201636030", "on-201636030", hostname=MQTT_Broker)

            if y["LED"] == "led-201636030":
                publish.single("/CCL/IoTP-DN201636030", "led-201636030", hostname=MQTT_Broker)


def on_publish(client, userdata, mid):
    print("message publish..")


def on_disconnect(client, userdata, rc):
    print("Disconnected")


client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_Broker, 1883, 60)
client.on_message = on_message
client.on_publish = on_publish
client.on_disconnect = on_disconnect
client.loop_forever()