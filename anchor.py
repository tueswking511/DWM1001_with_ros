import paho.mqtt.client as mqtt
import rospy
import json
import threading
import time
from std_msgs.msg import String, Header, ColorRGBA
from geometry_msgs.msg import PointStamped,Quaternion, Pose, Point, Vector3
from visualization_msgs.msg import Marker

MQTT_Server_IP="192.168.139.131"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("dwm/node/+/uplink/config")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    data = json.loads(str(msg.payload))
    if(str(data["configuration"]["nodeType"]) == "ANCHOR"):
        t = threading.Thread(target = push_anchor, args = (data,))
        t.start()
		
def push_anchor(data):
    pub = rospy.Publisher('dwm/anchor/' + str(data["configuration"]["label"]), PointStamped, queue_size=128)
    rate = rospy.Rate(100)
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
                pose=Pose(Point(data["configuration"]["anchor"]["position"]["x"],data["configuration"]["anchor"]["position"]["y"], data["configuration"]["anchor"]["position"]["z"]+0.5), Quaternion(0, 0, 0, 1)),
                scale=Vector3(0.25, 0.25, 0.25),
                header=Header(frame_id='/my_frame'),
                color=ColorRGBA(0.0, 0.0, 0.0, 0.8),
                text=str(data["configuration"]["label"]))
    while True:
        pose.header.stamp = rospy.Time.now()
        pub.publish(pose)
        marker_publisher.publish(marker)
        time.sleep(1)

rospy.init_node('tag_black', anonymous=True)
anchor_x = [0,0,0,0]
anchor_y = [0,0,0,0]
anchor_z = [0,0,0,0]
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_Server_IP, 1883, 60)
client.loop_forever()
