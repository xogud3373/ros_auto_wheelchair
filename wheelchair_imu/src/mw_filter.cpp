#include <ros/ros.h>
#include <iostream>
#include <sensor_msgs/Imu.h>
#include <sensor_msgs/MagneticField.h>
#include <tf/transform_broadcaster.h>
#include "Serial.h"

#define PI 3.14159265
#define BUFFER_SIZE 150
typedef struct
{
    float ax;
    float ay;
    float az;
    float gx;
    float gy;
    float gz;
    float roll;
    float pitch;
    float yaw;
    float magx;
    float magy;
    float magz;

}Imu_data;

class MW_AHRS
{

public:
    MW_AHRS()
    {
        for(int i=0; i<BUFFER_SIZE; i++)
            buffer[i] = 0;

        dev = open_serial((char*)"/dev/ttyUSB0", 115200, 0, 0);
        if(dev == -1)
        {
            cout << " Error opening port\n" << endl;
        }
        
        // ss=7 동기화 데이터 전송 -> 데이터 게속 보냄    
        Tx[0] = S;        // s
        Tx[1] = S;        // s
        Tx[2] = 0x3D;     // =
        Tx[3] = 0x31;     // 1
        Tx[4] = 0x35;     // 5
        Tx[5] = CR;       // CR
        Tx[6] = LF;       // LF

        write(dev,Tx,7);
        
    }

    ~MW_AHRS()
    {
        close_serial(dev);
    }

    void seperate_imu_data(void)
    {
        char *ptr = strtok(buffer, " ");
            null_count=0;

            while(ptr != NULL)
            {
                if(null_count == 0)
                {
                    imu_data.ax = atof(ptr);
                    //cout << "ax = " << imu_data.ax;
                }
                else if(null_count == 1)
                {
                    imu_data.ay = atof(ptr);
                    //cout << " ay = " << imu_data.ay;
                }
                else if(null_count == 2)
                {
                    imu_data.az = atof(ptr);
                    //cout << " az = " << imu_data.az;
                }
                else if(null_count == 3)
                {
                    imu_data.gx = atof(ptr);
                    //cout << " gx = " << imu_data.gx;
                }
                else if(null_count == 4)
                {
                    imu_data.gy = atof(ptr);
                    //cout << " gy = " << imu_data.gy;
                }
                else if(null_count == 5)
                {
                    imu_data.gz = atof(ptr);
                    //cout << " gz = " << imu_data.gz;
                }
                else if(null_count == 6)
                {
                    imu_data.roll = atof(ptr);
                    //cout << " roll = " << imu_data.roll;
                }
                else if(null_count == 7)
                {
                    imu_data.pitch = atof(ptr);
                    //cout << " pitch = " << imu_data.pitch;
                }
                else if(null_count == 8)
                {
                    imu_data.yaw = atof(ptr);
                    //cout << " yaw = " << imu_data.yaw;
                }
                else if(null_count == 9)
                {
                    imu_data.magx = atof(ptr);
                    //cout << " magx = " << imu_data.magx;
                }
                else if(null_count == 10)
                {
                    imu_data.magy = atof(ptr);
                    //cout << " magy = " << imu_data.magy;
                }
                else if(null_count == 11)
                {
                    imu_data.magz = atof(ptr);
                    //cout << " magz = " << imu_data.magz << endl;
                }
                else if(null_count == 12)
                {
                    //cout << " over " << endl;
                    error_cnt++;
                    if(error_cnt >= 5) 
                    {
                        cout << "OVER NULL ERROR !!!"  << endl;
                    
                    }

                }
                null_count++;
                ptr = strtok(NULL, " ");
            }
    }

    void get_data(void)
    {
        read(dev, &buffer, BUFFER_SIZE);

        skip_cnt++;
        //ROS_INFO("skip_cnt : %d",skip_cnt);
        
        if(skip_cnt > 10)
        {
            seperate_imu_data();
            pulishIMUtopic();
            if(skip_cnt > 254) skip_cnt = 10;
        }
        
    }

