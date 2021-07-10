#include <ros.h>
//DMD1K 모터드라이버 RS485 통신 패킷
#include "MDseries.h"
#include <std_msgs/Int32.h>
#include <geometry_msgs/Twist.h>

//@brief : 조이스틱 설정
#define X   A0
#define Y   A1
#define DEADZONE 200

//#define RS485_T   C10
//#define RS485_R   C11

//@brief : 휠체어 플랫폼 기구에 대한 정보
#define LENGTH_BET_WHEEL    0.52     // 바퀴 축 간의 거리 - (휠체어)52.0cm = 0.52m, (모바일로봇)28.1cm = 0.281m
#define WHEEL_RADIUS        0.1755     // 바퀴의 반지름 길이 - (휠체어)17.55cm = 0.1755m, (모바일로봇)6.25cm = 0.0625m

//@brief : Trapezoid Velocity Profile
#define T_COUNT 10000                // in microseconds; interrupts every 0.001 sec 
#define V_MAX 1890               // Vmax - 최대 RPM 값
#define ACCELERATION 550         // 가속도 = 0.825m/s^2 -> 945rpm

//@brief : 엔코더 A, B 핀 설정
#define ENCO_A_L   2   
#define ENCO_B_L   3
#define ENCO_A_R   7
#define ENCO_B_R   8

#define PPR 151200      //PPR - Pulse Per Revolution

HardwareTimer Timer1(TIMER_CH1);
HardwareTimer Timer2(TIMER_CH3);

//@brief : 휠체어 속도 
//@explain : - lmotor_speed & rmotor_speed : 조이스틱으로부터 선속도, 각속도를 계산하여 나타낸 값 
//           - lmotor_rpm & rmotor_rpm : 최종적으로 송신 될 속도(데이터)값
int lmotor_speed = 0;
int rmotor_speed = 0;
int lmotor_rpm = 0;
int rmotor_rpm = 0;


//@brief : Trapezoid Velocity Profile에서 초를 나타냄 (Timer Interrupt)
float l_acc_sec = 0;                 
float r_acc_sec = 0;

//@brief : 가감속 제어 함수에 사용되는 변수
//@explain : - lspeed_data_rpm & rspeed_data_rpm : Acc_Deceleration(가감속 제어 함수)에서 사용되는 변수
//           - l_init_speed & r_init_speed : Acc_Deceleration(가감속 제어 함수)에서 사용되는 변수
//           - l_flag & r_flag & left_motor_flag & right_motor_flag : 왼쪽, 오른쪽 모터에 대한 플래그 값
float lspeed_data_rpm = 0;
float rspeed_data_rpm = 0;
int l_init_speed = 0;
int r_init_speed = 0; 
char l_flag = 0;
char r_flag = 0;
char left_motor_flag = 0;
char right_motor_flag = 0;


int a_lmotor_rpm = 0;
int a_rmotor_rpm = 0;
int vl_sd = 0;
int vr_sd = 0;


//@brief : 엔코더 펄스 받을 변수
int enco_r = 0;
int enco_l = 0;

float r_rpm = 0;
float l_rpm = 0;

double vx = 0;
double vth = 0;


//@brief : 자율주행 ON flag
char autonomous_mode = 0;
  
ros::NodeHandle nh;


void cmdvelcallback(const geometry_msgs::Twist& msg)
{
  vx = msg.linear.x;
  vth = msg.angular.z;

  Autonomous_Drive(vx, vth);
}

std_msgs::Int32 lencoder;
std_msgs::Int32 rencoder;

//odom_mobilerobot::encpulse encoder_msg;
ros::Publisher pub_lencoder("encoder_lpulse", &lencoder);
ros::Publisher pub_rencoder("encoder_rpulse", &rencoder);
ros::Subscriber<geometry_msgs::Twist>wheelchair_vel("/cmd_vel",cmdvelcallback);

