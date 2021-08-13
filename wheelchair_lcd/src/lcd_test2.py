#!/usr/bin/env python3

import sys
import rospy
from tkinter.font import *
from datetime import datetime
import tkinter.messagebox
import time
import tkinter as tk
from tkinter import ttk
from tkinter import *

from wheelchair_msg.msg import doormsg
from wheelchair_msg.srv import door_mode, door_modeRequest
from wheelchair_msg.srv import normal_mode, normal_modeRequest
from wheelchair_msg.srv import coop_mode, coop_modeRequest


tk.Tk.flag =0

class wheelchairapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="")
        container = tk.Frame(self)
        container.pack(side = "top", fill="both", expand= True)
        container.grid_rowconfigure(1000, weight=1000)
        container.grid_columnconfigure(1000, weight=1000)
        
        self.frames = {}
        for F in (StartPage, Page1, Page2, Page3, Page4, Page5,   Page701, Page702, Page703, Page704, Page705, Page706, Page707, Page708, Page709) :
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=1000, column=1000, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        img = PhotoImage(file='ModeSelect77.png') 
        lbl = Label(self, image=img) 
        lbl.image = img 
        lbl.pack(padx=0, pady=0)
        
        button1 = tk.Button(self, text="일반/협응",font= ('Helvetica',11, 'bold'), bg = '#f6e5e2',width=30,command=lambda: controller.show_frame(Page1))
        button1.place(x= 110, y= 220)

        button2 = tk.Button(self, text="자율주행",font= ('Helvetica',11, 'bold') , bg = '#f6e5e2',width=30, command=lambda: controller.show_frame(Page4))
        button2.place(x= 110, y= 400)

        button3 = tk.Button(self, text="문 통과",font= ('Helvetica',11, 'bold') , bg = '#f6e5e2',width=30, command=lambda: controller.show_frame(Page5))
        button3.place(x= 110, y= 580)  

class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        img = PhotoImage(file='ModeSelect77.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        button1 = tk.Button(self, text="일반 모드", font= ('Helvetica',11, 'bold'),bg = '#f6e5e2', width=30,command=lambda: controller.show_frame(Page2))
        button1.place(x= 110, y= 220)

        button2 = tk.Button(self, text="협응 모드", font= ('Helvetica',11, 'bold'),bg = '#f6e5e2', width=30, command=lambda: controller.show_frame(Page3))
        button2.place(x= 110, y= 400)

        button3 = tk.Button(self, text="뒤로 가기", font= ('Helvetica',11, 'bold'),bg = '#f6e5e2', width=30, command=lambda: controller.show_frame(StartPage))
        button3.place(x= 110, y= 580)  

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = PhotoImage(file='Page277.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page1))
        button1.image = btn_back
        button1.place(x= 300, y= 350)

        btn_play = PhotoImage(file='play.png') 
        button2 = tk.Button(self, image=btn_play, command=nomal_mode)
        button2.image = btn_play
        button2.place(x= 160, y= 350)

class nomal_mode():
    def __init__(self):
        normal_request_srv.normal_mode_start_req =  True
        result = normal_client(normal_request_srv)
        if result.normal_mode_start_res == True:
            msg = tkinter.messagebox.showinfo("정보 메시지", "일반모드 주행")
        else:
            msg = tkinter.messagebox.showinfo("정보 메시지", "모드변경불가")###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 오른쪽 문통과 코드 기입 ######

        ###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 일반모드 코드 기입 ######

class Page3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='Page377.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page1))
        button1.image = btn_back
        button1.place(x= 300, y= 350)

        btn_play = PhotoImage(file='play.png') 
        button2 = tk.Button(self, image=btn_play, command=coordination_mode)
        button2.image = btn_play
        button2.place(x= 160, y= 350)

class coordination_mode():
    def __init__(self):
        coop_request_srv.coop_mode_start_req =  True
        result = coop_client(coop_request_srv)
        if result.coop_mode_start_res == True:
            msg = tkinter.messagebox.showinfo("정보 메시지", "협응모드 주행")
        else:
            msg = tkinter.messagebox.showinfo("정보 메시지", "모드변경불가")###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 오른쪽 문통과 코드 기입 ######
        ###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 협응모드 코드 기입 ######
        
class Page4(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='Page477.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        button701 = tk.Button(self, text="701호", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page701))
        button701.place(x= 140, y= 220)
        button702 = tk.Button(self, text="702호", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page702))
        button702.place(x= 140, y= 320)
        button703 = tk.Button(self, text="703호", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page703))
        button703.place(x= 140, y= 420)
        button704 = tk.Button(self, text="704호", font= ('Helvetica',11, 'bold'),bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page704))
        button704.place(x= 140, y= 520)
        button705 = tk.Button(self, text="705호", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page705))
        button705.place(x= 140, y= 620)
        
        button706 = tk.Button(self, text="706호", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page706))
        button706.place(x= 270, y= 220)
        button707 = tk.Button(self, text="707호", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page707))
        button707.place(x= 270, y= 320)
        button708 = tk.Button(self, text="708호", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page708))
        button708.place(x= 270, y= 420)
        button708 = tk.Button(self, text="709호", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page709))
        button708.place(x= 270, y= 520)

        buttonback = tk.Button(self, text="뒤로 가기", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(StartPage))
        buttonback.place(x= 270, y= 620)

