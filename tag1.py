import time
import threading
import paho.mqtt.client as mqtt
import rospy
import json
import base64
import sys
from std_msgs.msg import String, Header, ColorRGBA
from geometry_msgs.msg import PointStamped, Quaternion, Pose, Point, Vector3
from visualization_msgs.msg import Marker

system_argv = sys.argv
MQTT_Server_IP = system_argv[1]

x1 = 0
y1 = 0
z1 = 0
x2 = 0
y2 = 0
z2 = 0
text_size = 0.10


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("dwm/node/d43a/uplink/location", 0), ("dwm/node/d43a/uplink/data", 0),
                      ("dwm/node/410d/uplink/location", 0), ("dwm/node/410d/uplink/data", 0),
		      ("dwm/node/+/uplink/config",0)])


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global x1, y1, z1, x2, y2, z2
    # print(msg.topic+" "+str(msg.payload))
    data = json.loads(str(msg.payload))

    if msg.topic == "dwm/node/d43a/uplink/location":
        pose = PointStamped()
        pose.header.frame_id = "/my_frame"
        pose.header.stamp = rospy.Time.now()
        if type(data["position"]["x"]) == float:
            print("TAG1:x:%.2f, y:%.2f, z:%.2f" % (data["position"]["x"], data["position"]["y"], data["position"]["z"]))
            x1 = data["position"]["x"]
            y1 = data["position"]["y"]
            z1 = data["position"]["z"]
            pose.point.x = data["position"]["x"]
            pose.point.y = data["position"]["y"]
            pose.point.z = data["position"]["z"]
        pub.publish(pose)

    elif msg.topic == "dwm/node/d43a/uplink/data":
        print("IMU1:%s" % filter(lambda ch: ch in '0123456789-.,', base64.b64decode(data["data"])))
        temp = filter(lambda ch: ch in '0123456789-.,', base64.b64decode(data["data"]))
        location = 0
        for i in range(3):
            location = base64.b64decode(data["data"]).find(",", location + 1)
        # print("Accel:%s\nGyro:%s\n" % (temp[:location], temp[location + 1:]))
        marker_publisher = rospy.Publisher('visualization_marker/Tag1', Marker, queue_size=128)
        marker = Marker(
            type=Marker.TEXT_VIEW_FACING,
            id=0,
            lifetime=rospy.Duration(1000),
            pose=Pose(Point(x1, y1, z1 + 0.5),
                      Quaternion(0, 0, 0, 1)),
            scale=Vector3(text_size, text_size, text_size),
            header=Header(frame_id='/my_frame'),
            color=ColorRGBA(1.0, 1.0, 1.0, 0.8),
            text="UWB1\n" + "Pos:" + str(format(float(x1),'.2f')) + "," + str(format(float(y1),'.2f')) + "," + str(format(float(z1),'.2f')) + "\n" +
		 "Accel:" + temp[:location] + "\n" +
                 "Gyro:" + temp[location + 1:])
        marker_publisher.publish(marker)

    elif msg.topic == "dwm/node/410d/uplink/location":
        pose = PointStamped()
        pose.header.frame_id = "/my_frame"
        pose.header.stamp = rospy.Time.now()
        if type(data["position"]["x"]) == float:
            print("TAG2:x:%.2f, y:%.2f, z:%.2f" % (data["position"]["x"], data["position"]["y"], data["position"]["z"]))
            x2 = data["position"]["x"]
            y2 = data["position"]["y"]
            z2 = data["position"]["z"]
            pose.point.x = data["position"]["x"]
            pose.point.y = data["position"]["y"]
            pose.point.z = data["position"]["z"]
        pub2.publish(pose)

    elif msg.topic == "dwm/node/410d/uplink/data":
	print("IMU2:%s" % filter(lambda ch: ch in '0123456789-.,', base64.b64decode(data["data"])))
        temp = filter(lambda ch: ch in '0123456789-.,', base64.b64decode(data["data"]))
        location = 0
        for i in range(3):
            location = base64.b64decode(data["data"]).find(",", location + 1)
        # print("Accel:%s\nGyro:%s\n" % (temp[:location], temp[location + 1:]))
        marker_publisher2 = rospy.Publisher('visualization_marker/Tag2', Marker, queue_size=128)
        marker2 = Marker(
            type=Marker.TEXT_VIEW_FACING,
            id=0,
            lifetime=rospy.Duration(1000),
            pose=Pose(Point(x2, y2, z2 + 0.5),
                      Quaternion(0, 0, 0, 1)),
            scale=Vector3(text_size, text_size, text_size),
            header=Header(frame_id='/my_frame'),
            color=ColorRGBA(1.0, 1.0, 1.0, 0.8),
            text="UWB2\n" + "Pos:" + str(format(float(x2),'.2f')) + "," + str(format(float(y2),'.2f')) + "," + str(format(float(z2),'.2f')) + "\n" +
		 "Accel:" + temp[:location] + "\n" +
                 "Gyro:" + temp[location + 1:])
        marker_publisher2.publish(marker2)

    elif str(data["configuration"]["nodeType"]) == "ANCHOR":
	print(msg.topic+" "+str(msg.payload))
        t = threading.Thread(target=push_anchor, args=(data,))
	t.setDaemon(True)
        t.start()


def push_anchor(data):
    pub_anchor = rospy.Publisher('dwm/anchor/' + str(data["configuration"]["label"]), PointStamped, queue_size=128)
    rate = rospy.Rate(1000)
    pose = PointStamped()
    pose.header.frame_id = "/my_frame"
    pose.point.x = data["configuration"]["anchor"]["position"]["x"]
    pose.point.y = data["configuration"]["anchor"]["position"]["y"]
    pose.point.z = data["configuration"]["anchor"]["position"]["z"]
    marker_publisher = rospy.Publisher('visualization_marker/'+str(data["configuration"]["label"]), Marker, queue_size=128)
    marker = Marker(
                type=Marker.TEXT_VIEW_FACING,
                id=0,
                lifetime=rospy.Duration(1.5),
                pose=Pose(Point(data["configuration"]["anchor"]["position"]["x"],data["configuration"]["anchor"]["position"]["y"], data["configuration"]["anchor"]["position"]["z"]-0.5), Quaternion(0, 0, 0, 1)),
                scale=Vector3(0.25, 0.25, 0.25),
                header=Header(frame_id='/my_frame'),
                color=ColorRGBA(0.0, 0.0, 0.0, 0.8),
                text=str(data["configuration"]["label"]))
    while True:
        pose.header.stamp = rospy.Time.now()
        pub_anchor.publish(pose)
        marker_publisher.publish(marker)
        time.sleep(1)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_Server_IP, 1883, 60)

pub = rospy.Publisher('dwm/tag/Tag1/Pose', PointStamped, queue_size=128)
pub2 = rospy.Publisher('dwm/tag/Tag2/Pose', PointStamped, queue_size=128)
rospy.init_node('tag_black', anonymous=True)
rate = rospy.Rate(1000)

client.loop_forever()
