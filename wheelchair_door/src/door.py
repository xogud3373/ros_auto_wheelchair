#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import rospy
import math
from sensor_msgs.msg import LaserScan
from wheelchair_msg.msg import doormsg
from wheelchair_msg.srv import door_mode, door_modeResponse
# from wheelchair_door.msg import doorpos
# from wheelchair_door.srv import doorinfo, doorinfoResponse

MAX_LIDAR_ANGLE = 3.14159274101

lidar_angle = []
lidar_ranges = []
left_inf_index = []
index_even_count_odd = []
count = 0
mode = 	0
sub_mode = 0
is_door_cnt = 0
sum_door = 0
sum_x = 0
sum_y = 0
publish_cnt = 0

send_flag = False
door_scan_flag = False

lidar_pub = rospy.Publisher('/door_lidar', LaserScan, queue_size=1)
scann = LaserScan()    
door_pub = rospy.Publisher('/door_pos', doormsg, queue_size=1)
pos = doormsg()




def door_modeCallback(request):
    global mode, door_scan_flag, send_flag, sub_mode
    if request.door_req_flag == True:
        print("succ!!")
        mode = request.door_mode
        sub_mode = request.sub_door_mode
        door_scan_flag = True
        send_flag = True
        
        response = door_modeResponse()
        response.door_res_flag = True
        return True 


def clbk_laser(msg):
    global lidar_angle, lidar_ranges    
    lidar_angle_increment = 0
    lidar_angle = []
    lidar_ranges = []
    
    scann = msg
    #lidar_pub.publish(scann)

    lidar_ranges = list(msg.ranges)
    
    # 라이다 각도 배열 저장 => 1도씩
    for a in range(0, 360):
        lidar_angle.append(lidar_angle_increment)
        lidar_angle_increment += msg.angle_increment  # 0.0174532923847
        
    # 문 판별 함수 시작
    if door_scan_flag == True:
        Is_door_check(scann)

# 라이다 추출 거리 값이 5m 이상이면 inf 값으로 대치 
def lidar_5m_over_delete(mode):
    global lidar_ranges
    
    if mode == 1:     # front
        for i in range(0, 90):
            if lidar_ranges[i] > 5:
                lidar_ranges[i] = float('inf')
        for j in range(270, 360):
            if lidar_ranges[j] > 5:
                lidar_ranges[j] = float('inf')

    elif mode == 2:   # left
        for i in range(0, 135):
            if lidar_ranges[i] > 5:
                lidar_ranges[i] = float('inf')

    elif mode == 3:   # right
        for i in range(225, 360):
            if lidar_ranges[i] > 5:
                lidar_ranges[i] = float('inf')


# 거리 값 나오다가 쓰레기 값인 inf 제거 => 1개에 대한 처리 
def lidar_inf_diff_80cm(mode):
    global lidar_ranges

    if mode == 1:
        for i in range(0, 90):
            if lidar_ranges[i] == float('inf'):
                if i == 89:
                    break
                
                if abs(lidar_ranges[i - 1] - lidar_ranges[i +1]) < 0.8:
                    lidar_ranges[i] = (lidar_ranges[i - 1] + lidar_ranges[i + 1])/2
        
        for i in range(270, 360):
            if lidar_ranges[i] == float('inf'):
                if i == 359:
                    break
                
                if abs(lidar_ranges[i - 1] - lidar_ranges[i +1]) < 0.8:
                    lidar_ranges[i] = (lidar_ranges[i - 1] + lidar_ranges[i + 1])/2
        

    elif mode == 2:
        for i in range(0, 135):
            if lidar_ranges[i] == float('inf'):
                if i == 134:
                    break

                if abs(lidar_ranges[i - 1] - lidar_ranges[i +1]) < 0.8:
                    lidar_ranges[i] = (lidar_ranges[i - 1] + lidar_ranges[i + 1])/2

    elif mode == 3:
        for i in range(225, 360):
            if lidar_ranges[i] == float('inf'):
                if i == 359:
                    break

                # inf값 앞 뒤 차가 80cm이하면 쓰레기 값으로 판단하여 거리값으로 대치
                if abs(lidar_ranges[i - 1] - lidar_ranges[i + 1]) < 0.8:
                    lidar_ranges[i] = (lidar_ranges[i - 1] + lidar_ranges[i + 1])/2


