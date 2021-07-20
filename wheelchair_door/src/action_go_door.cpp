#include <ros/ros.h>
#include <geometry_msgs/PoseStamped.h>
#include <geometry_msgs/Pose2D.h>
#include <nav_msgs/Odometry.h>
#include <wheelchair_msg/door.h>
#include "wheelchair_door/doorpos.h"
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <tf/tf.h>
#include <sensor_msgs/Imu.h>
#include <math.h>

using namespace std;

#define LIDAR_X_POS	0.4188
#define LIDAR_Y_POS -0.25
#define WHEELCHAIR_ROTATE_POINT 0.35 

typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;

typedef struct
{
	float door_center_x;
	float door_center_y;
	float my_pos_x;
	float my_pos_y;
}Position;


class GoalToDoor
{

public:
	GoalToDoor() : ac("move_base",true)
	{

		goal_pos = nh.advertise<geometry_msgs::PoseStamped>("/move_base_simple/goal",1);
		now_odom = nh.subscribe("odom", 10, &GoalToDoor::odomCallback, this);
    	door_pos = nh.subscribe("door_pos", 10, &GoalToDoor::doorposCallback, this);
		pub_pose = nh.advertise<geometry_msgs::Pose2D>("pose2d", 1);

		client = nh.serviceClient<wheelchair_msg::door>("imu_flag_service");
		ac.waitForServer();
	}

	void doorposCallback(const wheelchair_door::doorpos::ConstPtr& msg)
	{
		float goal_x = 0.0, goal_y = 0.0, rotate_x = 0.0, rotate_y = 0.0;

		if(msg->send_data_flag == true)
		{
			position.door_center_x = msg->x_pos;
			position.door_center_y = msg->y_pos;
			door_width = msg->door_width;
			//Send_Goal();

			srv.request.imu_clear_flag = true;
			if(client.call(srv))
			{
				Send_Goal();
			}
			else
			{
				ROS_ERROR("Failed to call service");
			}


			// acgoal.target_pose.header.frame_id = "odom";
			// acgoal.target_pose.header.stamp = ros::Time::now();

			// goal_x = position.door_center_x + LIDAR_X_POS ;
			// goal_y = position.door_center_y + LIDAR_Y_POS ;
			
			// acgoal.target_pose.pose.position.x = ( (goal_x * cos(pose2d.theta)) + (goal_x * sin(pose2d.theta)) ) + 0.3; 
			// acgoal.target_pose.pose.position.y = ( -(goal_y * sin(pose2d.theta)) + (goal_y * cos(pose2d.theta)) ) + 1.0;
			// acgoal.target_pose.pose.orientation.z = -0.707;
			// acgoal.target_pose.pose.orientation.w = 0.707;
			// ac.sendGoal(acgoal, boost::bind(&GoalToDoor::doneCb, this, _1), MoveBaseClient::SimpleActiveCallback());
		}
		
	}

	#define Y_OFFSET 1.0
	void Send_Goal()
	{
		float goal_x = 0.0, goal_y = 0.0;

		acgoal.target_pose.header.frame_id = "odom";
		acgoal.target_pose.header.stamp = ros::Time::now();

		goal_x = position.door_center_x + LIDAR_X_POS + WHEELCHAIR_ROTATE_POINT;
		goal_y = position.door_center_y + LIDAR_Y_POS ;

		acgoal.target_pose.pose.position.x = goal_x; 
		acgoal.target_pose.pose.position.y = goal_y + Y_OFFSET;
		

		//acgoal.target_pose.pose.position.x = ( (goal_x * cos(pose2d.theta)) + (goal_x * sin(pose2d.theta)) ) + 0.3; 
		//acgoal.target_pose.pose.position.y = ( -(goal_y * sin(pose2d.theta)) + (goal_y * cos(pose2d.theta)) ) + 1.0;
		acgoal.target_pose.pose.orientation.z = -0.707;
		acgoal.target_pose.pose.orientation.w = 0.707;
		ac.sendGoal(acgoal, boost::bind(&GoalToDoor::doneCb, this, _1), MoveBaseClient::SimpleActiveCallback());
	}

	void doneCb(const actionlib::SimpleClientGoalState& state)
    {
		ROS_INFO("DONECB: Finished in state [%s]", state.toString().c_str());        
    	if (ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
    	{
			cout << "reach goal" << endl;
        	// do something as goal was reached                   
    	}
    	if (ac.getState() == actionlib::SimpleClientGoalState::ABORTED)
    	{
			cout << "not yet reach goal" << endl;
        	// do something as goal was canceled   
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

private:
	ros::NodeHandle nh;
	ros::Publisher goal_pos;
	ros::Subscriber now_odom;
	ros::Subscriber door_pos;
	ros::Publisher pub_pose;

	ros::ServiceClient client;

	MoveBaseClient ac;
	move_base_msgs::MoveBaseGoal acgoal;
	


	geometry_msgs::PoseStamped goal;
	geometry_msgs::Pose2D pose2d;
	wheelchair_msg::door srv;

	Position position;
	
	float door_width = 0.0;
};

int main(int argc, char** argv) {
	ros::init(argc, argv, "door_action_goals");
	
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