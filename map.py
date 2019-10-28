import rospy
 
from visualization_msgs.msg import *
 
if __name__=="__main__":
 
	rospy.init_node("cube", anonymous=True)

	rate = rospy.Rate(20)
	
	marker_pub = rospy.Publisher("/cube", Marker, queue_size=10)
	
	rospy.loginfo("Initializing...")
 
	marker = Marker()
	
	marker.header.frame_id = "/my_frame"
	
	marker.header.stamp = rospy.Time.now()
	
	marker.ns = "basic_shapes"
	
	marker.id = 0
	
	marker.type = Marker.CUBE
	
	marker.scale.x = 12
	marker.scale.y = 8
	marker.scale.z = 0.1

	marker.action = Marker.ADD
	
	marker.pose.position.x = 0.0
	marker.pose.position.y = 0.0
	marker.pose.position.z = -1.0
	marker.pose.orientation.x = 0.0
	marker.pose.orientation.y = 0.0
	marker.pose.orientation.z = 0.0
	marker.pose.orientation.w = 0.0
	
	marker.color.r = 0.0
	marker.color.g = 0.8
	marker.color.b = 0.0
	marker.color.a = 0.5
	
	marker.lifetime = rospy.Duration()
	
	while not rospy.is_shutdown():
		marker.header.stamp = rospy.Time.now()
		
		marker_pub.publish(marker)
		
		rate.sleep()