# 거리값, inf값에 대한 선형화 => 남은 inf 값 인덱스를 배열에 저장 
def lidar_left_inf_index_save(mode):
    global left_inf_index
    left_inf_index = []

    if mode == 1:
        for i in range(0, 90):
            if lidar_ranges[i] == float('inf'):
                left_inf_index.append(i)
        for i in range(270, 360):
            if lidar_ranges[i] == float('inf'):
                left_inf_index.append(i)

    elif mode == 2:
        for i in range(0, 135):
            if lidar_ranges[i] == float('inf'):
                left_inf_index.append(i)

    elif mode == 3:
        for i in range(225, 360):
            if lidar_ranges[i] == float('inf'):
                left_inf_index.append(i)


# 거리값, inf값에 대한 선형화 => inf 값의 연속성 판단
# inf 의 index는 짝수번째, count값은 홀수번째로 지정하여 시작과 끝을 판단
def lidar_left_inf_seperate(mode):
    global index_even_count_odd

    ctn_inf_cnt = 0
    inf_start_index = 0
    index_even_count_odd = []

    
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


# 거리값, inf값에 대한 선형화 => 거리값으로 판단되면  거리값으로, inf로 판단되면 inf로
def lidar_left_inf_trans(mode):
    global lidar_ranges, index_even_count_odd

    # 인덱스가 짝수번째에 있기에 2스텝씩
    for i in range(0,len(index_even_count_odd), 2): 
        if i == len(index_even_count_odd) - 2:
            break

        # inf 시작 배열의 끝 인덱스
        st_end_index = index_even_count_odd[i] + index_even_count_odd[i+1]
        inf_count = index_even_count_odd[i+1]
            
        # 다음 inf 시작 배열의 인덱스
        nx_first_index = index_even_count_odd[i+2]

        # inf값 숫자로 변환 => 시작 inf 묶음끝이 다음 inf 묶음시작의 차이가 5 이상이고 시작 inf 묶음 갯수가 5보다 작으면 거리값으로 판단
        if nx_first_index - st_end_index >= 5 and inf_count < 5:
            if lidar_ranges[index_even_count_odd[i] - 1] < lidar_ranges[st_end_index +  1]:
                max = lidar_ranges[st_end_index + 1]
            else:
                max = lidar_ranges[index_even_count_odd[i] - 1]

            for inf_change in range(index_even_count_odd[i], st_end_index + 1): 
                lidar_ranges[inf_change] = max

        # 숫자를 inf로 변환 => 5개 미만이면 빈공간으로 판단
        elif nx_first_index - st_end_index < 5:
            for num_change in range(st_end_index + 1, nx_first_index): 
                lidar_ranges[num_change] = float('inf')


