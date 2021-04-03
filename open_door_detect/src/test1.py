#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from sensor_msgs.msg import LaserScan

MAX_LIDAR_ANGLE = 3.14159274101

lidar_angle = []
lidar_ranges = []
left_inf_index = []
index_even_count_odd = []
count = 0

def clbk_laser(msg):
    global lidar_angle, lidar_ranges    
    lidar_angle_increment = 0
    lidar_angle = []
    lidar_ranges = []
    
    lidar_ranges = list(msg.ranges)
    
    # 라이다 각도 배열 저장 => 1도씩
    for a in range(0, 360):
        lidar_angle_increment += msg.angle_increment  # 0.0174532923847
        lidar_angle.append(lidar_angle_increment)

    
   
    Is_door_check()


def lidar_5m_over_delete():
    global lidar_ranges
    for i in range(225, 360):
        if lidar_ranges[i] > 5:
            lidar_ranges[i] = float('inf');

def lidar_inf_diff_80cm():
    global lidar_ranges
    for i in range(225, 360):
        if lidar_ranges[i] == float('inf'):
            if i == 359:
                break
            if abs(lidar_ranges[i - 1] - lidar_ranges[i + 1]) < 0.8:
                lidar_ranges[i] = (lidar_ranges[i - 1] + lidar_ranges[i + 1])/2


def lidar_left_inf_index_save():
    global left_inf_index
    left_inf_index = []
    for i in range(225, 360):
        if lidar_ranges[i] == float('inf'):
            left_inf_index.append(i)

def lidar_left_inf_seperate():
    global index_even_count_odd

    ctn_inf_cnt = 0
    inf_start_index = 0
    index_even_count_odd = []

    # index는 짝수번째, count값은 홀수번째로 지정하여 시작과 끝을 판단

    # 맨 처음 inf가 등장하는 배열 인덱스 저장 -> 인덱스, 카운터값 맞추기 위해서 먼저선언
    index_even_count_odd.append(left_inf_index[0])
    
    for i in range(1, len(left_inf_index)):
        diff = left_inf_index[i] - left_inf_index[i - 1]
        # inf가 연속적으로 얼마나 나오는지
        if diff == 1:
            inf_start_index += 1
            ctn_inf_cnt += 1

            # 마지막 배열값에 대한 처리
            if i == len(left_inf_index) - 1 :
                index_even_count_odd.append(ctn_inf_cnt)

        # 연속적인 inf가 끊겼을 때
        if diff > 1:
            inf_start_index += 1
            index_even_count_odd.append(ctn_inf_cnt)
            index_even_count_odd.append(left_inf_index[inf_start_index])
            ctn_inf_cnt = 0

            # 마지막 배열값에 대한 처리
            if i == len(left_inf_index) - 1:
                index_even_count_odd.append(ctn_inf_cnt)

def lidar_left_inf_trans():
    global lidar_ranges, index_even_count_odd

    for i in range(0,len(index_even_count_odd),2): # len = 10
        #print("len : %d out of range : %d"%(len(index_even_count_odd),i))
        if i == len(index_even_count_odd) - 2:
            break

        st_end_index = index_even_count_odd[i] + index_even_count_odd[i+1]
        nx_first_index = index_even_count_odd[i+2]

        # inf값 숫자로 변환
        if nx_first_index - st_end_index >= 5:
            if lidar_ranges[index_even_count_odd[i - 1]] < lidar_ranges[st_end_index +  1]:
                max = lidar_ranges[st_end_index + 1]
            else:
                max = lidar_ranges[index_even_count_odd[i - 1]]

            for inf_change in range(index_even_count_odd[i], st_end_index + 1): 
                lidar_ranges[inf_change] = max

        # 숫자를 inf로 변환
        else:
            for num_change in range(st_end_index + 1, nx_first_index): 
                lidar_ranges[num_change] = float('inf')


def Is_door_check():
    global count, lidar_ranges
    count += 1
    print("-----------------------")
    print("몇번 돌았냐면 : %d "%count)

    lidar_5m_over_delete()
    lidar_inf_diff_80cm()
    lidar_left_inf_index_save()
    lidar_left_inf_seperate()
    lidar_left_inf_trans()

    #print(lidar_ranges)
    
    # 라이다 225도 부터 시작
    for first_door in range(225, 360):
        if first_door == 359:
            break
        if lidar_ranges[first_door + 1] > lidar_ranges[first_door] + 1:
            first_door_len = lidar_ranges[first_door]
            first_door_ang = lidar_angle[first_door]

            for second_door in range(first_door + 5, 360):
                if second_door ==  359:
                    break
                if lidar_ranges[second_door + 1] < lidar_ranges[second_door] - 0.8:
                    second_door_len = lidar_ranges[second_door + 1]
                    second_door_ang = lidar_angle[second_door + 1]

                    # print("첫번째 길이 : %.3f"%first_door_len)
                    # print("두번째 길이 : %.3f"%second_door_len)
                    
                    # print("첫번째 폭 : %.3f"%first_door_ang)
                    # print("두번째 폭 : %.3f"%second_door_ang)
                        
                # 문틀 폭 계산 함수
                    door_width = Calc_Door_Width(first_door_len, second_door_len, first_door_ang, second_door_ang, 1)
                    print(door_width)
                    if door_width > 0.5 and door_width < 1.5:
                        isdoor = True

                        print("문이고 문 폭 : %.8f"%door_width)
                        break     
                    else:
                        print("문X")    
                    


def Calc_Door_Width(first_len, second_len, first_ang, second_ang, mode):
    if mode == 1:
        Theta_rad = second_ang - first_ang
        Theta = (Theta_rad * 180)/ math.pi
        
        b = first_len
        c = second_len
        b2 = first_len*first_len
        c2 = second_len*second_len
        
        # print("첫번째 제곱폭 : %.3f"%b2)
        # print("두번째 제곱폭 : %.3f"%c2)
        # print("Theta : %.6f"%Theta)
        
        # print("cos(rad) : %.6f"%math.cos(Theta_rad))
        # print("cos(Theta) : %.6f"%math.cos(Theta))
        door_width2 = b2 + c2 - (2*b*c*(math.cos(Theta_rad)))
        
        door_width = math.sqrt(door_width2)

        
        return door_width
                

def main():
    
    rospy.init_node('detect_door')

    #lidar_pub = rospy.Publisher('/detect_door', caselidar, queue_size=1)
    
    laser_sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    rospy.spin()
    #rate = rospy.Rate(50)    # 10hz 0.1s
    #while not rospy.is_shutdown():
    #    pub_lidar = caselidar()
    #    rate.sleep()

if __name__ == '__main__':
    main()