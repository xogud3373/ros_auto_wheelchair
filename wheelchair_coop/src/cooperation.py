#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from wheelchair_msg.msg import caselidar

lidar_pub = None
front_ranges = []
lidar_ranges = []
state_description = ''

dist = 0
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

    for i in range(0,360):
        if lidar_ranges[i] == float('inf'):
            lidar_ranges[i] = 20
    
    front_ranges = lidar_ranges[0:30]
    front_tmp = lidar_ranges[330:359]
    front_ranges.extend(front_tmp)

    
    pos_degree = {
       
        'front'  : min(front_ranges),
        'fleft'  : min(lidar_ranges[30:90]),
        'fright' : min(lidar_ranges[270:330]),
        
    }

    take_action()

def find_angle(state):
    global curr_state, front_ranges, obj_deg, lidar_ranges

    if state == 1:
        if(front_ranges.index(min(front_ranges)) < 30):
            obj_deg = front_ranges.index(min(front_ranges))
	    print("front : %d" % (obj_deg))
        else:
            obj_deg = -(60 - front_ranges.index(min(front_ranges)))
	    print("front : %d" % (obj_deg))

    elif state == 2:    
        obj_deg = -(360 -(lidar_ranges[270:330].index(min(lidar_ranges[270:330])) + 270)) 
        print("fright : %d" % (obj_deg))
    
    elif state == 3:
        obj_deg = (lidar_ranges[30:90].index(min(lidar_ranges[30:90]))) + 30
        print("fleft : %d" % (obj_deg))

    else:
        obj_deg = 0
	print("no object")

def change_state(state):
    global curr_state, state_dict
    
    if state is not curr_state:
        #print('mode: [%s] - %s'%(state, state_dict[state]))
        curr_state = state

    #print("state : %s" % (state_description))
    find_angle(curr_state)

def take_action():
    global pos_degree, state_description, dist

    pub_lidar = caselidar()

    state_description = ''

    dist = 0.65

    
    if pos_degree['front'] < dist + 0.55 and pos_degree['fleft'] > dist + 0.25 and pos_degree['fright'] > dist - 0.25:
        state_description = ' case 2 - front '
        change_state(1)
    elif pos_degree['front'] > dist + 0.55 and pos_degree['fleft'] > dist + 0.25 and pos_degree['fright'] < dist - 0.25:
        state_description = ' case 3 - fright '
        change_state(2)
    elif pos_degree['front'] > dist + 0.55 and pos_degree['fleft'] < dist + 0.25 and pos_degree['fright'] > dist - 0.25:
        state_description = ' case 4 - fleft '
        change_state(3)
    elif pos_degree['front'] < dist + 0.55 and pos_degree['fleft'] > dist + 0.25 and pos_degree['fright'] < dist - 0.25:
        state_description = ' case 5 - front and fright '
        change_state(2)
    elif pos_degree['front'] < dist + 0.55 and pos_degree['fleft'] < dist + 0.25 and pos_degree['fright'] > dist - 0.25:
        state_description = ' case 6 - front and fleft '
        change_state(3)
    elif pos_degree['front'] < dist + 0.55 and pos_degree['fleft'] < dist + 0.25 and pos_degree['fright'] < dist - 0.25:
        state_description = ' case 7 - front and fleft and fright '
        change_state(1)
    elif pos_degree['front'] > dist + 0.55 and pos_degree['fleft'] < dist + 0.25 and pos_degree['fright'] < dist - 0.25:
        state_description = ' case 8 - fleft and fright '
        change_state(0)
    elif pos_degree['front'] > dist + 0.55 and pos_degree['fleft'] > dist + 0.25 and pos_degree['fright'] > dist - 0.25:
        state_description = ' case 1 - not object - normal drive '
        change_state(0)
    else:
        state_description = ' unknown case '
        rospy.loginfo(pos_degree)
    


def main():
    global pos_degree, dist, obj_deg

    rospy.init_node('send_lidar')

    lidar_pub = rospy.Publisher('/lidar_ranges', caselidar, queue_size=1)
    
    laser_sub = rospy.Subscriber('/scan_filtered', LaserScan, clbk_laser)

    rate = rospy.Rate(50)    # 10hz 0.1s
    while not rospy.is_shutdown():
        pub_lidar = caselidar()

        if curr_state == 0:
            pub_lidar.object_pos = 'normal'
            pub_lidar.front_range = dist
            pub_lidar.left_range = dist     
            pub_lidar.right_range = dist
            pub_lidar.lidar_deg = 0
            lidar_pub.publish(pub_lidar)
        elif curr_state == 1:
            pub_lidar.object_pos = 'stop'
            pub_lidar.front_range = pos_degree['front']
            pub_lidar.left_range = dist
            pub_lidar.right_range = dist
            pub_lidar.lidar_deg = obj_deg
            lidar_pub.publish(pub_lidar)
        elif curr_state == 2:
            pub_lidar.object_pos = 'right'
            pub_lidar.front_range = dist
            pub_lidar.left_range = dist
            pub_lidar.right_range = pos_degree['fright']
            pub_lidar.lidar_deg = obj_deg
            lidar_pub.publish(pub_lidar)
        elif curr_state == 3:
            pub_lidar.object_pos = 'left'
            pub_lidar.front_range = dist
            pub_lidar.left_range = pos_degree['fleft']
            pub_lidar.right_range = dist
            pub_lidar.lidar_deg = obj_deg
            lidar_pub.publish(pub_lidar)
            
        else:
            rospy.logerr('Unknown state!')

        rate.sleep()

if __name__ == '__main__':
    main()