def Is_door_check(scann):
    global count, lidar_ranges, mode, is_door_cnt, sum_door, sum_x, sum_y, pos, send_flag, publish_cnt

    count += 1
    
   
    lidar_5m_over_delete(mode)
    lidar_inf_diff_80cm(mode)
    lidar_left_inf_index_save(mode)
    lidar_left_inf_seperate(mode)
    lidar_left_inf_trans(mode)
    
    scann.ranges = lidar_ranges
    lidar_pub.publish(scann)

    # print("--------------")
    # print(lidar_ranges)
    # print("--------------")
    if mode == 1:
        if sub_mode == 1:
            for first_door_idx in range(0, 90):
                if first_door_idx == 89:
                    break
                if lidar_ranges[first_door_idx + 1] > lidar_ranges[first_door_idx] + 1:
                    for second_door in range(first_door_idx + 5, 90):
                        if second_door ==  89:
                            break
                        if lidar_ranges[second_door + 1] < lidar_ranges[second_door] - 0.8:
                            second_door_idx = second_door + 1
                                
                            # 문틀 폭 계산 함수
                            door_width = Calc_Door_Width(first_door_idx,second_door_idx, 1)
                            if door_width > 0.7 and door_width < 1.0:
                                is_door_cnt = is_door_cnt + 1
                                
                                
                                cor_first_door_idx, cor_second_door_idx = Open_Door_Filtering(first_door_idx, second_door_idx)
                                door_width = Calc_Door_Width(cor_first_door_idx, cor_second_door_idx, 1)
                                door_center_x, door_center_y  = Calc_Door_Pos(cor_first_door_idx, cor_second_door_idx, 1, door_width)    
                                
                                
                                sum_x +=door_center_x
                                sum_y += door_center_y
                                sum_door += door_width
                                if is_door_cnt == 10:
                                    avg_door_width = sum_door / 10
                                    avg_pos_x = sum_x / 10
                                    avg_pos_y = sum_y / 10
                                    is_door_cnt = 0
                                    sum_door = 0
                                    sum_x = 0
                                    sum_y = 0
                                    
                                    pos.x_pos = avg_pos_x
                                    pos.y_pos = avg_pos_y
                                    pos.door_width = avg_door_width
                                    pos.send_data_flag = send_flag
                                    pos.door_loc = 1
                                    pos.door_sub_loc = 1
                                    door_pub.publish(pos)
                                    send_flag = False
                                
                                break     
                            else:
                                pass
                                
                                
        if sub_mode == 2:
            for first_door_idx in range(270, 360):
                if first_door_idx == 359:
                    break
                if lidar_ranges[first_door_idx + 1] > lidar_ranges[first_door_idx] + 1:
                    for second_door in range(first_door_idx + 5, 360):
                        if second_door ==  359:
                            check_0_90_flag = True
                            break
                        if lidar_ranges[second_door + 1] < lidar_ranges[second_door] - 0.8:
                            second_door_idx = second_door + 1
                                
                            # 문틀 폭 계산 함수
                            door_width = Calc_Door_Width(first_door_idx, second_door_idx, 1)
                            if door_width > 0.7 and door_width < 1.0:
                                is_door_cnt = is_door_cnt + 1

                            
                                cor_first_door_idx, cor_second_door_idx = Open_Door_Filtering(first_door_idx, second_door_idx)
                                door_width = Calc_Door_Width(cor_first_door_idx, cor_second_door_idx, 1)
                                door_center_x, door_center_y  = Calc_Door_Pos(cor_first_door_idx, cor_second_door_idx, 1, door_width)    
                                
                                sum_x +=door_center_x
                                sum_y += door_center_y
                                sum_door += door_width
                                if is_door_cnt == 10:
                                    avg_door_width = sum_door / 10
                                    avg_pos_x = sum_x / 10
                                    avg_pos_y = sum_y / 10
                                    is_door_cnt = 0
                                    sum_door = 0
                                    sum_x = 0
                                    sum_y = 0
                                    
                                    pos.x_pos = avg_pos_x
                                    pos.y_pos = avg_pos_y
                                    pos.door_width = avg_door_width
                                    pos.send_data_flag = send_flag
                                    pos.door_loc = 1
                                    pos.door_sub_loc = 2
                                    door_pub.publish(pos)
                                    
                                    send_flag = False

                                break     
                            else:
                                pass
                                

        if sub_mode == 3:                        
            for first_door_idx in range(270, 360):
                if first_door_idx == 359:
                    break
                if lidar_ranges[first_door_idx + 1] > lidar_ranges[first_door_idx] + 1:
                    for second_door in range(0, 90):
                        if second_door ==  89:
                            break
                        if lidar_ranges[second_door + 1] < lidar_ranges[second_door] - 0.8:
                            second_door_idx = second_door + 1
                                
                            # 문틀 폭 계산 함수
                            door_width = Calc_Door_Width(first_door_idx, second_door_idx, 2)
                            if door_width > 0.7 and door_width < 4.5:
                                is_door_cnt = is_door_cnt + 1

                                
                                cor_first_door_idx, cor_second_door_idx = Open_Door_Filtering(first_door_idx, second_door_idx)
                                door_width = Calc_Door_Width(cor_first_door_idx, cor_second_door_idx, 2)
                                door_center_x, door_center_y  = Calc_Door_Pos(cor_first_door_idx, cor_second_door_idx, 1, door_width)    
                                
                                                         
                                sum_x +=door_center_x
                                sum_y += door_center_y
                                sum_door += door_width
                                if is_door_cnt == 10:
                                    publish_cnt = publish_cnt + 1
                                    avg_door_width = sum_door / 10
                                    avg_pos_x = sum_x / 10
                                    avg_pos_y = sum_y / 10
                                    is_door_cnt = 0
                                    sum_door = 0
                                    sum_x = 0
                                    sum_y = 0
                                    
                                    pos.x_pos = avg_pos_x
                                    pos.y_pos = avg_pos_y
                                    pos.door_width = avg_door_width
                                    pos.send_data_flag = send_flag
                                    pos.door_loc = 1
                                    pos.door_sub_loc = 3
                                    if publish_cnt == 5:
                                        door_pub.publish(pos)
                                        send_flag = False
                                        publish_cnt = 0    
                                    
                                break
                            else:
                                pass                                
                               
                                 
    
    elif mode == 2:
        # 라이다 0도 부터 시작
        for first_door_idx in range(0, 135):
            if first_door_idx == 134:
                break
            if lidar_ranges[first_door_idx + 1] > lidar_ranges[first_door_idx] + 1:
                for second_door in range(first_door_idx + 5, 135):
                    if second_door ==  134:
                        break
                    if lidar_ranges[second_door + 1] < lidar_ranges[second_door] - 0.8:
                        second_door_idx = second_door + 1
                            
                        # 문틀 폭 계산 함수
                        door_width = Calc_Door_Width(first_door_idx, second_door_idx, 1)
                        if door_width > 0.7 and door_width < 1.0:
                            is_door_cnt = is_door_cnt + 1
                                
                    
                            cor_first_door_idx, cor_second_door_idx = Open_Door_Filtering(first_door_idx, second_door_idx)
                            door_width = Calc_Door_Width(cor_first_door_idx, cor_second_door_idx, 1)
                            door_center_x, door_center_y  = Calc_Door_Pos(cor_first_door_idx, cor_second_door_idx, 2, door_width)    
                            
                            sum_x +=door_center_x
                            sum_y += door_center_y
                            sum_door += door_width
                            if is_door_cnt == 10:
                                avg_door_width = sum_door / 10
                                avg_pos_x = sum_x / 10
                                avg_pos_y = sum_y / 10
                                is_door_cnt = 0
                                sum_door = 0
                                sum_x = 0
                                sum_y = 0
                                
                                pos.x_pos = avg_pos_x
                                pos.y_pos = avg_pos_y
                                pos.door_width = avg_door_width
                                pos.send_data_flag = send_flag
                                pos.door_loc = 2
                                pos.door_sub_loc = 0
                                door_pub.publish(pos)
                                
                                send_flag = False
                            break     
                        else:
                            pass
                            #print("문X")


            # elif lidar_ranges[first_door_idx + 1] + 1.5 < lidar_ranges[first_door_idx]:
            #     if not lidar_ranges[first_door_idx] == float('inf'):
            #         second_door_idx = first_door_idx + 1
            #         first_door_idx = first_door_idx - 10
                    
            #         door_width = Calc_Door_Width(first_door_idx, second_door_idx, 1)
            #         if door_width > 0.7 and door_width < 3:
            #             is_door_cnt = is_door_cnt + 1
                                
            #             cor_first_door_idx, cor_second_door_idx = Open_Door_Filtering(first_door_idx, second_door_idx)
            #             door_width = Calc_Door_Width(cor_first_door_idx, cor_second_door_idx, 1)
            #             door_center_x, door_center_y  = Calc_Door_Pos(cor_first_door_idx, cor_second_door_idx, 1, door_width)    
                                
            #             sum_x +=door_center_x
            #             sum_y += door_center_y
            #             sum_door += door_width
            #             if is_door_cnt == 10:
            #                 avg_door_width = sum_door / 10
            #                 avg_pos_x = sum_x / 10
            #                 avg_pos_y = sum_y / 10
            #                 is_door_cnt = 0
            #                 sum_door = 0
            #                 sum_x = 0
            #                 sum_y = 0
                                    
            #                 pos.x_pos = avg_pos_x
            #                 pos.y_pos = avg_pos_y
            #                 pos.door_width = avg_door_width
            #                 pos.send_data_flag = send_flag
            #                 door_pub.publish(pos)
            #                 send_flag = False
            #                 break             
            #         else:
            #             print(first_door_idx)
            #             print(second_door_idx)
            #             print(door_width)
            #             print("문요X")            


    elif mode == 3:
        # 라이다 225도 부터 시작
        for first_door_idx in range(225, 360):
            if first_door_idx == 359:
                break
            if lidar_ranges[first_door_idx + 1] > lidar_ranges[first_door_idx] + 1:
                for second_door in range(first_door_idx + 5, 360):
                    if second_door ==  359:
                        break
                    if lidar_ranges[second_door + 1] < lidar_ranges[second_door] - 0.8:
                        second_door_idx = second_door + 1
                                                    
                        # 문틀 폭 계산 함수
                        door_width = Calc_Door_Width(first_door_idx, second_door_idx, 1)
                        if door_width > 0.7 and door_width < 1.3:
                            is_door_cnt = is_door_cnt + 1
                                
                            scann.ranges = lidar_ranges
                            lidar_pub.publish(scann)


                            cor_first_door_idx, cor_second_door_idx = Open_Door_Filtering(first_door_idx, second_door_idx)
                            door_width = Calc_Door_Width(cor_first_door_idx, cor_second_door_idx, 1)
                            door_center_x, door_center_y  = Calc_Door_Pos(cor_first_door_idx, cor_second_door_idx, 3, door_width)    
                            
                            sum_x +=door_center_x
                            sum_y += door_center_y
                            sum_door += door_width
                            if is_door_cnt == 10:
                                avg_door_width = sum_door / 10
                                avg_pos_x = sum_x / 10
                                avg_pos_y = sum_y / 10
                                is_door_cnt = 0
                                sum_door = 0
                                sum_x = 0
                                sum_y = 0
                                
                                pos.x_pos = avg_pos_x
                                pos.y_pos = avg_pos_y
                                pos.door_width = avg_door_width
                                pos.send_data_flag = send_flag
                                pos.door_loc = 3
                                pos.door_sub_loc = 0
                                door_pub.publish(pos)
                                send_flag = False
                            
                            break     
                        else:
                            pass
                            #print("문X")
                            
                    
