#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from laser_values.msg import caselidar

lidar_pub = None
pos_degree = {
    'right' : 0,
    'fright' : 0,
    'front' : 0,
    'fleft' : 0,
    'left' : 0,
}

state_description = ''
curr_state = 0
state_dict = {
    0: 'straight',
    1: 'stop',
    2: 'turn left',
    3: 'turn right'
}

def callback(msg):
    global pos_degree

    
    lidar_ranges = list(msg.ranges)
    
    for i in range(0,505):
        if lidar_ranges[i] == 0:
            lidar_ranges[i] += 20

    pos_degree = {
        'right'  : min(lidar_ranges[125:175]),
        'fright' : min(lidar_ranges[176:236]),
        'front'  : min(lidar_ranges[237:287]),
        'fleft'  : min(lidar_ranges[288:338]),
        'left'   : min(lidar_ranges[339:389]),
    }

    take_action()

def take_action():
    global pos_degree, state_description, lidar_pub

    pub_lidar = caselidar()

    state_description = ''

    dist = 0.5

    if pos_degree['front'] > dist and pos_degree['fleft'] > dist and pos_degree['fright'] > dist:
        state_description = ' case 1 - not object - normal drive '
        pub_lidar.object_pose = 'case1'
        pub_lidar.lidar_range = 20
        lidar_pub.publish(pub_lidar)
    elif pos_degree['front'] < dist and pos_degree['fleft'] > dist and pos_degree['fright'] > dist:
        state_description = ' case 2 - front '
        pub_lidar.object_pose = 'case2'
        pub_lidar.lidar_range = pos_degree['front']
        lidar_pub.publish(pub_lidar)
    elif pos_degree['front'] > dist and pos_degree['fleft'] > dist and pos_degree['fright'] < dist:
        pub_lidar.object_pose = 'case3'
        pub_lidar.lidar_range = pos_degree['fright']
        lidar_pub.publish(pub_lidar)
    elif pos_degree['front'] > dist and pos_degree['fleft'] < dist and pos_degree['fright'] > dist:
        state_description = ' case 4 - fleft '
        pub_lidar.object_pose = 'case4'
        pub_lidar.lidar_range = pos_degree['fleft']
        lidar_pub.publish(pub_lidar)
    elif pos_degree['front'] < dist and pos_degree['fleft'] > dist and pos_degree['fright'] < dist:
        state_description = ' case 5 - front and fright '
        pub_lidar.object_pose = 'case5'
        pub_lidar.lidar_range = pos_degree['fright']
        lidar_pub.publish(pub_lidar)
    elif pos_degree['front'] < dist and pos_degree['fleft'] < dist and pos_degree['fright'] > dist:
        state_description = ' case 6 - front and fleft '
        pub_lidar.object_pose = 'case6'
        pub_lidar.lidar_range = pos_degree['fleft']
        lidar_pub.publish(pub_lidar)
    elif pos_degree['front'] < dist and pos_degree['fleft'] < dist and pos_degree['fright'] < dist:
        state_description = ' case 7 - front and fleft and fright '
        pub_lidar.object_pose = 'case7'
        pub_lidar.lidar_range = pos_degree['front']
        lidar_pub.publish(pub_lidar)
    elif pos_degree['front'] > dist and pos_degree['fleft'] < dist and pos_degree['fright'] < dist:
        state_description = ' case 8 - fleft and fright '
        pub_lidar.object_pose = 'case8'
        pub_lidar.lidar_range = 20
        lidar_pub.publish(pub_lidar)
    else:
        state_description = ' unknown case '
        rospy.loginfo(pos_degree)


def main():
    global lidar_pub

    rospy.init_node('scan_values')
    sub = rospy.Subscriber('/scan', LaserScan, callback)
    lidar_pub = rospy.Publisher('lidar_ranges',caselidar, queue_size=1)
    rospy.spin()

if __name__ == '__main__':
    main()
