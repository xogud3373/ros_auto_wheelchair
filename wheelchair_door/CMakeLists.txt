cmake_minimum_required(VERSION 3.0.2)
project(wheelchair_door)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  message_generation
  roscpp
  rospy
  sensor_msgs
  std_msgs
  move_base_msgs
  actionlib
  wheelchair_msg
)

## Generate messages in the 'msg' folder
add_message_files(
  FILES
  doorpos.msg
  
)

## Generate services in the 'srv' folder
add_service_files(
  FILES
  doorinfo.srv
)

## Generate actions in the 'action' folder
# add_action_files(
#   FILES
#   Action1.action
#   Action2.action
# )

## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  geometry_msgs
  sensor_msgs
  std_msgs
)


catkin_package(
 INCLUDE_DIRS include
 LIBRARIES wheelchair_door
 CATKIN_DEPENDS geometry_msgs roscpp rospy sensor_msgs std_msgs message_runtime move_base_msgs actionlib wheelchair_msg
 DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

## Declare a C++ library
# add_library(${PROJECT_NAME}
#   src/${PROJECT_NAME}/wheelchair_door.cpp
# )

add_executable(door_send_goals src/go_to_door.cpp)
add_dependencies(door_send_goals ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(door_send_goals ${catkin_LIBRARIES})

add_executable(gotodoor src/door_icr.cpp)
add_dependencies(gotodoor ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(gotodoor ${catkin_LIBRARIES})

add_executable(door_action_goals src/action_go_door.cpp)
add_dependencies(door_action_goals ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(door_action_goals ${catkin_LIBRARIES})