def Open_Door_Filtering(f_idx, s_idx):
    f_position = [[0 for j in range(2)] for i in range(60)]
    s_position = [[0 for j in range(2)] for i in range(60)]
    
    f_min_dist = []
    s_min_dist = []
    # 첫번째 문 틀부터 10도까지 감소된 지점의 좌표화
    for i in range(0, 60):
        if f_idx - i <= 0:
            break
        f_position[i][0] = -(lidar_ranges[f_idx - i] * math.sin(lidar_angle[f_idx - i]))
        f_position[i][1] = (lidar_ranges[f_idx - i] * math.cos(lidar_angle[f_idx - i]))

    # 두번째 문 틀부터 10도까지 증가된 지점의 좌표화
    for j in range(0, 60):
        if s_idx + j >= 360:
            break
        s_position[j][0] = -(lidar_ranges[s_idx + j] * math.sin(lidar_angle[s_idx + j]))
        s_position[j][1] = (lidar_ranges[s_idx + j] * math.cos(lidar_angle[s_idx + j]))

    # 첫번째 문 틀과 증가되는 두번째 문 틀의 직선거리 계산
    for k in range(0, 60):
        if s_position[k][0] == 0:
            break
        dist = math.sqrt( ( math.pow((f_position[0][0] - s_position[k][0]), 2) ) +  ( math.pow((f_position[0][1] - s_position[k][1]), 2)) ) 
        f_min_dist.append(dist)

    # 두번째 문 틀과 감소되는 첫번째 문 틀의 직선거리 계산
    for k in range(0, 60):
        if f_position[k][0] == 0:
            break
        dist = math.sqrt( ( math.pow((s_position[0][0] - f_position[k][0]), 2 ) ) +  ( math.pow((s_position[0][1] - f_position[k][1]), 2 )) ) 
        s_min_dist.append(dist)
    

    # 첫번째 문틀 기준으로 두번째 문틀을 보정
    if min(f_min_dist) <= min(s_min_dist):
        cor_s_idx = s_idx + f_min_dist.index(min(f_min_dist))
        return f_idx, cor_s_idx
    
    # 두번째 문틀 기준으로 첫번째 문틀을 보정
    else:
        cor_f_idx = f_idx - s_min_dist.index(min(s_min_dist))
        return cor_f_idx, s_idx    

    
