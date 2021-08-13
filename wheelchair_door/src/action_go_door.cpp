#include <ros/ros.h>
#include <geometry_msgs/PoseStamped.h>
#include <geometry_msgs/Pose2D.h>
#include <nav_msgs/Odometry.h>
#include <wheelchair_msg/door.h>
#include <wheelchair_msg/door_mode.h>
#include <wheelchair_msg/doormsg.h>
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
	GoalToDoor() : ac("move_base",true) , rate(10)
	{

		goal_pos = nh.advertise<geometry_msgs::PoseStamped>("/move_base_simple/goal",1);
		now_odom = nh.subscribe("odom", 10, &GoalToDoor::odomCallback, this);
    	door_pos = nh.subscribe("door_pos", 10, &GoalToDoor::doorposCallback, this);
		pub_pose = nh.advertise<geometry_msgs::Pose2D>("pose2d", 1);

		imu_client = nh.serviceClient<wheelchair_msg::door>("imu_flag_service");
		door_client = nh.serviceClient<wheelchair_msg::door_mode>("door_service_scan");
		
		ac.waitForServer();
	}

	void doorposCallback(const wheelchair_msg::doormsg::ConstPtr& msg)
	{
		float goal_x = 0.0, goal_y = 0.0, rotate_x = 0.0, rotate_y = 0.0;
		int door_loc = 0, door_sub_loc = 0;

		static int callback_cnt = 1;


		if(msg->send_data_flag == true && callback_cnt == 2)
		{
			ROS_INFO("NO");
			position.door_center_x = msg->x_pos;
			position.door_center_y = msg->y_pos;
			door_width = msg->door_width;
			door_loc = msg->door_loc;
			door_sub_loc = msg->door_sub_loc;
	
			Send_Goal(door_loc, door_sub_loc, callback_cnt);
			//callback_cnt = 1;
		}

		if(msg->send_data_flag == true && callback_cnt == 1)
		{
			ROS_INFO("hi");
			doing_flag = true;
			position.door_center_x = msg->x_pos;
			position.door_center_y = msg->y_pos;
			door_width = msg->door_width;
			door_loc = msg->door_loc;
			door_sub_loc = msg->door_sub_loc;
			
			imu_srv.request.imu_clear_flag = true;
			if(imu_client.call(imu_srv))
			{
				ROS_INFO("BYE");
				Send_Goal(door_loc, door_sub_loc, callback_cnt);
			}
			else
			{
				ROS_ERROR("Failed to call service");
			}
			callback_cnt++;
		}

		
		
		
	}
	#define X_OFFSET 0.5
	#define Y_OFFSET 1.0
	void Send_Goal(int door_loc, int door_sub_loc , int behavior)
	{
		float goal_x = 0.0, goal_y = 0.0;
		unsigned char count = 0;

		acgoal.target_pose.header.frame_id = "odom";
		acgoal.target_pose.header.stamp = ros::Time::now();

		if(behavior == 1)
		{	
			if(door_loc == 1)
			{	
				if(door_sub_loc == 1)
				{
					goal_x = position.door_center_x + LIDAR_X_POS ;
					goal_y = position.door_center_y + LIDAR_Y_POS ;
					acgoal.target_pose.pose.position.x = goal_x - Y_OFFSET; 
					acgoal.target_pose.pose.position.y = goal_y;
				}
				else if(door_sub_loc == 2)
				{
					goal_x = position.door_center_x + LIDAR_X_POS ;
					goal_y = position.door_center_y + LIDAR_Y_POS ;
					acgoal.target_pose.pose.position.x = goal_x - Y_OFFSET; 
					acgoal.target_pose.pose.position.y = goal_y;
				}

				else if(door_sub_loc == 3)
				{
					goal_x = position.door_center_x + LIDAR_X_POS ;
					goal_y = position.door_center_y + LIDAR_Y_POS ;
					acgoal.target_pose.pose.position.x = goal_x - Y_OFFSET; 
					acgoal.target_pose.pose.position.y = goal_y;
				}
			}

			else if(door_loc == 2)
			{
				goal_x = position.door_center_x + LIDAR_X_POS + WHEELCHAIR_ROTATE_POINT;
				goal_y = position.door_center_y + LIDAR_Y_POS ;
				acgoal.target_pose.pose.position.x = goal_x; 
				acgoal.target_pose.pose.position.y = goal_y - Y_OFFSET;
			}

			else if(door_loc == 3)
			{
				goal_x = position.door_center_x + LIDAR_X_POS + WHEELCHAIR_ROTATE_POINT;
				goal_y = position.door_center_y + LIDAR_Y_POS ;
				acgoal.target_pose.pose.position.x = goal_x; 
				acgoal.target_pose.pose.position.y = goal_y + Y_OFFSET;
			}
		}

		else if(behavior == 2)
		{
			acgoal.target_pose.header.frame_id = "odom";
			acgoal.target_pose.header.stamp = ros::Time::now();
			goal_x = position.my_pos_x + position.door_center_x + LIDAR_X_POS + WHEELCHAIR_ROTATE_POINT + X_OFFSET;
			goal_y = position.my_pos_y + position.door_center_y + LIDAR_Y_POS - 0.1;
			acgoal.target_pose.pose.position.x = goal_x; 
			acgoal.target_pose.pose.position.y = goal_y;
		}
			

		
		if(door_loc == 1)
		{
			acgoal.target_pose.pose.orientation.z = 0;
			acgoal.target_pose.pose.orientation.w = 1.0;
			ac.sendGoal(acgoal, boost::bind(&GoalToDoor::doneCb, this, _1), MoveBaseClient::SimpleActiveCallback());	
		}
		else if(door_loc == 2)
		{
			acgoal.target_pose.pose.orientation.z = 0.707;
			acgoal.target_pose.pose.orientation.w = 0.707;
			ac.sendGoal(acgoal, boost::bind(&GoalToDoor::doneCb, this, _1), MoveBaseClient::SimpleActiveCallback());
		}
		else if(door_loc == 3)
		{
			acgoal.target_pose.pose.orientation.z = -0.707;
			acgoal.target_pose.pose.orientation.w = 0.707;
			ac.sendGoal(acgoal, boost::bind(&GoalToDoor::doneCb, this, _1), MoveBaseClient::SimpleActiveCallback());
		}
		else
		{
			ROS_ERROR("Failed to get door location");
		}
	}

	void doneCb(const actionlib::SimpleClientGoalState& state)
    {
		ROS_INFO("DONECB: Finished in state [%s]", state.toString().c_str());        
    	if (ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
    	{
			cout << "reach goal" << endl;
			if(doing_flag == true)
			{	
				imu_srv.request.imu_clear_flag = true;

				door_mode_srv.request.door_req_flag = true;
				door_mode_srv.request.door_mode = 1;
				door_mode_srv.request.sub_door_mode = 3;
				
				if(imu_client.call(imu_srv))
				{
					if(door_client.call(door_mode_srv))
					{
						ROS_INFO("SECOND NAVI START");
					}
					else
					{
						ROS_ERROR("Failed to Second Navi");
					}
				}
				else
				{
					ROS_ERROR("Failed to Second Imu reset");
				}
				doing_flag = false;
			}                   
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

	ros::ServiceClient imu_client;
	ros::ServiceClient door_client;
	
	ros::Rate rate;
	
	MoveBaseClient ac;
	move_base_msgs::MoveBaseGoal acgoal;

	geometry_msgs::PoseStamped goal;
	geometry_msgs::Pose2D pose2d;
	wheelchair_msg::door imu_srv;
	wheelchair_msg::door_mode door_mode_srv;

	Position position;
	
	float door_width = 0.0;
	bool doing_flag = true;
};

int main(int argc, char** argv) {
	ros::init(argc, argv, "door_action_goals");
	
	GoalToDoor goaltodoor;

    // while (ros::ok())
    // {
    //     ahrs_obj.get_data();
    //     loop_rate.sleep();
    // }
	

	ros::spin();
	return 0;
}