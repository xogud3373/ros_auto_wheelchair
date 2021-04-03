#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

vel_pub = None
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

def clbk_laser(msg):
    global pos_degree

    lidar_ranges = list(msg.ranges)

    for i in range(0,505):
        if lidar_ranges[i] == 0:
            lidar_ranges[i] += 20
    
    pos_degree = {
        # 'right'  : min(min(msg.ranges[0:100]), 10),
        # 'fright' : min(min(msg.ranges[101:201]), 10),
        # 'front'  : min(min(msg.ranges[202:302]), 10),
        # 'fleft'  : min(min(msg.ranges[303:403]), 10),
        # 'left'   : min(min(msg.ranges[404:504]), 10),

        'right'  : min(lidar_ranges[125:175]),
        'fright' : min(lidar_ranges[176:236]),
        'front'  : min(lidar_ranges[237:287]),
        'fleft'  : min(lidar_ranges[288:338]),
        'left'   : min(lidar_ranges[339:389]),

        # 'right'  : right_min_range,
        # 'fright' : fright_min_range,
        # 'front'  : front_min_range,
        # 'fleft'  : fleft_min_range,
        # 'left'   : left_min_range,
    }

    take_action()

def change_state(state):
    global curr_state, state_dict
    
    if state is not curr_state:
        print('mode: [%s] - %s'%(state, state_dict[state]))
        curr_state = state

    print("state : %s" % (state_description))

def take_action():
    global pos_degree, state_description
    # msg = Twist()
    # linear_x = 0
    # angular_z = 0

    state_description = ''

    dist = 0.5

    if pos_degree['front'] > dist and pos_degree['fleft'] > dist and pos_degree['fright'] > dist:
        # print('1')
        state_description = ' case 1 - not object - normal drive '
        change_state(0)
    elif pos_degree['front'] < dist and pos_degree['fleft'] > dist and pos_degree['fright'] > dist:
        # print('2')
        state_description = ' case 2 - front '
        change_state(1)
    elif pos_degree['front'] > dist and pos_degree['fleft'] > dist and pos_degree['fright'] < dist:
        # print('3')
        state_description = ' case 3 - fright '
        change_state(2)
    elif pos_degree['front'] > dist and pos_degree['fleft'] < dist and pos_degree['fright'] > dist:
        # print('4')
        state_description = ' case 4 - fleft '
        change_state(3)
    elif pos_degree['front'] < dist and pos_degree['fleft'] > dist and pos_degree['fright'] < dist:
        # print('5')
        state_description = ' case 5 - front and fright '
        change_state(2)
    elif pos_degree['front'] < dist and pos_degree['fleft'] < dist and pos_degree['fright'] > dist:
        # print('6')
        state_description = ' case 6 - front and fleft '
        change_state(3)
    elif pos_degree['front'] < dist and pos_degree['fleft'] < dist and pos_degree['fright'] < dist:
        # print('7')
        # print('regions : %s '%(pos_degree['front']))
        # print('regions : %s '%(pos_degree['fleft']))
        # print('regions : %s '%(pos_degree['fright']))
        state_description = ' case 7 - front and fleft and fright '
        change_state(1)
    elif pos_degree['front'] > dist and pos_degree['fleft'] < dist and pos_degree['fright'] < dist:
        # print('8')
        state_description = ' case 8 - fleft and fright '
        change_state(1)
    else:
        state_description = ' unknown case '
        rospy.loginfo(pos_degree)


def straight():
    msg = Twist()
    msg.linear.x = 0.25
    msg.angular.z = 0
    return msg

def stop():
    msg = Twist()
    msg.linear.x = 0
    msg.angular.z = 0
    return msg

def turn_left():
    msg = Twist()
    # msg.linear.x = 0.3
    msg.angular.z = 1
    return msg


def turn_right():
    msg = Twist()
    # msg.linear.x = 0.3
    msg.angular.z = -1
    return msg

def main():
    # global vel_pub

    rospy.init_node('reading_laser')

    vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
    laser_sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)

    rate = rospy.Rate(50)    # 10hz 0.1s
    while not rospy.is_shutdown():
        msg = Twist()
        if curr_state == 0:
            msg = straight()
        elif curr_state == 1:
            msg  = stop()
        elif curr_state == 2:
            msg = turn_left()
        elif curr_state == 3:
            msg = turn_right()
        else:
            rospy.logerr('Unknown state!')

        vel_pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    main()