def Calc_Door_Width(first_door_idx, second_door_idx, mode):
    first_len = lidar_ranges[first_door_idx]
    first_ang = lidar_angle[first_door_idx]
    second_len = lidar_ranges[second_door_idx]
    second_ang = lidar_angle[second_door_idx]
    
    
    # 문이 정면에 있지 않을 경우
    if mode == 1:
        Theta_rad = second_ang - first_ang
        Theta = (Theta_rad * 180)/ math.pi
            
        b = first_len
        c = second_len
        b2 = first_len*first_len
        c2 = second_len*second_len
            
        door_width2 = b2 + c2 - (2*b*c*(math.cos(Theta_rad)))
        door_width = math.sqrt(door_width2)

        #print('%.8f %.8f %.8f %.8f %.8f'%(b, c, second_ang, first_ang, door_width))
    
        return door_width
    
    # 문이 정면에 있을 경우
    if mode == 2:
        first_ang = 6.283185259 - first_ang              # 두번째 각도는 360도(6.283185259rad)에서 두번째각도를 빼야함
        
        #second_ang = 6.283185259 - second_ang              # 두번째 각도는 360도(6.283185259rad)에서 두번째각도를 빼야함
        Theta_rad = second_ang + first_ang
        Theta = (Theta_rad * 180)/ math.pi
            
        b = first_len
        c = second_len
        b2 = first_len*first_len
        c2 = second_len*second_len
            
        door_width2 = b2 + c2 - (2*b*c*(math.cos(Theta_rad)))
        door_width = math.sqrt(door_width2)

        return door_width


