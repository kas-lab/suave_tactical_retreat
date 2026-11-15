# Copyright 2026 KAS-lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

cmake_minimum_required(VERSION 3.8)
project(suave_tactical_retreat)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(ament_index_cpp REQUIRED)
find_package(behaviortree_cpp REQUIRED)
find_package(rclcpp REQUIRED)
find_package(suave_bt REQUIRED)
# find_package(adapt_x_bt REQUIRED)
find_package(adapt_x_msgs REQUIRED)

set(THIS_PACKAGE_DEPS
  ament_index_cpp
  behaviortree_cpp
  rclcpp
  suave_bt
  # adapt_x_bt
  adapt_x_msgs
)

add_executable(suave_tactical_retreat_bt src/suave_tactical_retreat_bt.cpp)
target_compile_features(suave_tactical_retreat_bt PUBLIC cxx_std_17)
ament_target_dependencies(suave_tactical_retreat_bt ${THIS_PACKAGE_DEPS})

install(TARGETS
  suave_tactical_retreat_bt
  DESTINATION lib/${PROJECT_NAME}
)

ament_python_install_package(${PROJECT_NAME})

install(DIRECTORY
  bts
  config
  launch
  models
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  find_package(ament_cmake_pytest REQUIRED)
  find_package(ament_lint_auto REQUIRED)
  find_package(adapt_x_msgs REQUIRED)
  find_package(mavros_msgs REQUIRED)
  find_package(rclcpp_action REQUIRED)
  find_package(std_msgs REQUIRED)
  find_package(std_srvs REQUIRED)

  set(ament_cmake_xmllint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()

  ament_add_pytest_test(
    test_copyright
    test/test_copyright.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
  ament_add_pytest_test(
    test_flake8
    test/test_flake8.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
  ament_add_pytest_test(
    test_pep257
    test/test_pep257.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
  ament_add_pytest_test(
    test_recovery_configuration
    test/test_recovery_configuration.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
  ament_add_pytest_test(
    test_suave_tactics_kb
    test/test_suave_tactics_kb.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
  # set_tests_properties(
  #   test_suave_tactics_kb
  #   PROPERTIES LABELS "pytest;typedb"
  # )

  # ament_add_gtest(test_suave_tactical_retreat_bt_xml test/test_suave_tactical_retreat_bt_xml.cpp)
  # target_compile_features(test_suave_tactical_retreat_bt_xml PUBLIC cxx_std_17)
  # target_compile_definitions(test_suave_tactical_retreat_bt_xml PRIVATE
  #   SUAVE_TACTICAL_RETREAT_BT_XML="${CMAKE_CURRENT_SOURCE_DIR}/bts/suave.xml")
  # file(MAKE_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/ros_log")
  # set_tests_properties(test_suave_tactical_retreat_bt_xml
  #   PROPERTIES ENVIRONMENT "ROS_LOG_DIR=${CMAKE_CURRENT_BINARY_DIR}/ros_log")
  # ament_target_dependencies(test_suave_tactical_retreat_bt_xml
  #   ament_index_cpp
  #   behaviortree_cpp
  #   rclcpp
  #   rclcpp_action
  #   mavros_msgs
  #   std_msgs
  #   std_srvs
  #   suave_bt
  # )
endif()

ament_package()
