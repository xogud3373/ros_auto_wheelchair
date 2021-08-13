#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from wheelchair_msg.msg import caselidar

lidar_pub = None
front_ranges = []
lidar_ranges = []
state_description = ''

front_dist = 0
left_dist = 0
right_dist = 0
curr_state = 0
obj_deg = 0


pos_degree = {

    'front' : 0,
    'fright' : 0,
    'fleft' : 0,
}

state_dict = {
    0: 'straight',
    1: 'stop',
    2: 'turn left',
    3: 'turn right'
}

def clbk_laser(msg):
    global pos_degree,front_ranges, lidar_ranges

    lidar_ranges = []
    lidar_ranges = list(msg.ranges)

    for i in range(0,720):
        if lidar_ranges[i] == float('inf'):
            lidar_ranges[i] = 20
    
    front_ranges = lidar_ranges[0:84]
    front_tmp = lidar_ranges[686:719]
    front_ranges.extend(front_tmp)
    print('111111')
    print(lidar_ranges)
    print('-----')
    pos_degree = {
       
        'front'  : min(front_ranges),
        'fleft'  : min(lidar_ranges[85:180]),
        'fright' : min(lidar_ranges[540:686]),
        
    }

    take_action()

def find_angle(state):
    global curr_state, front_ranges, obj_deg, lidar_ranges

    if state == 1:
        if front_ranges.index(min(front_ranges)) < 84:
            obj_deg = (front_ranges.index( min(front_ranges) ) / 2.0)
            print(front_ranges)
            print('222222')
            # if obj_deg != 0:
            #     obj_deg = obj_deg / 2.0
            # elif obj_deg == 0:
            #     obj_deg = 0    
            print("front1 : %.3f" % (obj_deg))
        
        else:
            obj_deg = -( (120 - front_ranges.index( min(front_ranges) ) ) / 2.0 )
            print("front2 : %.3f" % (obj_deg))

    elif state == 2:    
        obj_deg = -( (720 - ( lidar_ranges[540:686].index(min( lidar_ranges[540:686]) ) + 540) ) / 2.0 ) 
        print("fright : %.3f" % (obj_deg))
    
    elif state == 3:
        obj_deg = (( lidar_ranges[85:180].index(min(lidar_ranges[85:180]) ) ) / 2.0) + 43
        # if obj_deg != 0:
        #     obj_deg = (obj_deg / 2.0) + 43
        # else:
        #     obj_deg = 43
        print("fleft : %.3f" % (obj_deg))

    else:
        obj_deg = 0
	print("no object")

def change_state(state):
    global curr_state, state_dict
    
    if state is not curr_state:
        print('mode: [%s] - %s'%(state, state_dict[state]))
        curr_state = state

    print("state : %s" % (state_description))
    find_angle(curr_state)

def take_action():
    global pos_degree, state_description, front_dist, left_dist, right_dist

    pub_lidar = caselidar()

    state_description = ''

    front_dist = 0.6
    left_dist = 0.6
    right_dist = 0.6
    dist = 0.65

    
    if pos_degree['front'] < front_dist and pos_degree['fleft'] > left_dist and pos_degree['fright'] > right_dist:
        state_description = ' case 2 - front '
        change_state(1)
    elif pos_degree['front'] > front_dist and pos_degree['fleft'] > left_dist and pos_degree['fright'] < right_dist:
        state_description = ' case 3 - fright '
        change_state(2)
    elif pos_degree['front'] > front_dist and pos_degree['fleft'] < left_dist and pos_degree['fright'] > right_dist:
        state_description = ' case 4 - fleft '
        change_state(3)
    elif pos_degree['front'] < front_dist and pos_degree['fleft'] > left_dist and pos_degree['fright'] < right_dist:
        state_description = ' case 5 - front and fright '
        change_state(2)
    elif pos_degree['front'] < front_dist and pos_degree['fleft'] < left_dist and pos_degree['fright'] > right_dist:
        state_description = ' case 6 - front and fleft '
        change_state(3)
    elif pos_degree['front'] < front_dist and pos_degree['fleft'] < left_dist and pos_degree['fright'] < right_dist:
        state_description = ' case 7 - front and fleft and fright '
        change_state(1)
    elif pos_degree['front'] > front_dist and pos_degree['fleft'] < left_dist and pos_degree['fright'] < right_dist:
        state_description = ' case 8 - fleft and fright '
        change_state(0)
    elif pos_degree['front'] > front_dist and pos_degree['fleft'] > left_dist and pos_degree['fright'] > right_dist:
        state_description = ' case 1 - not object - normal drive '
        change_state(0)
    else:
        state_description = ' unknown case '
        rospy.loginfo(pos_degree)
    


def main():
    global pos_degree, front_dist, left_dist, right_dist, obj_deg

    rospy.init_node('send_lidar')

    lidar_pub = rospy.Publisher('/lidar_ranges', caselidar, queue_size=1)
    
    laser_sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)

    rate = rospy.Rate(50)    # 10hz 0.1s
    while not rospy.is_shutdown():
        pub_lidar = caselidar()

        if curr_state == 0:
            pub_lidar.object_pos = 'normal'
            pub_lidar.front_range = front_dist
            pub_lidar.left_range = left_dist     
            pub_lidar.right_range = right_dist
            pub_lidar.lidar_deg = 0
            lidar_pub.publish(pub_lidar)
        elif curr_state == 1:
            pub_lidar.object_pos = 'front'
            pub_lidar.front_range = pos_degree['front']
            pub_lidar.left_range = left_dist
            pub_lidar.right_range = right_dist
            pub_lidar.lidar_deg = obj_deg
            lidar_pub.publish(pub_lidar)
        elif curr_state == 2:
            pub_lidar.object_pos = 'right'
            pub_lidar.front_range = front_dist
            pub_lidar.left_range = left_dist
            pub_lidar.right_range = pos_degree['fright']
            pub_lidar.lidar_deg = obj_deg
            lidar_pub.publish(pub_lidar)
        elif curr_state == 3:
            pub_lidar.object_pos = 'left'
            pub_lidar.front_range = front_dist
            pub_lidar.left_range = pos_degree['fleft']
            pub_lidar.right_range = right_dist
            pub_lidar.lidar_deg = obj_deg
            lidar_pub.publish(pub_lidar)
            
        else:
            rospy.logerr('Unknown state!')

        rate.sleep()

if __name__ == '__main__':
    main()



