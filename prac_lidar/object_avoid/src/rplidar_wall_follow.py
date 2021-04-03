#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from laser_values.msg import caselidar

lidar_pub = None

pos_degree = {
    # 'right' : 0,
    # 'fright' : 0,
    # 'front' : 0,
    # 'fleft' : 0,
    # 'left' : 0,

    'front' : 0,
    'fright' : 0,
    'fleft' : 0,
}

state_description = ''

dist = 0
curr_state = 0
state_dict = {
    0: 'straight',
    1: 'stop',
    2: 'turn left',
    3: 'turn right'
}

def clbk_laser(msg):
    global pos_degree

    lidar_ranges = list(msg.ranges)

    for i in range(0,360):
        if lidar_ranges[i] == float('inf'):
            lidar_ranges[i] = 20
    
    front_ranges = lidar_ranges[0:30]
    front_tmp = lidar_ranges[330:0]
    front_ranges.extend(front_tmp)

    pos_degree = {
       
        # 'right'  : min(lidar_ranges[125:175]),
        # 'fright' : min(lidar_ranges[176:236]),
        # 'front'  : min(lidar_ranges[237:287]),
        # 'fleft'  : min(lidar_ranges[288:338]),
        # 'left'   : min(lidar_ranges[339:389]),

        'front'  : min(front_ranges),
        'fleft'  : min(lidar_ranges[30:90]),
        'fright' : min(lidar_ranges[270:330]),
        
    }

    take_action()

def change_state(state):
    global curr_state, state_dict
    
    if state is not curr_state:
        print('mode: [%s] - %s'%(state, state_dict[state]))
        curr_state = state

    print("state : %s" % (state_description))

def take_action():
    global pos_degree, state_description, dist

    pub_lidar = caselidar()

    state_description = ''

    dist = 0.6

    if pos_degree['front'] > dist and pos_degree['fleft'] > dist and pos_degree['fright'] > dist:
        state_description = ' case 1 - not object - normal drive '
        change_state(0)
    elif pos_degree['front'] < dist and pos_degree['fleft'] > dist and pos_degree['fright'] > dist:
        state_description = ' case 2 - front '
        change_state(1)
    elif pos_degree['front'] > dist and pos_degree['fleft'] > dist and pos_degree['fright'] < dist:
        state_description = ' case 3 - fright '
        change_state(2)
    elif pos_degree['front'] > dist and pos_degree['fleft'] < dist and pos_degree['fright'] > dist:
        state_description = ' case 4 - fleft '
        change_state(3)
    elif pos_degree['front'] < dist and pos_degree['fleft'] > dist and pos_degree['fright'] < dist:
        state_description = ' case 5 - front and fright '
        change_state(2)
    elif pos_degree['front'] < dist and pos_degree['fleft'] < dist and pos_degree['fright'] > dist:
        state_description = ' case 6 - front and fleft '
        change_state(3)
    elif pos_degree['front'] < dist and pos_degree['fleft'] < dist and pos_degree['fright'] < dist:
        state_description = ' case 7 - front and fleft and fright '
        change_state(1)
    elif pos_degree['front'] > dist and pos_degree['fleft'] < dist and pos_degree['fright'] < dist:
        state_description = ' case 8 - fleft and fright '
        change_state(0)
    else:
        state_description = ' unknown case '
        rospy.loginfo(pos_degree)
    


def main():
    global pos_degree, dist

    rospy.init_node('send_lidar')

    lidar_pub = rospy.Publisher('/lidar_ranges', caselidar, queue_size=1)
    
    laser_sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)

    rate = rospy.Rate(50)    # 10hz 0.1s
    while not rospy.is_shutdown():
        pub_lidar = caselidar()

        if curr_state == 0:
            pub_lidar.object_pose = 'normal'
            pub_lidar.front_range = dist
            pub_lidar.left_range = dist     
            pub_lidar.right_range = dist
            lidar_pub.publish(pub_lidar)
        elif curr_state == 1:
            pub_lidar.object_pose = 'stop'
            pub_lidar.front_range = pos_degree['front']
            pub_lidar.left_range = dist
            pub_lidar.right_range = dist
            lidar_pub.publish(pub_lidar)
        elif curr_state == 2:
            pub_lidar.object_pose = 'right'
            pub_lidar.front_range = dist
            pub_lidar.left_range = dist
            pub_lidar.right_range = pos_degree['fright']
            lidar_pub.publish(pub_lidar)
        elif curr_state == 3:
            pub_lidar.object_pose = 'left'
            pub_lidar.front_range = dist
            pub_lidar.left_range = pos_degree['fleft']
            pub_lidar.right_range = dist
            lidar_pub.publish(pub_lidar)
            
        else:
            rospy.logerr('Unknown state!')

        rate.sleep()

if __name__ == '__main__':
    main()