void setup() {
  Serial.begin(115200);   //COM과 통신속도
  Serial1.begin(115200);  //DMD1K 모터드라이버와의 통신속도
  analogReadResolution(12);  //ADC 12bit resolution

  nh.initNode();
  nh.advertise(pub_lencoder);
  nh.advertise(pub_rencoder);
  nh.subscribe(wheelchair_vel); 

  //인터럽트 Input 설정
  pinMode(2,INPUT_PULLDOWN);
  pinMode(3,INPUT_PULLDOWN);
  pinMode(7,INPUT_PULLDOWN);
  pinMode(8,INPUT_PULLDOWN);
  
  //인터럽트 3,4번 설정
  attachInterrupt(0, Encoder_A_L, RISING);
  attachInterrupt(1, Encoder_B_L, RISING);
  attachInterrupt(3, Encoder_A_R, RISING);
  attachInterrupt(4, Encoder_B_R, RISING);

  //타이머 초기설정 및 시작
  Timer1_Init();
  Timer2_Init();
    
}

void loop() {
//  int x,y;

  nh.spinOnce();

  if(autonomous_mode)
  {
    
  left_motor_flag = 1, right_motor_flag = 0;
  a_lmotor_rpm = Acc_Deceleration(&vl_sd);
  left_motor_flag = 0, right_motor_flag = 1;
  a_rmotor_rpm = Acc_Deceleration(&vr_sd);


  MD_Packet(183,184,1,130,2,a_lmotor_rpm);
  delay(0.2);
  MD_Packet(183,184,2,130,2,a_rmotor_rpm);
  delay(0.2);
  }
  
  
  
//  x=analogRead(X);
//  y=analogRead(Y);
//  
//  Joystick_Value(x,y,&lmotor_speed,&rmotor_speed);
//  Joystick_Control(&lmotor_speed,&rmotor_speed);
}

void Timer1_Init()
{
  Timer1.stop();
  Timer1.setPeriod(T_COUNT);           // in microseconds
  Timer1.attachInterrupt(handler_T);
  Timer1.start();
}


void Timer2_Init()
{
  Timer2.stop();
  Timer2.setPeriod(33000);           // in microseconds
  Timer2.attachInterrupt(enco_timer);
  Timer2.start();
}


//@brief : Timer Interrupt
void handler_T(void) 
{
  l_acc_sec += 0.01;
  r_acc_sec += 0.01;   
}


//@brief : 0.033초마다 갱신되는 엔코더 펄스 개수
void enco_timer(void)
{

  lencoder.data = enco_l;
  rencoder.data = enco_r;

  pub_lencoder.publish(&lencoder);
  pub_rencoder.publish(&rencoder);
  
  /*
  r_rpm = (60*enco_r)/((0.033)*PPR);
  l_rpm = (60*enco_l)/((0.033)*PPR);
  
  Serial.print("R : ");
  Serial.print(r_rpm);
  Serial.print("  L : ");
  Serial.println(l_rpm);
  */

  enco_r = 0;
  enco_l = 0;
}


void Encoder_A_R()
{
  if(digitalRead(ENCO_B_R)==0){enco_r--;}
  else if(digitalRead(ENCO_B_R)==1){enco_r++;}
}

void Encoder_B_R()
{
  if(digitalRead(ENCO_A_R)==0){enco_r++;}
  else if(digitalRead(ENCO_A_R)==1){enco_r--;}
}

void Encoder_A_L()
{
  if(digitalRead(ENCO_B_L)==0){enco_l--;}
  else if(digitalRead(ENCO_B_L)==1){enco_l++;}
}

void Encoder_B_L()
{
  if(digitalRead(ENCO_A_L)==0){enco_l++;}
  else if(digitalRead(ENCO_A_L)==1){enco_l--;}
}


