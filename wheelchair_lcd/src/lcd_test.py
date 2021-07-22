#!/usr/bin/env python

import sys
import rospy
from Tkinter.font import *
from datetime import datetime
import Tkinter.messagebox
import time
import Tkinter as tk
from Tkinter import ttk
from Tkinter import *

from wheelchair_msg.msg import doormsg
from wheelchair_msg.srv import door_mode, door_modeRequest


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
        
        img = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/ModeSelect7.png') #이미지 읽고
        lbl = Label(self, image=img) #이미지 넣어
        lbl.image = img  # 레퍼런스 추가
        lbl.pack(padx=0, pady=0)    #위치
        
        button1 = tk.Button(self, text="일반/협응",font= ('Helvetica',11, 'bold'), bg = '#f6e5e2',width=30,command=lambda: controller.show_frame(Page1))
        button1.place(x= 360, y= 220)

        button2 = tk.Button(self, text="자율주행",font= ('Helvetica',11, 'bold') , bg = '#f6e5e2',width=30, command=lambda: controller.show_frame(Page4))
        button2.place(x= 360, y= 300)

        button3 = tk.Button(self, text="문 통과",font= ('Helvetica',11, 'bold') , bg = '#f6e5e2',width=30, command=lambda: controller.show_frame(Page5))
        button3.place(x= 360, y= 380)  

class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        img = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/ModeSelect7.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        button1 = tk.Button(self, text="일반 모드", font= ('Helvetica',11, 'bold'),bg = '#f6e5e2', width=30,command=lambda: controller.show_frame(Page2))
        button1.place(x= 360, y= 220)

        button2 = tk.Button(self, text="협응 모드", font= ('Helvetica',11, 'bold'),bg = '#f6e5e2', width=30, command=lambda: controller.show_frame(Page3))
        button2.place(x= 360, y= 300)

        button3 = tk.Button(self, text="뒤로 가기", font= ('Helvetica',11, 'bold'),bg = '#f6e5e2', width=30, command=lambda: controller.show_frame(StartPage))
        button3.place(x= 360, y= 380)  

class mode_stop():
    def __init__(self):
        tk.Tk.flag =0
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "Stop")

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/Page27.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page1))
        button1.image = btn_back
        button1.place(x= 590, y= 300)

        btn_play = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/play.png') 
        button2 = tk.Button(self, image=btn_play, command=nomal_mode)
        button2.image = btn_play
        button2.place(x= 390, y= 300)

        btn_stop = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/stop.png') 
        button3 = tk.Button(self, image=btn_stop,command=mode_stop)
        button3.image = btn_stop
        button3.place(x= 490, y= 300)

class nomal_mode():
    def __init__(self):
        tk.Tk.flag =1
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "일반모드\n주행 시작")

class Page3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/Page37.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page1))
        button1.image = btn_back
        button1.place(x= 590, y= 300)

        btn_play = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/play.png') 
        button2 = tk.Button(self, image=btn_play, command=coordination_mode)
        button2.image = btn_play
        button2.place(x= 390, y= 300)

        btn_stop = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/stop.png') 
        button3 = tk.Button(self, image=btn_stop,command=mode_stop)
        button3.image = btn_stop
        button3.place(x= 490, y= 300)

class coordination_mode():
    def __init__(self):
        tk.Tk.flag =2
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "협응모드\n주행 시작")
##################################################################################################################
class Page4(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/Page47.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        # button1 = ttk.Button(self, text="701", command = click_701)
        # button1.pack()

        button701 = tk.Button(self, text="701호", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page701))
        button701.place(x= 380, y= 220)
        button702 = tk.Button(self, text="702호", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page702))
        button702.place(x= 380, y= 270)
        button703 = tk.Button(self, text="703호", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page703))
        button703.place(x= 380, y= 320)
        button704 = tk.Button(self, text="704호", font= ('Helvetica',11, 'bold'),bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page704))
        button704.place(x= 380, y= 370)
        button705 = tk.Button(self, text="705호", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page705))
        button705.place(x= 380, y= 420)
        
        button706 = tk.Button(self, text="706호", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page706))
        button706.place(x= 550, y= 220)
        button707 = tk.Button(self, text="707호", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page707))
        button707.place(x= 550, y= 270)
        button708 = tk.Button(self, text="708호", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page708))
        button708.place(x= 550, y= 320)
        button708 = tk.Button(self, text="709호", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(Page709))
        button708.place(x= 550, y= 370)

        buttonback = tk.Button(self, text="뒤로 가기", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=lambda: controller.show_frame(StartPage))
        buttonback.place(x= 550, y= 420)

class Page701(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/7017.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 590, y= 300)

        btn_play = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_701_mode)
        button2.image = btn_play
        button2.place(x= 390, y= 300)

        btn_stop = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/stop.png') 
        button3 = tk.Button(self, image=btn_stop,command=mode_stop)
        button3.image = btn_stop
        button3.place(x= 490, y= 300)
        
class go_701_mode():
    def __init__(self):
        tk.Tk.flag =701
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "701호\n주행 시작")

class Page702(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/7027.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 590, y= 300)

        btn_play = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_702_mode)
        button2.image = btn_play
        button2.place(x= 390, y= 300)

        btn_stop = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/stop.png') 
        button3 = tk.Button(self, image=btn_stop,command=mode_stop)
        button3.image = btn_stop
        button3.place(x= 490, y= 300)

