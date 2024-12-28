#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/joint_state.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"

class ArmControlNode : public rclcpp::Node
{
public:
    ArmControlNode()
        : Node("arm_control_node")
    {
        // Publisher per inviare comandi di posizione al controller
        position_publisher_ = this->create_publisher<std_msgs::msg::Float64MultiArray>("/JointPositionController/commands", 10);
        timer_ = this->create_wall_timer(
             500ms, std::bind(&ArmController::positionCommandCallback, this));
        
        // Subscriber per ricevere lo stato delle giunture
        joint_state_subscriber_ = this->create_subscription<sensor_msgs::msg::JointState>(
            "/joint_states", 10,
            std::bind(&ArmControlNode::jointStateCallback, this, std::placeholders::_1));
        
        
        RCLCPP_INFO(this->get_logger(), "Arm Control Node started and ready for external position commands.");
    }

private:
    void positionCommandCallback()
    {
        auto msg = std_msgs::msg::Float64MultiArray();
        msg.data = {0.0, 0.5, 1.0, 0.5};
        
        // Invia il comando di posizione ricevuto al controller
        position_publisher_->publish(*msg);
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

};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ArmControlNode>());
    rclcpp::shutdown();
    return 0;

}
