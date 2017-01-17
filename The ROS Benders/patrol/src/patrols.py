#!/usr/bin/env python

import rospy
import actionlib
from std_msgs.msg import String, Int32
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

room_number = -1
#*** BELOW CODE TAKEN FROM Programming Robots with ROS: A Practical Introduction to the Robot Operating System, p.162
#*** AND EDITED BY TEAM The ROS Benders  ***
waypoints = [       #points of the classes and the start point
	[(13.0, 0.7, 0.0), (0.0, 0.0, 0.0, 1.0)],	
	[(8.5, 0.7, 0.0), (0.0, 0.0, 0.0, 1.0)],
	[(3.0, 0.7, 0.0), (0.0, 0.0, 0.0, 1.0)],
	[(0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 1.0)]
]
#*** BELOW CODE TAKEN FROM Programming Robots with ROS: A Practical Introduction to the Robot Operating System, p.162
def goal_pose(pose):    #turn the current pose into MoveBaseGoal
	goal_pose = MoveBaseGoal()
	goal_pose.target_pose.header.frame_id = 'map'
	goal_pose.target_pose.pose.position.x = pose[0][0]
	goal_pose.target_pose.pose.position.y = pose[0][1]
	goal_pose.target_pose.pose.position.z = pose[0][2]
	goal_pose.target_pose.pose.orientation.x = pose[1][0]
	goal_pose.target_pose.pose.orientation.y = pose[1][1]
	goal_pose.target_pose.pose.orientation.z = pose[1][2]
	goal_pose.target_pose.pose.orientation.w = pose[1][3]
	
	return goal_pose

#*** BELOW CODE ADDED BY TEAM The ROS Benders ***
def find_the_room_number(msg):  #Takes room number from the message and transforms it to its index on waypoints array
	print("Mesaji aldim: {}".format(msg))
	msg = str(msg)
	num = int(''.join(str(i) for i in msg if i.isdigit() is True))
	print(num)
	if num in [2102, 2104, 2106]:
		num = (num - 2102) / 2
		print(room_number)
		global room_number
		room_number = num
		print(room_number)

#*** BELOW CODE TAKEN FROM Programming Robots with ROS: A Practical Introduction to the Robot Operating System, p.162
#*** AND EDITED BY TEAM The ROS Benders  ***
if __name__ == '__main__':
	rospy.init_node('patrols')    #initiates node to communicate with move_base
	rospy.Subscriber('/out_value', Int32, find_the_room_number)  #subscribes /out_value to have the room number
	print('Basladim')
	
	client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
	client.wait_for_server()

	while room_number == -1:
		pass
	
	pose = waypoints[room_number]  #pose is taken from the waypoints
	goal = goal_pose(pose)
	client.send_goal(goal)
	print("goal sent")			
	client.wait_for_result()
	print("result arrived")

	rospy.spin()

	
	
