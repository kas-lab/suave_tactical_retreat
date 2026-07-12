// Copyright 2026 KAS-lab
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <algorithm>
#include <chrono>
#include <memory>
#include <mutex>
#include <string>
#include <thread>
#include <vector>

#include "aal_msgs/srv/adapt_architecture.hpp"
#include "adapt_x_msgs/srv/fetch_plan_from_desired_features.hpp"
#include "ament_index_cpp/get_package_share_directory.hpp"
#include "behaviortree_cpp/bt_factory.h"
#include "behaviortree_cpp/utils/shared_library.h"
#include "gtest/gtest.h"
#include "mavros_msgs/msg/state.hpp"
#include "mavros_msgs/srv/command_bool.hpp"
#include "mavros_msgs/srv/set_mode.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/bool.hpp"
#include "std_srvs/srv/empty.hpp"
#include "suave_bt/action_arm_thrusters.hpp"
#include "suave_bt/action_inspect_pipeline.hpp"
#include "suave_bt/action_search_pipeline.hpp"
#include "suave_bt/action_set_guided_mode.hpp"
#include "suave_bt/suave_mission.hpp"

using namespace std::chrono_literals;

namespace
{

struct ReconfigureGoal
{
  std::vector<std::string> active_features;
  std::vector<std::string> inactive_features;
};

void RegisterSuaveRebetmcNodes(BT::BehaviorTreeFactory & factory)
{
  const auto adapt_x_bt_pkgpath = ament_index_cpp::get_package_share_directory("adapt_x_bt");
  const auto adapt_x_bt_plugin_path =
    adapt_x_bt_pkgpath + "/bt_plugins/" + BT::SharedLibrary::getOSName("adapt_x_bt_nodes");
  factory.registerFromPlugin(adapt_x_bt_plugin_path);

  factory.registerNodeType<suave_bt::ArmThrusters>("arm_thrusters");
  factory.registerNodeType<suave_bt::InspectPipeline>("inspect_pipeline");
  factory.registerNodeType<suave_bt::SearchPipeline>("search_pipeline");
  factory.registerNodeType<suave_bt::SetGuidedMode>("set_guided_mode");
}

BT::Tree CreateSuaveRebetmcTree(
  BT::BehaviorTreeFactory & factory,
  const std::shared_ptr<suave_bt::SuaveMission> & node)
{
  auto blackboard = BT::Blackboard::create();
  blackboard->set<std::shared_ptr<suave_bt::SuaveMission>>("node", node);

  return factory.createTreeFromFile(SUAVE_REBETMC_BT_XML, blackboard);
}

class MockSuaveRuntime : public rclcpp::Node
{
public:
  using FetchPlanSrv = adapt_x_msgs::srv::FetchPlanFromDesiredFeatures;
  using AdaptSrv = aal_msgs::srv::AdaptArchitecture;

  MockSuaveRuntime()
  : Node("mock_suave_rebetmc_bt_runtime")
  {
    fetch_plan_service_ = create_service<FetchPlanSrv>(
      "/fetch_plan_from_desired_features",
      [this](
        const FetchPlanSrv::Request::SharedPtr request,
        FetchPlanSrv::Response::SharedPtr response)
      {
        {
          std::lock_guard<std::mutex> lock(mutex_);
          received_goals_.push_back(
            ReconfigureGoal{
              request->desired_features.active_features,
              request->desired_features.inactive_features});
        }
        // The mock runtime doesn't need a real reconfiguration plan: the
        // decorator only forwards whatever fetch_plan_from_desired_features
        // returns to adapt_architecture, which is mocked below.
        response->adaptation_plan = {};
        response->success = true;
      });

    adapt_service_ = create_service<AdaptSrv>(
      "/adapt_architecture",
      [this](
        const AdaptSrv::Request::SharedPtr,
        AdaptSrv::Response::SharedPtr response)
      {
        adapt_requests_++;
        response->success = true;
      });

    arming_service_ = create_service<mavros_msgs::srv::CommandBool>(
      "mavros/cmd/arming",
      [this](
        const mavros_msgs::srv::CommandBool::Request::SharedPtr,
        mavros_msgs::srv::CommandBool::Response::SharedPtr response)
      {
        armed_requests_++;
        response->success = true;
      });

    set_mode_service_ = create_service<mavros_msgs::srv::SetMode>(
      "mavros/set_mode",
      [this](
        const mavros_msgs::srv::SetMode::Request::SharedPtr request,
        mavros_msgs::srv::SetMode::Response::SharedPtr response)
      {
        if (request->custom_mode == "GUIDED") {
          guided_requests_++;
        }
        response->mode_sent = true;
      });

    save_metrics_service_ = create_service<std_srvs::srv::Empty>(
      "mission_metrics/save",
      [this](
        const std_srvs::srv::Empty::Request::SharedPtr,
        std_srvs::srv::Empty::Response::SharedPtr)
      {
        save_metrics_requests_++;
      });

    mavros_state_pub_ = create_publisher<mavros_msgs::msg::State>("mavros/state", 10);
    pipeline_detected_pub_ = create_publisher<std_msgs::msg::Bool>("/pipeline/detected", 10);
    pipeline_inspected_pub_ = create_publisher<std_msgs::msg::Bool>("/pipeline/inspected", 10);

    publish_timer_ = create_wall_timer(
      20ms,
      [this]()
      {
        mavros_msgs::msg::State state;
        state.mode = "GUIDED";
        mavros_state_pub_->publish(state);

        std_msgs::msg::Bool detected;
        detected.data = true;
        pipeline_detected_pub_->publish(detected);

        std_msgs::msg::Bool inspected;
        inspected.data = true;
        pipeline_inspected_pub_->publish(inspected);
      });
  }

