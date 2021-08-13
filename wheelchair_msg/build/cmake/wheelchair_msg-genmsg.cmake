# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "wheelchair_msg: 4 messages, 4 services")

set(MSG_I_FLAGS "-Iwheelchair_msg:/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(wheelchair_msg_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/caselidar.msg" NAME_WE)
add_custom_target(_wheelchair_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "wheelchair_msg" "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/caselidar.msg" ""
)

get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/coop_mode.srv" NAME_WE)
add_custom_target(_wheelchair_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "wheelchair_msg" "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/coop_mode.srv" ""
)

get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/doormsg.msg" NAME_WE)
add_custom_target(_wheelchair_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "wheelchair_msg" "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/doormsg.msg" ""
)

get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/normal.msg" NAME_WE)
add_custom_target(_wheelchair_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "wheelchair_msg" "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/normal.msg" ""
)

get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door_mode.srv" NAME_WE)
add_custom_target(_wheelchair_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "wheelchair_msg" "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door_mode.srv" ""
)

get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door.srv" NAME_WE)
add_custom_target(_wheelchair_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "wheelchair_msg" "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door.srv" ""
)

get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/coop.msg" NAME_WE)
add_custom_target(_wheelchair_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "wheelchair_msg" "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/coop.msg" ""
)

get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/normal_mode.srv" NAME_WE)
add_custom_target(_wheelchair_msg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "wheelchair_msg" "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/normal_mode.srv" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/normal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/wheelchair_msg
)
_generate_msg_cpp(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/caselidar.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/wheelchair_msg
)
_generate_msg_cpp(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/coop.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/wheelchair_msg
)
_generate_msg_cpp(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/doormsg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/wheelchair_msg
)

### Generating Services
_generate_srv_cpp(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/wheelchair_msg
)
_generate_srv_cpp(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/normal_mode.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/wheelchair_msg
)
_generate_srv_cpp(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/coop_mode.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/wheelchair_msg
)
_generate_srv_cpp(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door_mode.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/wheelchair_msg
)