    void pulishIMUtopic(void)
    {
        sensor_msgs::Imu imu_data_msg;
        sensor_msgs::MagneticField mag_data_msg;

        imu_data_msg.linear_acceleration_covariance[0] = 
        imu_data_msg.linear_acceleration_covariance[4] =
        imu_data_msg.linear_acceleration_covariance[8] = -1;

        imu_data_msg.angular_velocity_covariance[0] = 
        imu_data_msg.angular_velocity_covariance[4] = 
        imu_data_msg.angular_velocity_covariance[8] = -1;

        imu_data_msg.orientation_covariance[0] =
        imu_data_msg.orientation_covariance[4] =
        imu_data_msg.orientation_covariance[8] = -1;

        mag_data_msg.magnetic_field_covariance[0] =
        mag_data_msg.magnetic_field_covariance[4] =
        mag_data_msg.magnetic_field_covariance[8] = -1;

        static double convertor_d2r = PI / 180.0;
        static double convertor_r2d = 180.0 / PI;
        static double convertor_g2m = 9.80665;

        double roll, pitch, yaw;
        roll = imu_data.roll * convertor_d2r;
        pitch = imu_data.pitch * convertor_d2r;
        yaw = imu_data.yaw * convertor_d2r;

        tf::Quaternion orientation = tf::createQuaternionFromRPY(roll, pitch, yaw);
        
        ros::Time now = ros::Time::now();

        imu_data_msg.header.stamp = now;
        mag_data_msg.header.stamp = now;

        imu_data_msg.header.frame_id = "imu_link";
        mag_data_msg.header.frame_id = "imu_mag_link";

        imu_data_msg.orientation.x = orientation[0];
        imu_data_msg.orientation.y = orientation[1];
        imu_data_msg.orientation.z = orientation[2];
        imu_data_msg.orientation.w = orientation[3];

        // 기존 g 단위를 m/s^2 로 변경
		imu_data_msg.linear_acceleration.x = 0;
		imu_data_msg.linear_acceleration.y = 0;
		imu_data_msg.linear_acceleration.z = 0;
		imu_data_msg.linear_acceleration.x = imu_data.ax * convertor_g2m;
		imu_data_msg.linear_acceleration.y = imu_data.ay * convertor_g2m;
		imu_data_msg.linear_acceleration.z = imu_data.az * convertor_g2m;

		// imu.gx gy gz.
		// 기존 degree/s 단위를 radian/s 로 변경
        imu_data_msg.angular_velocity.x = 0;
		imu_data_msg.angular_velocity.y = 0;
		imu_data_msg.angular_velocity.z = 0;
		imu_data_msg.angular_velocity.x = imu_data.gx * convertor_d2r;
		imu_data_msg.angular_velocity.y = imu_data.gy * convertor_d2r;
		imu_data_msg.angular_velocity.z = imu_data.gz * convertor_d2r;

        mag_data_msg.magnetic_field.x = 0;
        mag_data_msg.magnetic_field.y = 0;
        mag_data_msg.magnetic_field.z = 0;
        mag_data_msg.magnetic_field.x = imu_data.magx;
        mag_data_msg.magnetic_field.y = imu_data.magy;
        mag_data_msg.magnetic_field.z = imu_data.magz;

        imu_pub.publish(imu_data_msg);
        imu_mag_pub.publish(mag_data_msg);
    }


private:
    ros::NodeHandle nh;
    ros::Publisher imu_pub = nh.advertise<sensor_msgs::Imu>("imu/data_raw", 10);
    ros::Publisher imu_mag_pub = nh.advertise<sensor_msgs::MagneticField>("imu/mag", 10);    
    Imu_data imu_data{};
    
    // Device Name
    int dev = 0;

    // Data buffer
    char buffer[BUFFER_SIZE];
    unsigned char Tx[7];

    // Serperate Imu Data Variable
    int null_count = 0;
   
    unsigned char skip_cnt = 0;
    unsigned char error_cnt = 0;

    // ASCII CODE
    const unsigned char A = 0x61;
    const unsigned char N = 0x6E;
    const unsigned char G = 0x67;
    const unsigned char CR = 0x0D;
    const unsigned char LF = 0x0A;
    const unsigned char S = 0x73;

    
};


int main(int argc, char **argv)
{
    ros::init(argc, argv, "wheelchair_filter_imu");
    
    MW_AHRS ahrs_obj;
    ros::Rate loop_rate(50);

    while (ros::ok())
    {
        ahrs_obj.get_data();
        //ahrs_obj.pulishIMUtopic(imu_data);

        loop_rate.sleep();

    }

    return 0;
}