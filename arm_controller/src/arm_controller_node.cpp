#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/joint_state.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"
#include <chrono>
#include <functional>
#include <memory>
#include <string>
#include <vector>
using namespace std::chrono_literals;

class ArmControlNode : public rclcpp::Node
{
public:
    ArmControlNode()
        : Node("arm_control_node")
    {

        // Publisher per inviare comandi di posizione al controller
        position_publisher_ = this->create_publisher<std_msgs::msg::Float64MultiArray>("/JointPositionController/commands", 10);
        timer_ = this->create_wall_timer(
             500ms, std::bind(&ArmControlNode::positionCommandCallback, this));
        
        // Subscriber per ricevere lo stato delle giunture
        joint_state_subscriber_ = this->create_subscription<sensor_msgs::msg::JointState>(
            "/joint_states", 10,
            std::bind(&ArmControlNode::jointStateCallback, this, std::placeholders::_1));

        input_data.resize(4);
    	std::cout << "Enter joints' position (4 double):\n";
      	std::cin >> input_data[0] >> input_data[1] >> input_data[2] >> input_data[3];
        
        
        RCLCPP_INFO(this->get_logger(), "Arm Control Node started and ready for external position commands.");
    }

private:
    void positionCommandCallback()
    {
       
        auto pub_msg = std_msgs::msg::Float64MultiArray();
        for (size_t i = 0; i < 4; ++i) {
            pub_msg.data.push_back(static_cast<double>(input_data[i])); 
        }

        // Pubblica il messaggio
        position_publisher_->publish(pub_msg);
        RCLCPP_INFO(this->get_logger(), "Position command received and published.");
    }

    void jointStateCallback(const sensor_msgs::msg::JointState::SharedPtr msg)
    {
        RCLCPP_INFO(this->get_logger(), "Joint positions:");
        for (size_t i = 0; i < msg->name.size(); ++i)
        {
            RCLCPP_INFO(this->get_logger(), "  %s: %f", msg->name[i].c_str(), msg->position[i]);
        }
    }

    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr position_publisher_;
    rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr joint_state_subscriber_;
    std::vector<float> input_data;

};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ArmControlNode>());
    rclcpp::shutdown();
    return 0;

}