def Calc_Door_Pos(first_door_idx, second_door_idx, mode, door_width):
    first_len = lidar_ranges[first_door_idx]
    first_ang = lidar_angle[first_door_idx]
    second_len = lidar_ranges[second_door_idx]
    second_ang = lidar_angle[second_door_idx]

    # first_x_pos = -(first_len * math.sin(first_ang))
    # first_y_pos = (first_len * math.cos(first_ang))
    # second_x_pos = -(second_len * math.sin(second_ang))
    # second_y_pos = (second_len * math.cos(second_ang))

    # if mode == 0:
    #     center_x_pos = (first_x_pos + second_x_pos) / 2
    #     center_y_pos = first_y_pos

    # elif mode == 1:
    #     center_x_pos = second_x_pos
    #     center_y_pos = (first_y_pos + second_y_pos) / 2

    # elif mode == 2:
    #     center_x_pos = first_x_pos
    #     center_y_pos = (second_y_pos + first_y_pos) / 2    
    
    # return center_x_pos, center_y_pos

    # 좌표계 틀어졌을 때의 문의 좌표
    first_x_pos = (first_len * math.cos(first_ang))
    first_y_pos = (first_len * math.sin(first_ang))
    second_x_pos = (second_len * math.cos(second_ang))
    second_y_pos = (second_len * math.sin(second_ang))

    if mode == 1:
        center_x_pos = first_x_pos
        center_y_pos = (first_y_pos + second_y_pos) / 2
        
    elif mode == 2:
        center_x_pos = (first_x_pos + second_x_pos) / 2
        center_y_pos = second_y_pos
        
    elif mode == 3:
        center_x_pos = (second_x_pos + first_x_pos) / 2    
        center_y_pos = first_y_pos
        
    return center_x_pos, center_y_pos

    #print('%.8f %.8f %.8f %.8f %.8f'%(door_width, first_x_pos, first_y_pos, second_x_pos,second_y_pos))
    #print('%.8f %.8f %.8f'%(door_width, center_x_pos, center_y_pos))


def main():
    
    rospy.init_node('detect_door')

    laser_sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    service_server = rospy.Service('/door_service_scan', door_mode, door_modeCallback)

    rospy.spin()
    
    #rate = rospy.Rate(50)    # 10hz 0.1s
    #while not rospy.is_shutdown():
    #    lidar_pub.publish(lidar_ranges)
    #    rate.sleep()

if __name__ == '__main__':
    main()