//@brief : 가감속 제어
//@explain : - v_desire : 목표속도
//           - ACCELERATION : 가속도 값
//           - acc_sec : at = v에 사용되는 t값
//@ATTENTION : 본 함수에서 직진은 (-), 후진은 (+)으로 설정되어있음
int Acc_Deceleration(int* v_desire)
{
  //LEFT MOTOR
  if(left_motor_flag)
  {
    if(lspeed_data_rpm > (*v_desire)) 
    {
      if(!l_flag) {l_init_speed = lspeed_data_rpm; l_acc_sec = 0; l_flag = ~l_flag;}
      lspeed_data_rpm = l_init_speed - (ACCELERATION * l_acc_sec);
    } 
    else if(lspeed_data_rpm < (*v_desire)) 
    {
      if(l_flag) {l_init_speed = lspeed_data_rpm; l_acc_sec = 0; l_flag = ~l_flag;}
      lspeed_data_rpm = l_init_speed + (ACCELERATION * l_acc_sec);
    }

    if(lspeed_data_rpm == *v_desire) {lspeed_data_rpm = *v_desire; l_acc_sec = 0;}

    if(*v_desire==0)
    {
      if((lspeed_data_rpm>-83)&&(lspeed_data_rpm<83)) {lspeed_data_rpm = *v_desire; l_init_speed = 0;}
    }
   // Serial.println(lspeed_data_rpm);
    
    return lspeed_data_rpm;
  }

  //RIGHT MOTOR
  if(right_motor_flag)
  {
    if(rspeed_data_rpm > (*v_desire)) 
    {
      if(!r_flag) {r_init_speed = rspeed_data_rpm; r_acc_sec = 0; r_flag = ~r_flag;}
      rspeed_data_rpm = r_init_speed - (ACCELERATION * r_acc_sec);
  //  Serial.println(acc_sec);
    } 
    else if(rspeed_data_rpm < (*v_desire)) 
    {
      if(r_flag) {r_init_speed = rspeed_data_rpm; r_acc_sec = 0; r_flag = ~r_flag;}
    // Serial.println(acc_sec);
      rspeed_data_rpm = r_init_speed + (ACCELERATION * r_acc_sec);
    }

    if(rspeed_data_rpm == *v_desire) {rspeed_data_rpm = *v_desire; r_acc_sec = 0;}

    if(*v_desire==0)
    {
      if((rspeed_data_rpm>-83)&&(rspeed_data_rpm<83)) {rspeed_data_rpm = *v_desire; r_init_speed = 0;}
    }
    return rspeed_data_rpm;
  }
//  if(speed_data_rpm <= -1890) speed_data_rpm = -V_MAX;
//  else if(speed_data_rpm >= 1890) speed_data_rpm = V_MAX;
}


//@brief : 단위 변환 함수
float Unit_Convert(float input, int unit)
{   
    float output = 0;         
    
    switch(unit)
    {
        case 1 :
        //degree to radian
        output = (input)*(0.0055556)*PI;          
        break;        
        
        case 2 :
        //radian to degree
        output = ((input)*180)/PI;
        break;      
        
        case 3 :
        //RPM to m/s
        output = WHEEL_RADIUS*((2*PI)/60)*(input);
        break;      
        
        case 4 :
        //m/s to RPM
        output = ((input)*60)/(2*PI*WHEEL_RADIUS);
        break;        
                                       
        case 5 :
        //RPM to speed data
        output = (input)*21;
        break;
    }   
    return output;            
}

