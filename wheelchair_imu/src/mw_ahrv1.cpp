#include <ros/ros.h>
#include <iostream>
#include <sensor_msgs/Imu.h>
#include <tf/transform_broadcaster.h>
#include "Serial.h"
#include <wheelchair_msg/door.h>

#define PI 3.14159265
#define BUFFER_SIZE 200
#define TX_SIZE 6

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

}Imu_data;

class MW_AHRS
{

public:
    MW_AHRS()
    {
        memset(buffer, 0, sizeof(buffer));

        dev = open_serial((char*)"/dev/ttyUSB0", 921600, 0, 0);
        if(dev == -1)
        {
            cout << " Error opening port\n" << endl;
        }
        
        server =  nh.advertiseService("imu_flag_service", &MW_AHRS::doorCallback, this);
        // Eulur 초기화 ( Yaw 드리프트 초기화 )
        /*
        Tx[0] = 0x63;     // c
        Tx[1] = 0x6D;     // m
        Tx[2] = 0x64;     // d
        Tx[3] = 0x3D;     // =
        Tx[4] = 0x35;     // 5
        Tx[5] = CR;       // CR
        Tx[6] = LF;       // LF

        write(dev,Tx,7);
        */
    
       strcpy((char *)Tx,"SS=7\r\n");
       write(dev,Tx,strlen((char *)Tx));
        

       strcpy((char *)Tx,"SP=20\r\n");// unit ms
       write(dev,Tx,strlen((char *)Tx));

    }

    ~MW_AHRS()
    {
        close_serial(dev);
    }

    bool doorCallback(wheelchair_msg::door::Request &req, wheelchair_msg::door::Response &res)
    {
        res.calc_door_flag = true;
        ROS_INFO("IMU RESET COMFILCATE");
        strcpy((char *)Tx,"cmd=5\r\n");
        write(dev,Tx,strlen((char *)Tx));
        return true;
    }

    void seperate_imu_data(char *recData)
    {
        
        Imu_data lImuDarta;
        int dataCnt =0;

        dataCnt = sscanf(recData,"%f %f %f %f %f %f %f %f %f"
            , &lImuDarta.ax  
            , &lImuDarta.ay  
            , &lImuDarta.az
            , &lImuDarta.gx  
            , &lImuDarta.gy  
            , &lImuDarta.gz 
            , &lImuDarta.roll  
            , &lImuDarta.pitch
            , &lImuDarta.yaw

            );
            if(dataCnt == 9)
            {
                memcpy(&imu_data, &lImuDarta, sizeof(lImuDarta));

            }
            else
            {
                cout << "Err\r\n";
            }
       
    }

    void get_data(void)
    {
        char lrecData[BUFFER_SIZE] = {0,};

        length = read(dev, &buffer[buffer_tail_Index], BUFFER_SIZE);
        buffer_tail_Index += length;

        
        if( (length==0) && (buffer_tail_Index >= 82))
        {
            memcpy(lrecData, buffer, sizeof(buffer));
            memset(buffer,0,sizeof(buffer));
            buffer_tail_Index = 0;

            seperate_imu_data(lrecData);
            pulishIMUtopic();

        }
        
    }

    void pulishIMUtopic(void)
    {
        sensor_msgs::Imu imu_data_msg;

        imu_data_msg.linear_acceleration_covariance[0] = 
        imu_data_msg.linear_acceleration_covariance[4] =
        imu_data_msg.linear_acceleration_covariance[8] = -1;

        imu_data_msg.angular_velocity_covariance[0] = 
        imu_data_msg.angular_velocity_covariance[4] = 
        imu_data_msg.angular_velocity_covariance[8] = -1;

        imu_data_msg.orientation_covariance[0] =
        imu_data_msg.orientation_covariance[4] =
        imu_data_msg.orientation_covariance[8] = -1;

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
        imu_data_msg.header.frame_id = "imu_link";

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

        imu_pub.publish(imu_data_msg);

    }


private:
    ros::NodeHandle nh;
    ros::Publisher imu_pub = nh.advertise<sensor_msgs::Imu>("imu/data_raw", 1);
    ros::ServiceServer server;

    Imu_data imu_data{};
    
    // Device Name
    int dev = 0;

    // Data buffer
    char buffer[BUFFER_SIZE];
    int16_t buffer_tail_Index = 0;

    unsigned char Tx[TX_SIZE];

    // Serperate Imu Data Variable
    int null_count = 0;
    int length = 0;
    //unsigned char skip_cnt = 0;
    unsigned int skip_cnt = 0;
    unsigned char error_cnt = 0;

    // ASCII CODE
    const unsigned char A = 0x61;
    const unsigned char N = 0x6E;
    const unsigned char G = 0x67;
    const unsigned char CR = 0x0D;
    const unsigned char LF = 0x0A;
    const unsigned char S = 0x73;
    const unsigned char P = 0x70;

    uint16_t PackCnt = 0;
    
};


int main(int argc, char **argv)
{
    ros::init(argc, argv, "wheelchair_imu");
    
    MW_AHRS ahrs_obj;
    ros::Rate loop_rate(1000);

    while (ros::ok())
    {
        ahrs_obj.get_data();
        loop_rate.sleep();
        ros::spinOnce();
    }

    return 0;
}