### Generating Module File
_generate_module_cpp(wheelchair_msg
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/wheelchair_msg
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(wheelchair_msg_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(wheelchair_msg_generate_messages wheelchair_msg_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/caselidar.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_cpp _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/coop_mode.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_cpp _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/doormsg.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_cpp _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/normal.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_cpp _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door_mode.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_cpp _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_cpp _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/coop.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_cpp _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/normal_mode.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_cpp _wheelchair_msg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(wheelchair_msg_gencpp)
add_dependencies(wheelchair_msg_gencpp wheelchair_msg_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS wheelchair_msg_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/normal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/wheelchair_msg
)
_generate_msg_eus(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/caselidar.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/wheelchair_msg
)
_generate_msg_eus(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/coop.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/wheelchair_msg
)
_generate_msg_eus(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/doormsg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/wheelchair_msg
)

### Generating Services
_generate_srv_eus(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/wheelchair_msg
)
_generate_srv_eus(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/normal_mode.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/wheelchair_msg
)
_generate_srv_eus(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/coop_mode.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/wheelchair_msg
)
_generate_srv_eus(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door_mode.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/wheelchair_msg
)

### Generating Module File
_generate_module_eus(wheelchair_msg
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/wheelchair_msg
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(wheelchair_msg_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(wheelchair_msg_generate_messages wheelchair_msg_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/caselidar.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_eus _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/coop_mode.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_eus _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/doormsg.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_eus _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/normal.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_eus _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door_mode.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_eus _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_eus _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/coop.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_eus _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/normal_mode.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_eus _wheelchair_msg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(wheelchair_msg_geneus)
add_dependencies(wheelchair_msg_geneus wheelchair_msg_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS wheelchair_msg_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/normal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/wheelchair_msg
)
_generate_msg_lisp(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/caselidar.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/wheelchair_msg
)
_generate_msg_lisp(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/coop.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/wheelchair_msg
)
_generate_msg_lisp(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/doormsg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/wheelchair_msg
)

### Generating Services
_generate_srv_lisp(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/wheelchair_msg
)
_generate_srv_lisp(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/normal_mode.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/wheelchair_msg
)
_generate_srv_lisp(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/coop_mode.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/wheelchair_msg
)
_generate_srv_lisp(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door_mode.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/wheelchair_msg
)

### Generating Module File
_generate_module_lisp(wheelchair_msg
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/wheelchair_msg
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(wheelchair_msg_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(wheelchair_msg_generate_messages wheelchair_msg_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/caselidar.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_lisp _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/coop_mode.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_lisp _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/doormsg.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_lisp _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/normal.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_lisp _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door_mode.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_lisp _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_lisp _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/coop.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_lisp _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/normal_mode.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_lisp _wheelchair_msg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(wheelchair_msg_genlisp)
add_dependencies(wheelchair_msg_genlisp wheelchair_msg_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS wheelchair_msg_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/normal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/wheelchair_msg
)
_generate_msg_nodejs(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/caselidar.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/wheelchair_msg
)
_generate_msg_nodejs(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/coop.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/wheelchair_msg
)
_generate_msg_nodejs(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/doormsg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/wheelchair_msg
)

### Generating Services
_generate_srv_nodejs(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/wheelchair_msg
)
_generate_srv_nodejs(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/normal_mode.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/wheelchair_msg
)
_generate_srv_nodejs(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/coop_mode.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/wheelchair_msg
)
_generate_srv_nodejs(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door_mode.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/wheelchair_msg
)

### Generating Module File
_generate_module_nodejs(wheelchair_msg
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/wheelchair_msg
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(wheelchair_msg_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(wheelchair_msg_generate_messages wheelchair_msg_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/caselidar.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_nodejs _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/coop_mode.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_nodejs _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/doormsg.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_nodejs _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/normal.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_nodejs _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door_mode.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_nodejs _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_nodejs _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/coop.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_nodejs _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/normal_mode.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_nodejs _wheelchair_msg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(wheelchair_msg_gennodejs)
add_dependencies(wheelchair_msg_gennodejs wheelchair_msg_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS wheelchair_msg_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/normal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wheelchair_msg
)
_generate_msg_py(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/caselidar.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wheelchair_msg
)
_generate_msg_py(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/coop.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wheelchair_msg
)
_generate_msg_py(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/doormsg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wheelchair_msg
)

### Generating Services
_generate_srv_py(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wheelchair_msg
)
_generate_srv_py(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/normal_mode.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wheelchair_msg
)
_generate_srv_py(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/coop_mode.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wheelchair_msg
)
_generate_srv_py(wheelchair_msg
  "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door_mode.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wheelchair_msg
)

### Generating Module File
_generate_module_py(wheelchair_msg
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wheelchair_msg
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(wheelchair_msg_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(wheelchair_msg_generate_messages wheelchair_msg_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/caselidar.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_py _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/coop_mode.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_py _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/doormsg.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_py _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/normal.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_py _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door_mode.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_py _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/door.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_py _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/msg/coop.msg" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_py _wheelchair_msg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/taehyung/catkin_ws/src/wheelchair/ros_auto_wheelchair/wheelchair_msg/srv/normal_mode.srv" NAME_WE)
add_dependencies(wheelchair_msg_generate_messages_py _wheelchair_msg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(wheelchair_msg_genpy)
add_dependencies(wheelchair_msg_genpy wheelchair_msg_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS wheelchair_msg_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/wheelchair_msg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/wheelchair_msg
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(wheelchair_msg_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/wheelchair_msg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/wheelchair_msg
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(wheelchair_msg_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/wheelchair_msg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/wheelchair_msg
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(wheelchair_msg_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/wheelchair_msg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/wheelchair_msg
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(wheelchair_msg_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wheelchair_msg)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wheelchair_msg\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/wheelchair_msg
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(wheelchair_msg_generate_messages_py std_msgs_generate_messages_py)
endif()
