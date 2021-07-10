#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include <std_msgs/Int32.h>
#include <sensor_msgs/Imu.h>
#include "wc_encoder.h"

int lpulse = 0, rpulse = 0;
int PPR = 151200;   // 21(모터기어비) * 7200(엔코더tick)
double Tc = 0.02;
float orientation[4] = {0,};

void lencoderCallback(const std_msgs::Int32::ConstPtr& msg)
{
    lpulse = msg->data;
    
}

void rencoderCallback(const std_msgs::Int32::ConstPtr& msg)
{
    rpulse = msg->data; 
}

void imuCallback(const sensor_msgs::Imu::ConstPtr& msg)
{
    orientation[0] = msg->orientation.w;
    orientation[1] = msg->orientation.x;
    orientation[2] = msg->orientation.y;
    orientation[3] = msg->orientation.z;
}

int main(int argc, char** argv)
{
    ros::init(argc,argv,"wheelchair_odometry_imu_pub");

    ros::NodeHandle nh;
    ros::Publisher odom_pub = nh.advertise<nav_msgs::Odometry>("odom",10);
    ros::Subscriber lencoder_sub = nh.subscribe("encoder_lpulse", 10, lencoderCallback);
    ros::Subscriber rencoder_sub = nh.subscribe("encoder_rpulse", 10, rencoderCallback);
    //ros::Subscriber imu_sub = nh.subscribe("wheelchair_imu", 10, imuCallback);
    ros::Subscriber imu_sub = nh.subscribe("imu/data", 10, imuCallback);
    
    tf::TransformBroadcaster odom_broadcaster;

    ENCODER encoder;     // encoder instance
    HEELVEL hlv;         // encoder struct


    double x = 0.0;
    double y = 0.0;
    double th = 0.0;

    double vx = 0.0;
    double vy = 0.0;
    double vth = 0.0;

    float odom_pose[3] = {0, };
    double odom_vel[3] = {0, };

    double delta_s, theta, delta_theta;
    static double last_theta = 0.0;
    double v, w;

    
    ros::Time current_time, last_time;
    current_time = ros::Time::now();
    last_time = ros::Time::now();

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
        // delta_s
        delta_s = (( hlv.l_heel_vel + hlv.r_heel_vel ) / 2 ) * dt;   // m/s * s => m
        
        theta = atan2f(orientation[1]*orientation[2] + orientation[0]*orientation[3], 
                0.5f - orientation[2]*orientation[2] - orientation[3]*orientation[3]);

        delta_theta = theta - last_theta; 

        odom_pose[0] += delta_s * cos(odom_pose[2] + (delta_theta / 2.0));
        odom_pose[1] += delta_s * sin(odom_pose[2] + (delta_theta / 2.0));
        odom_pose[2] += delta_theta;

        v = delta_s / dt;
        w = delta_theta / dt;

        odom_vel[0] = v;
        odom_vel[1] = 0.0;
        odom_vel[2] = w;

        //double vx = ( hlv.l_heel_vel + hlv.r_heel_vel ) / 2;   // m/s
        //double vy = 0.0;                                       // m/s
        //double vth = ( hlv.l_heel_vel - hlv.r_heel_vel ) / lengthBetweenWheels;    // 1/s
        
        //double delta_x = (vx * cos(th));     // m
        //double delta_y = (vx * sin(th));     // m
        //double delta_th = vth * dt;               // 단위 x

        //x += delta_x;
        //y += delta_y;
        //th += delta_th;
        
        geometry_msgs::Quaternion odom_quat = tf::createQuaternionMsgFromYaw(odom_pose[2]);

        geometry_msgs::TransformStamped odom_trans;
        odom_trans.header.stamp = current_time;
        odom_trans.header.frame_id = "odom";
        odom_trans.child_frame_id = "base_footprint";

        odom_trans.transform.translation.x = odom_pose[0];
        odom_trans.transform.translation.y = odom_pose[1];
        odom_trans.transform.translation.z = 0.0;

        //rotation data type is Quaternion
        odom_trans.transform.rotation = odom_quat;

        // odom transform data send to broadcaster
        odom_broadcaster.sendTransform(odom_trans);

        // navigation stack get velocity information from nav_msgs::Odometry
        nav_msgs::Odometry odom;
        odom.header.stamp = current_time;
        odom.header.frame_id = "odom";
        odom.child_frame_id = "base_footprint";
        
        odom.pose.pose.position.x = odom_pose[0];
        odom.pose.pose.position.y = odom_pose[1];
        odom.pose.pose.position.z = 0.0;
        odom.pose.pose.orientation = odom_quat;

        odom.twist.twist.linear.x = odom_vel[0];
        odom.twist.twist.linear.y = 0.0;
        odom.twist.twist.angular.z = odom_vel[2];

        odom_pub.publish(odom);

        last_theta = theta;
        last_time = current_time;
        r.sleep();
    }
}
        