class go_702_mode():
    def __init__(self):
        tk.Tk.flag =702
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "702호\n주행 시작")

class Page703(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/7037.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 590, y= 300)

        btn_play = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_703_mode)
        button2.image = btn_play
        button2.place(x= 390, y= 300)

        btn_stop = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/stop.png') 
        button3 = tk.Button(self, image=btn_stop,command=mode_stop)
        button3.image = btn_stop
        button3.place(x= 490, y= 300)

class go_703_mode():
    def __init__(self):
        tk.Tk.flag =703
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "703호\n주행 시작")

class Page704(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/7047.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 590, y= 300)

        btn_play = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_704_mode)
        button2.image = btn_play
        button2.place(x= 390, y= 300)

        btn_stop = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/stop.png') 
        button3 = tk.Button(self, image=btn_stop,command=mode_stop)
        button3.image = btn_stop
        button3.place(x= 490, y= 300)

class go_704_mode():
    def __init__(self):
        tk.Tk.flag =704
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "704호\n주행 시작")

class Page705(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/7057.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 590, y= 300)

        btn_play = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_705_mode)
        button2.image = btn_play
        button2.place(x= 390, y= 300)

        btn_stop = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/stop.png') 
        button3 = tk.Button(self, image=btn_stop,command=mode_stop)
        button3.image = btn_stop
        button3.place(x= 490, y= 300)

class go_705_mode():
    def __init__(self):
        tk.Tk.flag =705
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "705호\n주행 시작")

class Page706(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/7067.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 590, y= 300)

        btn_play = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_706_mode)
        button2.image = btn_play
        button2.place(x= 390, y= 300)

        btn_stop = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/stop.png') 
        button3 = tk.Button(self, image=btn_stop,command=mode_stop)
        button3.image = btn_stop
        button3.place(x= 490, y= 300)

class go_706_mode():
    def __init__(self):
        tk.Tk.flag =706
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "706호\n주행 시작")

class Page707(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/7077.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 590, y= 300)

        btn_play = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_707_mode)
        button2.image = btn_play
        button2.place(x= 390, y= 300)

        btn_stop = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/stop.png') 
        button3 = tk.Button(self, image=btn_stop,command=mode_stop)
        button3.image = btn_stop
        button3.place(x= 490, y= 300)

class go_707_mode():
    def __init__(self):
        tk.Tk.flag =707
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "707호\n주행 시작") 

class Page708(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/7087.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 590, y= 300)

        btn_play = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_708_mode)
        button2.image = btn_play
        button2.place(x= 390, y= 300)

        btn_stop = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/stop.png') 
        button3 = tk.Button(self, image=btn_stop,command=mode_stop)
        button3.image = btn_stop
        button3.place(x= 490, y= 300)

class go_708_mode():
    def __init__(self):
        tk.Tk.flag =708
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "708호\n주행 시작")

class Page709(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/7097.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        btn_back = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/back.png') 
        button1 = tk.Button(self, image=btn_back, command=lambda: controller.show_frame(Page4))
        button1.image = btn_back
        button1.place(x= 590, y= 300)

        btn_play = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/play.png') 
        button2 = tk.Button(self, image=btn_play, command=go_709_mode)
        button2.image = btn_play
        button2.place(x= 390, y= 300)

        btn_stop = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/stop.png') 
        button3 = tk.Button(self, image=btn_stop,command=mode_stop)
        button3.image = btn_stop
        button3.place(x= 490, y= 300)

class go_709_mode():
    def __init__(self):
        tk.Tk.flag =709
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "709호\n주행 시작")

class Page5(tk.Frame):
    def __init__(self, parent, controller):
        tk.Tk.flag =0
        tk.Frame.__init__(self, parent)
        img = PhotoImage(file='/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_lcd/image/Page57.png') 
        lbl = Label(self, image=img)
        lbl.image = img
        lbl.pack(padx=0, pady=0)

        button1 = tk.Button(self, text="왼쪽",font= ('Helvetica',11, 'bold'), bg = '#f6e5e2',  width=9,command=click_L)
        button1.place(x= 315, y= 290)

        button2 = tk.Button(self, text="앞쪽", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9,command=click_F)
        button2.place(x= 470, y= 210)

        button3 = tk.Button(self, text="중간", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9, command=click_M)
        button3.place(x= 470, y= 290)

        button4 = tk.Button(self, text="오른쪽", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9, command=click_R)
        button4.place(x= 630, y= 290)

        button5 = tk.Button(self, text="뒤로 가기", font= ('Helvetica',11, 'bold'), bg = '#f6e5e2', width=9, command=lambda: controller.show_frame(StartPage))
        button5.place(x= 470, y= 370) 

class click_L():
    def __init__(self):
        tk.Tk.flag =7
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "왼쪽 선택")
class click_F():
    def __init__(self):
        tk.Tk.flag =8
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "앞쪽 선택")
class click_M():
    def __init__(self):
        tk.Tk.flag =9
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "중간 선택")
class click_R():
    def __init__(self):
        tk.Tk.flag =0
        print(tk.Tk.flag)
        msg = tkinter.messagebox.showinfo("정보 메시지", "오른쪽 선택")

app=wheelchairapp()

rospy.wait_for_service('/door_service_scan')
door_client = rospy.ServiceProxy('/door_service_scan',door_mode)
door_request_srv = door_modeRequest()

rospy.init_node('wheelchar_lcd', anonymous=True)
app.mainloop()