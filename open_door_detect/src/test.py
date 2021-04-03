#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from sensor_msgs.msg import LaserScan

MAX_LIDAR_ANGLE = 3.14159274101

lidar_angle = []
lidar_ranges = []
count = 0

def clbk_laser(msg):
    global lidar_angle, lidar_ranges    
    lidar_angle_increment = 0
    lidar_angle = []
    
    lidar_ranges = list(msg.ranges)
    
    # 라이다 각도 배열 저장 => 1도씩
    for a in range(0, 360):
        lidar_angle_increment += msg.angle_increment  # 0.0174532923847
        lidar_angle.append(lidar_angle_increment)

    
   
    Is_door_check()
    
def Is_door_check():
    global count
    count += 1
    print("-----------------------")
    print("몇번 돌았냐면 : %d "%count)
    # # 초기값이 무한대일 경우에 대한 예외처리
    # if lidar_ranges[180] == float('inf'):
    #     first_door_len = 12
    # else:
    #     first_door_len = lidar_ranges[180] 

    # 라이다 225도 부터 시작
    for i in range(225, 359):
        
        # 첫번째 문틀탐색 => 큰거리 -> 작은거리 (X) / 작은거리 -> 큰 거리 (O)
        # 문과의 거리 5미터로 제한
        if(lidar_ranges[i] < 5):
            if lidar_ranges[i + 1] > lidar_ranges[i] + 1:    # 1m = 1
                first_door_len = lidar_ranges[i]
                first_door_ang = lidar_angle[i]
                #print("f_ang : %.6f"%first_door_ang)

                # 무한대면 라이다 최대거리 12으로 치환, 아니면 그 값 그대로
                # if lidar_ranges[i + 1] == float('inf'):
                #     lidar_ranges[i + 1] = 12

                
                
                # 두번째 문틀탐색 => i + 10 번째부터 시작 => 10도 이상
                for j in range(i+10, 360):
                    # 225 ~ 360범위안에 두번째 문틀 검출
                    if lidar_ranges[j] < lidar_ranges[i]:
                        print(i)
                        print(j)
                        second_door_len = lidar_ranges[j]
                        second_door_ang = lidar_angle[j]
                        print("첫번째 폭 : %.3f"%first_door_len)
                        print("두번째 폭 : %.3f"%second_door_len)
                        print("첫번째 각 : %.3f"%first_door_ang)
                        print("두번째 각 : %.3f"%second_door_ang)
                        #print("s_ang : %.6f"%second_door_ang)

                        # 문틀 폭 계산 함수
                        door_width = Calc_Door_Width(first_door_len, second_door_len, first_door_ang, second_door_ang, 1)
                        if door_width > 0.5 and door_width < 2:
                            isdoor = True
                            
                            print("문이고 문 폭 : %.8f"%door_width)
                            # print("첫번째 폭 : %.3f"%first_door_ang)
                            # print("두번째 폭 : %.3f"%second_door_ang)
                            
                        else:
                            print("문X")
                                
                        
                    # 첫번째 문틀 탐색 된 후 225 ~ 360범위 안에 두번째 문틀 검출 안될 시 
                    else:
                        # 0 ~ 135범위에서 두번째 문틀 검출
                        for k in range(0, 135):
                        
                            if lidar_ranges[k] < lidar_ranges[i + 1]:
                                
                                second_door_len = lidar_ranges[k]
                                second_door_ang = lidar_angle[k]

                                # 문틀 폭 계산 함수
                                door_width = Calc_Door_Width(first_door_len, second_door_len, first_door_ang, second_door_ang, 2)
                                
                                
                                if door_width > 0.8 and door_width < 2:
                                    isdoor = True
                                    print("180 ~ 360 범위 문 발견")
                                    print(door_width)
                                else:
                                    break_flag = True
                                    break

    #  # 라이다 0~135도 시작
    # for q in range(0, 135):
        
    #     # 첫번째 문틀탐색 => 큰거리 -> 작은거리 (X) / 작은거리 -> 큰 거리 (O)
    #     if lidar_ranges[q + 1] > lidar_ranges[q] + 1:    # 1m = 1
    #         first_door_len = lidar_ranges[q]
    #         first_door_ang = lidar_angle[q]

    #         # 무한대면 라이다 최대거리 12으로 치환, 아니면 그 값 그대로
    #         if lidar_ranges[q + 1] == float('inf'):
    #             lidar_ranges[q + 1] = 12

    #         # break_flag = False

    #         # 두번째 문틀탐색 => i 번째부터 시작
    #         for w in range(q, 135):
    #             # 0 ~ 135범위안에 두번째 문틀 검출
    #             if lidar_ranges[w] < lidar_ranges[q + 1] and lidar_ranges[w] < lidar_ranges[q]:
    #                 second_door_len = lidar_ranges[w]
    #                 second_door_ang = lidar_angle[w]

    #                 # 문틀 폭 계산 함수
    #                 door_width = Calc_Door_Width(first_door_len, second_door_len, first_door_ang, second_door_ang, 2)
    #                 if door_width > 0.8:
    #                     isdoor = True
    #                     #print("0 ~ 135 범위 문 발견")
    #                     #print(door_width)
    #                 else:
    #                     break

                    


def Calc_Door_Width(first_len, second_len, first_ang, second_ang, mode):
    if mode == 1:
        Theta_rad = second_ang - first_ang
        Theta = (Theta_rad * 180)/ math.pi
        
        b = first_len
        c = second_len
        b2 = first_len*first_len
        c2 = second_len*second_len
        # print("첫번째 폭 : %.3f"%b)
        # print("두번째 폭 : %.3f"%c)
        # print("Theta : %.6f"%Theta)
        



        door_width2 = b2 + c2 - 2*b*c*round(math.cos(Theta))
        door_width = math.sqrt(door_width2)

        #print(door_width)
        #print("180~360 : %.3f"%door_width)
        return door_width
        

    # elif mode == 2:
    #     Theta_1 = MAX_LIDAR_ANGLE - first_ang
    #     Theta_2 = second_ang
    #     Theta_rad = Theta_1 + Theta_2
    #     Theta = (Theta_rad * 180)/ math.pi
        
    #     b = first_len
    #     c = second_len
    #     b2 = first_len*first_len
    #     c2 = second_len*second_len
        
    #     door_width2 = b2 + c2 - 2*b*c*round(math.cos(Theta))
    #     door_width = math.sqrt(door_width2)

    #     print("0~180 : %.3f"%door_width)
    #     return door_width

            

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