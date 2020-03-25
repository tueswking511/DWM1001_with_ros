#!/bin/bash

gnome-terminal -e "rosrun tf static_transform_publisher $1 $2 $3 $4 $5 $6 $7 map my_frame 10"