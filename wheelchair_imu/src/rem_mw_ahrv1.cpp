#include <ros/ros.h>
#include <iostream>
#include <sensor_msgs/Imu.h>
#include <tf/transform_broadcaster.h>
#include "Serial.h"

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
        
        // ss=7 동기화 데이터 전송 -> 데이터 게속 보냄    
        
        /*
        Tx[0] = 'S';        // s
        Tx[1] = 'S';        // s
        Tx[2] = '=';     // =
        Tx[3] = '7';     // 7
        Tx[4] = '\r';       // CR
        Tx[5] = '\n';       // LF
        */
       strcpy((char *)Tx,"SS=7\r\n");
       write(dev,Tx,strlen((char *)Tx));
        

        // sp = 100 데이터 전송속도 변경
        /*
        Tx[0] = S;        // s
        Tx[1] = P;        // p
        Tx[2] = 0x3D;     // =
        Tx[3] = 0x31;     // 1
        Tx[4] = 0x30;     // 0
        Tx[5] = 0x30;     // 0
        Tx[6] = CR;       // CR
        Tx[7] = LF;       // LF
        */

       strcpy((char *)Tx,"SP=20\r\n");// unit ms
       write(dev,Tx,strlen((char *)Tx));

        //        write(dev,Tx,strlen((char *)Tx));
    }

    ~MW_AHRS()
    {
        close_serial(dev);
    }

    void seperate_imu_data(char *recData)
    {
        // printf("%05d, L:%3d - %s\r\n"
        //     , PackCnt
        // //    , strlen((char*)buffer)
        //     , buffer_tail_Index
        // //    , buffer
        //     , recData
        // );
        // // //cout<<buffer;
        // // //cout<<recData;
        //  PackCnt++;
        //  PackCnt %= 1000;

        
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
                // cout << "Acc :" 
                //     << imu_data.ax << " " 
                //     << imu_data.ay << " " 
                //     << imu_data.az << "\t"
                //     ;
                // cout << "Gyro :" 
                //     << imu_data.gx << " " 
                //     << imu_data.gy << " " 
                //     << imu_data.gz << "\t"
                //     ;
                // cout << "Euler :" 
                //     << imu_data.roll << " " 
                //     << imu_data.pitch << " " 
                //     << imu_data.yaw << "\r\n"
                //     ;

            }
            else
            {
                cout << "Err\r\n";
            }
            /*
        char *ptr = strtok(recData, " ");
        null_count=0;

        while(ptr != NULL)
        {
            if(null_count == 0)
            {
                imu_data.ax = atof(ptr);
                cout << "ax = " << imu_data.ax;
            }
            else if(null_count == 1)
            {
                imu_data.ay = atof(ptr);
                cout << " ay = " << imu_data.ay;
            }
            else if(null_count == 2)
            {
                imu_data.az = atof(ptr);
                cout << " az = " << imu_data.az;
            }
            else if(null_count == 3)
            {
                imu_data.gx = atof(ptr);
                cout << " gx = " << imu_data.gx;
            }
            else if(null_count == 4)
            {
                imu_data.gy = atof(ptr);
                cout << " gy = " << imu_data.gy;
            }
            else if(null_count == 5)
            {
                imu_data.gz = atof(ptr);
                cout << " gz = " << imu_data.gz;
            }
            else if(null_count == 6)
            {
                imu_data.roll = atof(ptr);
                cout << " roll = " << imu_data.roll;
            }
            else if(null_count == 7)
            {
                imu_data.pitch = atof(ptr);
                cout << " pitch = " << imu_data.pitch;
            }
            else if(null_count == 8)
            {
                imu_data.yaw = atof(ptr);
                cout << " yaw = " << imu_data.yaw << endl;
            }
            else if(null_count == 9)
            {
                error_cnt++;
                if(error_cnt >= 5) 
                {
                    //cout << "OVER NULL ERROR !!!"  << endl;
                
                }

            }
            null_count++;
            ptr = strtok(NULL, " ");
        }
            */
    }

    void get_data(void)
    {
        char lrecData[BUFFER_SIZE] = {0,};

        length = read(dev, &buffer[buffer_tail_Index], BUFFER_SIZE);
        buffer_tail_Index += length;

        
        //  skip_cnt++;
        //ROS_INFO("length : %d",length);
        
        
         // if(skip_cnt > 10)
        
        if( (length==0) && (buffer_tail_Index >= 82))
        {
            memcpy(lrecData, buffer, sizeof(buffer));
            memset(buffer,0,sizeof(buffer));
            buffer_tail_Index = 0;

            seperate_imu_data(lrecData);
            pulishIMUtopic();
            //buffer_tail_Index = 0;


        }
        //    if(skip_cnt > 254) skip_cnt = 10;

        /*
        if(skip_cnt > 10 && length == 82)
        {
            seperate_imu_data();
            pulishIMUtopic();
            if(skip_cnt > 254) skip_cnt = 10;
        }
        */
        
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
    //ros::Publisher imu_pub = nh.advertise<sensor_msgs::Imu>("wheelchair_imu", 1);    
    ros::Publisher imu_pub = nh.advertise<sensor_msgs::Imu>("imu/data_raw", 1);    
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
    }

    return 0;
}
