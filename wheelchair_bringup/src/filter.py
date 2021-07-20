#!/usr/bin/env python

from __future__ import print_function
import sys
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

class DoFilter:
    def __init__(self):

        self.sub = rospy.Subscriber("scan", LaserScan, self.callback)
        self.pub = rospy.Publisher("filteredscan", LaserScan, queue_size=1)

    def callback(self, data):

        newdata = data
        
        #The distance and intensity data read from the message are tuples, which need to be converted to list for operation
        newdata.ranges = list(data.ranges)
        newdata.intensities = list(data.intensities)

        #Keep valid data by clearing the data of unnecessary sectors
        for x in range(110,210):
            newdata.ranges[x]=0
            newdata.intensities[x]=0

        self.pub.publish(newdata)
        

if __name__ == '__main__':

    # Initialize
    rospy.init_node('LidarFilter', anonymous=False)
    lidar = DoFilter()

    rospy.spin()