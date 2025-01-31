// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from driving1_interfaces:srv/NotifySoldout.idl
// generated code does not contain a copyright notice

#ifndef DRIVING1_INTERFACES__SRV__DETAIL__NOTIFY_SOLDOUT__BUILDER_HPP_
#define DRIVING1_INTERFACES__SRV__DETAIL__NOTIFY_SOLDOUT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "driving1_interfaces/srv/detail/notify_soldout__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace driving1_interfaces
{

namespace srv
{

namespace builder
{

class Init_NotifySoldout_Request_message
{
public:
  Init_NotifySoldout_Request_message()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::driving1_interfaces::srv::NotifySoldout_Request message(::driving1_interfaces::srv::NotifySoldout_Request::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::driving1_interfaces::srv::NotifySoldout_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::driving1_interfaces::srv::NotifySoldout_Request>()
{
  return driving1_interfaces::srv::builder::Init_NotifySoldout_Request_message();
}

}  // namespace driving1_interfaces


namespace driving1_interfaces
{

namespace srv
{

namespace builder
{

class Init_NotifySoldout_Response_response_message
{
public:
  explicit Init_NotifySoldout_Response_response_message(::driving1_interfaces::srv::NotifySoldout_Response & msg)
  : msg_(msg)
  {}
  ::driving1_interfaces::srv::NotifySoldout_Response response_message(::driving1_interfaces::srv::NotifySoldout_Response::_response_message_type arg)
  {
    msg_.response_message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::driving1_interfaces::srv::NotifySoldout_Response msg_;
};

class Init_NotifySoldout_Response_success
{
public:
  Init_NotifySoldout_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_NotifySoldout_Response_response_message success(::driving1_interfaces::srv::NotifySoldout_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_NotifySoldout_Response_response_message(msg_);
  }

private:
  ::driving1_interfaces::srv::NotifySoldout_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::driving1_interfaces::srv::NotifySoldout_Response>()
{
  return driving1_interfaces::srv::builder::Init_NotifySoldout_Response_success();
}

}  // namespace driving1_interfaces

#endif  // DRIVING1_INTERFACES__SRV__DETAIL__NOTIFY_SOLDOUT__BUILDER_HPP_
