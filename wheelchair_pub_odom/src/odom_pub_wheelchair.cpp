#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include <std_msgs/Int32.h>
#include "wc_encoder.h"

int lpulse = 0, rpulse = 0;
int PPR = 151200;   // 21(모터기어비) * 7200(엔코더tick)
double Tc = 0.02;

void lencoderCallback(const std_msgs::Int32::ConstPtr& msg)
{
    lpulse = msg->data;
    
}

void rencoderCallback(const std_msgs::Int32::ConstPtr& msg)
{
    rpulse = msg->data; 
}


int main(int argc, char** argv)
{
    ros::init(argc,argv,"wheelchair_odometry_pub");

    ros::NodeHandle nh;
    ros::Publisher odom_pub = nh.advertise<nav_msgs::Odometry>("odom",10);
    ros::Subscriber lencoder_sub = nh.subscribe("encoder_lpulse", 10, lencoderCallback);
    ros::Subscriber rencoder_sub = nh.subscribe("encoder_rpulse", 10, rencoderCallback);
    
    tf::TransformBroadcaster odom_broadcaster;

    ENCODER encoder;     // encoder instance
    HEELVEL hlv;         // encoder struct


    double x = 0.0;
    double y = 0.0;
    double th = 0.0;

    

    double vx = 0.0;
    double vy = 0.0;
    double vth = 0.0;

    ros::Time current_time, last_time;
    current_time = ros::Time::now();
    last_time = ros::Time::now();

    //ros::Rate r(50);
    ros::Rate r(30);
    while(nh.ok())
    {
        ros::spinOnce();
        
        current_time = ros::Time::now();
        // 0.02s 주기마다 홀센서 펄스 받기, dt = 0.02s
        double dt = (current_time - last_time).toSec();
        
        // 엔코더 값 Subscribe 후 속도값 변환
        encoder.UpdateEncoder(lpulse, rpulse, dt ,PPR);
        // 엔코더 값 속도 변환 M 방법 사용
        
        hlv = encoder.SubVelocity();
        
        // 선속도, 각속도
        double vx = ( hlv.l_heel_vel + hlv.r_heel_vel ) / 2;   // m/s
        double vy = 0.0;                                       // m/s
        double vth = ( hlv.l_heel_vel - hlv.r_heel_vel ) / lengthBetweenWheels;    // 1/s
        
        double delta_x = (vx * cos(th)) * dt;     // m
        double delta_y = (vx * sin(th)) * dt;     // m
        double delta_th = vth * dt;               // 단위 x

        x += delta_x;
        y += delta_y;
        th += delta_th;
        //ROS_INFO("x: %.3lf", x);
        //ROS_INFO("y: %.3lf", y);
        geometry_msgs::Quaternion odom_quat = tf::createQuaternionMsgFromYaw(th);

        geometry_msgs::TransformStamped odom_trans;
        odom_trans.header.stamp = current_time;
        odom_trans.header.frame_id = "odom";
        odom_trans.child_frame_id = "base_footprint";

        odom_trans.transform.translation.x = x;
        odom_trans.transform.translation.y = y;
        odom_trans.transform.translation.z = 0.0;

        //rotation data type is Quaternion
        odom_trans.transform.rotation = odom_quat;

        // odom transform data send to broadcaster
        odom_broadcaster.sendTransform(odom_trans);

        // navigation stack get velocity information from nav_msgs::Odometry
        nav_msgs::Odometry odom;
        odom.header.stamp = current_time;
        odom.header.frame_id = "odom";

        odom.pose.pose.position.x = x;
        odom.pose.pose.position.y = y;
        odom.pose.pose.position.z = 0.0;
        odom.pose.pose.orientation = odom_quat;

        odom.child_frame_id = "base_footprint";
        odom.twist.twist.linear.x = vx;
        odom.twist.twist.linear.y = vy;
        odom.twist.twist.angular.z = vth;

        odom_pub.publish(odom);

        last_time = current_time;
        r.sleep();
    }
}
        