  std::vector<ReconfigureGoal> receivedGoals()
  {
    std::lock_guard<std::mutex> lock(mutex_);
    return received_goals_;
  }

  int armedRequests() const {return armed_requests_;}
  int guidedRequests() const {return guided_requests_;}
  int saveMetricsRequests() const {return save_metrics_requests_;}
  int adaptRequests() const {return adapt_requests_;}

private:
  mutable std::mutex mutex_;
  std::vector<ReconfigureGoal> received_goals_;
  int armed_requests_{0};
  int guided_requests_{0};
  int save_metrics_requests_{0};
  int adapt_requests_{0};

  rclcpp::Service<FetchPlanSrv>::SharedPtr fetch_plan_service_;
  rclcpp::Service<AdaptSrv>::SharedPtr adapt_service_;
  rclcpp::Service<mavros_msgs::srv::CommandBool>::SharedPtr arming_service_;
  rclcpp::Service<mavros_msgs::srv::SetMode>::SharedPtr set_mode_service_;
  rclcpp::Service<std_srvs::srv::Empty>::SharedPtr save_metrics_service_;
  rclcpp::Publisher<mavros_msgs::msg::State>::SharedPtr mavros_state_pub_;
  rclcpp::Publisher<std_msgs::msg::Bool>::SharedPtr pipeline_detected_pub_;
  rclcpp::Publisher<std_msgs::msg::Bool>::SharedPtr pipeline_inspected_pub_;
  rclcpp::TimerBase::SharedPtr publish_timer_;
};

bool ContainsGoalWithActiveNode(
  const std::vector<ReconfigureGoal> & goals,
  const std::string & active_node)
{
  return std::any_of(
    goals.begin(),
    goals.end(),
    [&active_node](const ReconfigureGoal & goal)
    {
      return std::find(
        goal.active_features.begin(), goal.active_features.end(), active_node) !=
      goal.active_features.end();
    });
}

}  // namespace

TEST(SuaveRebetmcBtXml, LoadsWithProductionRegistrations)
{
  auto node = std::make_shared<suave_bt::SuaveMission>("mission_node_xml_test");
  BT::BehaviorTreeFactory factory;
  RegisterSuaveRebetmcNodes(factory);
  factory.registerSimpleCondition(
    "is_mission_aborted", [&](const auto &) {
      return node->is_mission_aborted() ? BT::NodeStatus::SUCCESS : BT::NodeStatus::FAILURE;
    });

  EXPECT_NO_THROW(
  {
    auto tree = CreateSuaveRebetmcTree(factory, node);
    EXPECT_NE(tree.rootNode(), nullptr);
  });
}

TEST(SuaveRebetmcBtRuntime, CompletesWithMockedRuntimeEndpoints)
{
  auto mission_node = std::make_shared<suave_bt::SuaveMission>("mission_node_runtime_test");
  auto runtime_node = std::make_shared<MockSuaveRuntime>();

  BT::BehaviorTreeFactory factory;
  RegisterSuaveRebetmcNodes(factory);
  factory.registerSimpleCondition(
    "is_mission_aborted", [&](const auto &) {
      return mission_node->is_mission_aborted() ? BT::NodeStatus::SUCCESS :
      BT::NodeStatus::FAILURE;
    });
  auto tree = CreateSuaveRebetmcTree(factory, mission_node);

  rclcpp::executors::MultiThreadedExecutor executor;
  executor.add_node(mission_node->get_node_base_interface());
  executor.add_node(runtime_node);
  std::thread spin_thread([&executor]() {executor.spin();});

  BT::NodeStatus status = BT::NodeStatus::IDLE;
  const auto deadline = std::chrono::steady_clock::now() + 8s;
  while (rclcpp::ok() && std::chrono::steady_clock::now() < deadline) {
    status = tree.rootNode()->executeTick();
    if (status == BT::NodeStatus::SUCCESS || status == BT::NodeStatus::FAILURE) {
      break;
    }
    std::this_thread::sleep_for(20ms);
  }

  EXPECT_EQ(status, BT::NodeStatus::SUCCESS);
  mission_node->finish_mission();

  executor.cancel();
  spin_thread.join();

  const auto goals = runtime_node->receivedGoals();
  EXPECT_GE(runtime_node->armedRequests(), 1);
  EXPECT_GE(runtime_node->guidedRequests(), 1);
  EXPECT_GE(runtime_node->saveMetricsRequests(), 1);
  EXPECT_TRUE(ContainsGoalWithActiveNode(goals, "/f_generate_search_path"));
  EXPECT_TRUE(ContainsGoalWithActiveNode(goals, "/f_follow_pipeline_node"));
}

int main(int argc, char ** argv)
{
  testing::InitGoogleTest(&argc, argv);
  rclcpp::init(argc, argv);
  const int result = RUN_ALL_TESTS();
  rclcpp::shutdown();
  return result;
}