//@brief : 협응주행 함수
void Autonomous_Drive(float velocity, float angular_velocity)
{
  float v = 0;
  float av = 0;
  float vl_ms = 0;     // ms : m/s
  float vr_ms = 0;
  int vl_rpm = 0;
  int vr_rpm = 0;
  //int vl_sd = 0;       // sd : speed data
  //int vr_sd = 0;  

  autonomous_mode = 1;

  
  v = velocity;             // 속도의 단위는 m/s
  av = angular_velocity;    // 각속도의 단위는 rad/s
  vl_ms = v;
  vr_ms = v;

  vl_ms = -(vl_ms - (av*LENGTH_BET_WHEEL/4));
  vr_ms = -(vr_ms + (av*LENGTH_BET_WHEEL/4));

  vl_rpm = Unit_Convert(vl_ms, 4);
  vr_rpm = Unit_Convert(vr_ms, 4);
  vl_sd = Unit_Convert(vl_rpm, 5);
  vr_sd = Unit_Convert(vr_rpm, 5);


  /*
  left_motor_flag = 1, right_motor_flag = 0;
  a_lmotor_rpm = Acc_Deceleration(&vl_sd);
  left_motor_flag = 0, right_motor_flag = 1;
  a_rmotor_rpm = Acc_Deceleration(&vr_sd);


  MD_Packet(183,184,1,130,2,a_lmotor_rpm);
  delay(0.2);
  MD_Packet(183,184,2,130,2,a_rmotor_rpm);
  delay(0.2);*/
}


//@brief : Joystick 값 처리 함수
void Joystick_Value(int x, int y, int* lmotor_speed, int* rmotor_speed)
{
  int j_x = x-2069;
  int j_y = y-2060;
 
  if(j_y >= 1850) {j_y = 1260;}              //200보다 크거나 -200보다 작을 때 최소 속도 구동, 1850보다 크면 최대값으로 고정
  else if(j_y >= DEADZONE && j_y < 1850) {j_y = (0.713*j_y)-58.6;}
  else if(j_y < DEADZONE && j_y > -DEADZONE) {j_y = 0;}
  else if(j_y <= -DEADZONE && j_y > -1850) {j_y = (0.713*j_y)+58.6;}
  else if(j_y <= -1850) {j_y = -1260;}

  if(j_x >= 1850) {j_x = 1260;}              //200보다 크거나 -200보다 작을 때 최소 속도 구동, 1850보다 크면 최대값으로 고정
  else if(j_x >= DEADZONE && j_x < 1850) {j_x = (0.713*j_x)-58.6;}
  else if(j_x < DEADZONE && j_x > -DEADZONE) {j_x = 0;}
  else if(j_x <= -DEADZONE && j_x > -1850) {j_x = (0.713*j_x)+58.6;}
  else if(j_x <= -1850) {j_x = -1260;}
  
  
  *lmotor_speed = -(j_y + ((j_x*LENGTH_BET_WHEEL)/4));
  *rmotor_speed = -(j_y - ((j_x*LENGTH_BET_WHEEL)/4));
  
 // Serial.println(*lmotor_speed);
}


//@brief : 최종적으로 보내지는 속도 값 함수
void Joystick_Control(int* lmotor_speed, int* rmotor_speed)
{ 
  left_motor_flag = 1, right_motor_flag = 0;
  lmotor_rpm = Acc_Deceleration(lmotor_speed);
  left_motor_flag = 0, right_motor_flag = 1;
  rmotor_rpm = Acc_Deceleration(rmotor_speed);

  
  if(!((lmotor_rpm==0)&&(rmotor_rpm==0)))
  {
    MD_Packet(183,184,1,130,2,lmotor_rpm);
    delay(0.2);
    MD_Packet(183,184,2,130,2,rmotor_rpm);
    delay(0.2);
  } else if((((*lmotor_speed==0)&&(*rmotor_speed==0))&&((lmotor_rpm==0)&&(rmotor_rpm==0))))
  { 
    MD_Packet(183,184,2,5,1,1);
    delay(0.2);
    MD_Packet(183,184,1,5,1,1);
    delay(0.2);
  }
}

unsigned short CRC16(char *puchMsg, int usDataLen)
{
  int i;
  unsigned short crc, flag;
  crc = 0xffff;

  while(usDataLen--){
    crc ^= *puchMsg++;

    for(i=0;i<8;i++)
    {
       flag = crc & 0x0001;
       crc >>= 1;
       if(flag) crc ^= 0xA001;
    }
  }
  return crc;
}