class Page701(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='70177.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 300, y= 350)

        btn_play = PhotoImage(file='play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_701_mode)
        button2.image = btn_play
        button2.place(x= 160, y= 350)
        
class go_701_mode():
    def __init__(self):
        tk.Tk.flag =701
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "701호\n주행 시작")
        ###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 701호 자율주행 코드 기입 ######

class Page702(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='70277.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 300, y= 350)

        btn_play = PhotoImage(file='play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_702_mode)
        button2.image = btn_play
        button2.place(x= 160, y= 350)

class go_702_mode():
    def __init__(self):
        tk.Tk.flag =702
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "702호\n주행 시작")
        ###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 702호 자율주행 코드 기입 ######

class Page703(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='70377.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 300, y= 350)

        btn_play = PhotoImage(file='play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_703_mode)
        button2.image = btn_play
        button2.place(x= 160, y= 350)

class go_703_mode():
    def __init__(self):
        tk.Tk.flag =703
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "703호\n주행 시작")
        ###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 703호 자율주행 코드 기입 ######

class Page704(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='70477.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 300, y= 350)

        btn_play = PhotoImage(file='play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_704_mode)
        button2.image = btn_play
        button2.place(x= 160, y= 350)

class go_704_mode():
    def __init__(self):
        tk.Tk.flag =704
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "704호\n주행 시작")
        ###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 704호 자율주행 코드 기입 ######

class Page705(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='70577.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 300, y= 350)

        btn_play = PhotoImage(file='play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_705_mode)
        button2.image = btn_play
        button2.place(x= 160, y= 350)

class go_705_mode():
    def __init__(self):
        tk.Tk.flag =705
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "705호\n주행 시작")
        ###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 705호 자율주행 코드 기입 ######

class Page706(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='70677.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 300, y= 350)

        btn_play = PhotoImage(file='play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_706_mode)
        button2.image = btn_play
        button2.place(x= 160, y= 350)

class go_706_mode():
    def __init__(self):
        tk.Tk.flag =706
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "706호\n주행 시작")
        ###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 706호 자율주행 코드 기입 ######

class Page707(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='70777.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 300, y= 350)

        btn_play = PhotoImage(file='play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_707_mode)
        button2.image = btn_play
        button2.place(x= 160, y= 350)

class go_707_mode():
    def __init__(self):
        tk.Tk.flag =707
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "707호\n주행 시작")
        ###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 707호 자율주행 코드 기입 ###### 

class Page708(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='70877.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 300, y= 350)

        btn_play = PhotoImage(file='play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_708_mode)
        button2.image = btn_play
        button2.place(x= 160, y= 350)

class go_708_mode():
    def __init__(self):
        tk.Tk.flag =708
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "708호\n주행 시작")
        ###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 708호 자율주행 코드 기입 ######

class Page709(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='70977.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 300, y= 350)

        btn_play = PhotoImage(file='play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_709_mode)
        button2.image = btn_play
        button2.place(x= 160, y= 350)

class go_709_mode():
    def __init__(self):
        tk.Tk.flag =709
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "709호\n주행 시작")
        ###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 709호 자율주행 코드 기입 ######

class Page5(tk.Frame):
    def __init__(self, parent, controller):
        tk.Tk.flag =0
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='Page577.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        button1 = tk.Button(self, text="왼쪽",font= ('Helvetica',11, 'bold'), bg = '#f6e5e2',  width=9,command=click_L)
        button1.place(x= 50, y= 400)

        button2 = tk.Button(self, text="정면", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=click_F)
        button2.place(x= 205, y= 290)

        button6 = tk.Button(self, text="정면왼쪽", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=click_FL)
        button6.place(x= 50, y= 290)

        button7 = tk.Button(self, text="정면오른쪽", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=click_FR)
        button7.place(x= 365, y= 290)

        button3 = tk.Button(self, text="중간", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9, command=click_M)
        button3.place(x= 205, y= 400)

        button4 = tk.Button(self, text="오른쪽", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9, command=click_R)
        button4.place(x= 365, y= 400)

        button5 = tk.Button(self, text="뒤로 가기", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9, command=lambda: controller.show_frame(StartPage))
        button5.place(x= 205, y= 510) 

class click_L():
    def __init__(self):
        door_request_srv.door_req_flag =  True
        door_request_srv.door_mode = 2
        door_request_srv.sub_door_mode = 0
        result = door_client(door_request_srv)
        if result.door_res_flag == True:
            msg = tkinter.messagebox.showinfo("정보 메시지", "왼쪽 선택")
        else:
            msg = tkinter.messagebox.showinfo("정보 메시지", "문 통과불가")
        ###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 왼쪽 문통과 코드 기입 ######

class click_F():
    def __init__(self):
        door_request_srv.door_req_flag =  True
        door_request_srv.door_mode = 1
        door_request_srv.sub_door_mode = 3
        result = door_client(door_request_srv)
        if result.door_res_flag == True:
            msg = tkinter.messagebox.showinfo("정보 메시지", "정면 선택")
        else:
            msg = tkinter.messagebox.showinfo("정보 메시지", "문 통과불가")
        ###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 정면 문통과 코드 기입 ######

class click_FL():
    def __init__(self):
        door_request_srv.door_req_flag =  True
        door_request_srv.door_mode = 1
        door_request_srv.sub_door_mode = 1
        result = door_client(door_request_srv)
        if result.door_res_flag == True:
            msg = tkinter.messagebox.showinfo("정보 메시지", "정면왼쪽 선택")
        else:
            msg = tkinter.messagebox.showinfo("정보 메시지", "문 통과불가")
        ###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 정면왼쪽 문통과 코드 기입 ######

class click_FR():
    def __init__(self):
        door_request_srv.door_req_flag =  True
        door_request_srv.door_mode = 1
        door_request_srv.sub_door_mode = 2
        result = door_client(door_request_srv)
        if result.door_res_flag == True:
            msg = tkinter.messagebox.showinfo("정보 메시지", "정면오른쪽 선택")
        else:
            msg = tkinter.messagebox.showinfo("정보 메시지", "문 통과불가")
        ###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 정면오른쪽 문통과 코드 기입 ######


class click_M():
    def __init__(self):
        tk.Tk.flag =9
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "중간 선택")
        ###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 중간 문통과 코드 기입 ######

class click_R():
    def __init__(self):
        door_request_srv.door_req_flag =  True
        door_request_srv.door_mode = 3
        door_request_srv.sub_door_mode = 0
        result = door_client(door_request_srv)
        if result.door_res_flag == True:
            msg = tkinter.messagebox.showinfo("정보 메시지", "오른쪽 선택")
        else:
            msg = tkinter.messagebox.showinfo("정보 메시지", "문 통과불가")###### tk.Tk.flag 부터 msg 라인 까지 삭제 후 오른쪽 문통과 코드 기입 ######

app=wheelchairapp()

rospy.wait_for_service('/door_service_scan')
door_client = rospy.ServiceProxy('/door_service_scan',door_mode)
door_request_srv = door_modeRequest()

rospy.wait_for_service('/normal_mode_service')
normal_client = rospy.ServiceProxy('/normal_mode_service',normal_mode)
normal_request_srv = normal_modeRequest()

rospy.wait_for_service('/coop_mode_service')
coop_client = rospy.ServiceProxy('/coop_mode_service',coop_mode)
coop_request_srv = coop_modeRequest()

rospy.init_node('wheelchar_lcd', anonymous=True)

app.mainloop()