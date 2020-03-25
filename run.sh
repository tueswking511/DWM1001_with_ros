#!/bin/bash

gnome-terminal -e "roscore" && sleep 5

gnome-terminal -e "rosrun rviz rviz"

gnome-terminal -e "rosrun tf static_transform_publisher 0 0 0 0 0 0 1 map my_frame 10"

python /home/user/DWM1001_with_ros/tag1.py $1