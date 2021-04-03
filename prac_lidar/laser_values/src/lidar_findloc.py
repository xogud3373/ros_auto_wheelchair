#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

def callback(msg):
    # print("0 : %d" %(msg.ranges[0]))
    # print("90 : %d" %(msg.ranges[90]))
    # print("180 : %d" %(msg.ranges[180]))
    # print("270 : %d" %(msg.ranges[270]))
    # print("360 : %d" %(msg.ranges[359]))
    
    #print(msg.ranges[0])
    #print(msg.ranges[90])
    #print(msg.ranges[180])
    #print(msg.ranges[270])
    print(msg.ranges[359])
    if msg.ranges[359] == float('inf'):
        print("ok")
    else :
        print("no")
   
    
    


rospy.init_node('scan_values')
sub = rospy.Subscriber('/scan',LaserScan, callback)
rospy.spin()