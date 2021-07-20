#include <ros/ros.h>
#include <geometry_msgs/PoseStamped.h>
#include <geometry_msgs/Pose2D.h>
#include <nav_msgs/Odometry.h>
#include "wheelchair_door/doorpos.h"
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <sensor_msgs/Imu.h>
#include <tf/tf.h>
#include <math.h>
#include <wheelchair_door/doorinfo.h>

using namespace std;

#define LIDAR_X_POS	0.4188
#define LIDAR_Y_POS -0.25

typedef struct
{
	float door_center_x;
	float door_center_y;
	float my_pos_x;
	float my_pos_y;
	
}Position;

float my_theta[4] = {0,};

class GoalToDoor
{

public:
	GoalToDoor()
	{
		pub_pose = nh.advertise<geometry_msgs::Pose2D>("pose2d", 1);
		goal_pos = nh.advertise<geometry_msgs::PoseStamped>("/move_base_simple/goal",1);
		now_odom = nh.subscribe("odom", 10, &GoalToDoor::odomCallback, this);
    	door_pos = nh.subscribe("door_pos", 10, &GoalToDoor::doorposCallback, this);
		imu_theta = nh.subscribe("imu/data_raw", 1, &GoalToDoor::imuCallback, this);
		imu_flag_client = nh.serviceClient<wheelchair_door::doorinfo>("imu_flag_service");
	}

	void imuCallback(const sensor_msgs::Imu::ConstPtr& msg)
	{
		my_theta[0] = msg->orientation.w;
		my_theta[1] = msg->orientation.x;
		my_theta[2] = msg->orientation.y;
		my_theta[3] = msg->orientation.z;
		//cout << my_theta[0] << endl;
	}

	void doorposCallback(const wheelchair_door::doorpos::ConstPtr& msg)
	{
		if(msg->send_data_flag == true)
		{
			position.door_center_x = msg->x_pos;
			position.door_center_y = msg->y_pos;
			door_width = msg->door_width;
			
			srv.request.imu_clear_flag = true;
			if(imu_flag_client.call(srv))
			{
				Send_Goal();
			}
			else
			{
				ROS_ERROR("Failed to call service");
			}


		}
		
	}

   
	void odomCallback(const nav_msgs::Odometry::ConstPtr& msg)
	{
		position.my_pos_x = msg->pose.pose.position.x;
		position.my_pos_y = msg->pose.pose.position.y;


		pose2d.x = msg->pose.pose.position.x;
		pose2d.y = msg->pose.pose.position.y;

		tf::Quaternion q(
        	msg->pose.pose.orientation.x,
        	msg->pose.pose.orientation.y,
        	msg->pose.pose.orientation.z,
        	msg->pose.pose.orientation.w);
    	tf::Matrix3x3 m(q);
    	double roll, pitch, yaw;
    	m.getRPY(roll, pitch, yaw);
    
    	pose2d.theta = yaw;
    	pub_pose.publish(pose2d);

	}

	void Send_Goal()
	{
		float goal_x = 0.0, goal_y = 0.0, rotate_x = 0.0, rotate_y = 0.0;

		goal.header.frame_id = "odom";
		goal.header.stamp = ros::Time::now();
		//goal.pose.position.x = position.my_pos_x + position.door_center_x + LIDAR_X_POS;
		//goal.pose.position.y = position.my_pos_y + position.door_center_y + LIDAR_Y_POS ;
		
		goal_x = position.door_center_x + LIDAR_X_POS ;
		goal_y = position.door_center_y + LIDAR_Y_POS ;
		
		//goal_x = position.door_center_x ;
		//goal_y = position.door_center_y ;
		
		goal.pose.position.x = ( (goal_x * cos(pose2d.theta)) + (goal_x * sin(pose2d.theta)) ) + 0.3; 
		goal.pose.position.y = ( -(goal_y * sin(pose2d.theta)) + (goal_y * cos(pose2d.theta)) ) + 1.0;
		
		//goal.pose.position.x = ( (goal_x * cos(pose2d.theta)) + (goal_x * sin(pose2d.theta)) ) ; 
		//goal.pose.position.y = ( -(goal_y * sin(pose2d.theta)) + (goal_y * cos(pose2d.theta)) );
		
		//1.2

		//goal.pose.position.x = goal_x;
		//goal.pose.position.y = goal_y;
		
		
		// rotate_x = ( (goal_x * cos(pose2d.theta)) + (goal_x * sin(pose2d.theta)) ) + 0.3; 
		// rotate_y = ( -(goal_y * sin(pose2d.theta)) + (goal_y * cos(pose2d.theta)) ) + 1.0;
		// goal.pose.position.x = ( (rotate_x * cos(pose2d.theta)) + (rotate_x * sin(pose2d.theta)) ); 
		// goal.pose.position.y = ( -(rotate_y * sin(pose2d.theta)) + (rotate_y * cos(pose2d.theta)) );
		

		goal.pose.position.z = 0;




		goal.pose.orientation.x = 0;
		goal.pose.orientation.y = 0;
		//goal.pose.orientation.z = 0.0;
		//goal.pose.orientation.w = -1.0;
		goal.pose.orientation.z = -0.707;
		goal.pose.orientation.w = 0.707;
		
		// goal.pose.orientation.w = my_theta[0];
		// goal.pose.orientation.x = my_theta[1];
		// goal.pose.orientation.y = my_theta[2];
		// goal.pose.orientation.z = my_theta[3];
		

		goal_pos.publish(goal);
	}

private:
	ros::NodeHandle nh;
	ros::Publisher goal_pos;
	ros::Subscriber now_odom;
	ros::Subscriber door_pos;
	ros::Subscriber imu_theta;
	ros::Publisher pub_pose;

	ros::ServiceClient imu_flag_client;

	geometry_msgs::PoseStamped goal;
	geometry_msgs::Pose2D pose2d;

	wheelchair_door::doorinfo srv;

	Position position;
	
	
	float door_width = 0.0;
};

int main(int argc, char** argv) {
	ros::init(argc, argv, "gotodoor");
	
	GoalToDoor goaltodoor;
    //ros::Rate loop_rate(50);

    // while (ros::ok())
    // {
    //     ahrs_obj.get_data();
    //     loop_rate.sleep();
    // }
	

	ros::spin();
	return 0;
}