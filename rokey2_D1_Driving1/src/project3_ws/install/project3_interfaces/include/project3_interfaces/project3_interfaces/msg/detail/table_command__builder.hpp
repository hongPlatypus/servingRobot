// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from project3_interfaces:msg/TableCommand.idl
// generated code does not contain a copyright notice

#ifndef PROJECT3_INTERFACES__MSG__DETAIL__TABLE_COMMAND__BUILDER_HPP_
#define PROJECT3_INTERFACES__MSG__DETAIL__TABLE_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "project3_interfaces/msg/detail/table_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace project3_interfaces
{

namespace msg
{

namespace builder
{

class Init_TableCommand_to_robot
{
public:
  Init_TableCommand_to_robot()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::project3_interfaces::msg::TableCommand to_robot(::project3_interfaces::msg::TableCommand::_to_robot_type arg)
  {
    msg_.to_robot = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project3_interfaces::msg::TableCommand msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::project3_interfaces::msg::TableCommand>()
{
  return project3_interfaces::msg::builder::Init_TableCommand_to_robot();
}

}  // namespace project3_interfaces

#endif  // PROJECT3_INTERFACES__MSG__DETAIL__TABLE_COMMAND__BUILDER_HPP_
