import paho.mqtt.client as mqtt
import rospy
import json
from std_msgs.msg import String, Header, ColorRGBA
from geometry_msgs.msg import PointStamped, Quaternion, Pose, Point, Vector3
from visualization_msgs.msg import Marker

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("dwm/node/47b9/uplink/location")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    data = json.loads(str(msg.payload))
    pose = PointStamped()
    pose.header.frame_id = "/my_frame"
    pose.header.stamp = rospy.Time.now()
    if type(data["position"]["x"]) == float:
    	print("x:%f, y:%f, z:%f" % (data["position"]["x"], data["position"]["y"], data["position"]["z"]))
        pose.point.x = data["position"]["x"]
        pose.point.y = data["position"]["y"]
        pose.point.z = data["position"]["z"]
        marker_publisher = rospy.Publisher('visualization_marker/Black', Marker, queue_size=128)
        marker = Marker(
                type=Marker.TEXT_VIEW_FACING,
                id=0,
                lifetime=rospy.Duration(1000),
                pose=Pose(Point(data["position"]["x"],data["position"]["y"], data["position"]["z"]+0.5), Quaternion(0, 0, 0, 1)),
                scale=Vector3(0.25, 0.25, 0.25),
                header=Header(frame_id='/my_frame'),
                color=ColorRGBA(0.0, 0.0, 0.0, 0.8),
                text="Black")
	pub.publish(pose)
        marker_publisher.publish(marker)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.137.131", 1883, 60)

pub = rospy.Publisher('dwm/tag/black/Pose', PointStamped, queue_size=128)
rospy.init_node('tag_black', anonymous=True)
rate = rospy.Rate(1000)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
