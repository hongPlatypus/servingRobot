// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from driving1_interfaces:srv/NotifySoldout.idl
// generated code does not contain a copyright notice

#ifndef DRIVING1_INTERFACES__SRV__DETAIL__NOTIFY_SOLDOUT__TRAITS_HPP_
#define DRIVING1_INTERFACES__SRV__DETAIL__NOTIFY_SOLDOUT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "driving1_interfaces/srv/detail/notify_soldout__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace driving1_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const NotifySoldout_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const NotifySoldout_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const NotifySoldout_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace driving1_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use driving1_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const driving1_interfaces::srv::NotifySoldout_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  driving1_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use driving1_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const driving1_interfaces::srv::NotifySoldout_Request & msg)
{
  return driving1_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<driving1_interfaces::srv::NotifySoldout_Request>()
{
  return "driving1_interfaces::srv::NotifySoldout_Request";
}

template<>
inline const char * name<driving1_interfaces::srv::NotifySoldout_Request>()
{
  return "driving1_interfaces/srv/NotifySoldout_Request";
}

template<>
struct has_fixed_size<driving1_interfaces::srv::NotifySoldout_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<driving1_interfaces::srv::NotifySoldout_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<driving1_interfaces::srv::NotifySoldout_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace driving1_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const NotifySoldout_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: response_message
  {
    out << "response_message: ";
    rosidl_generator_traits::value_to_yaml(msg.response_message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const NotifySoldout_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: response_message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "response_message: ";
    rosidl_generator_traits::value_to_yaml(msg.response_message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const NotifySoldout_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace driving1_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use driving1_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const driving1_interfaces::srv::NotifySoldout_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  driving1_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use driving1_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const driving1_interfaces::srv::NotifySoldout_Response & msg)
{
  return driving1_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<driving1_interfaces::srv::NotifySoldout_Response>()
{
  return "driving1_interfaces::srv::NotifySoldout_Response";
}

template<>
inline const char * name<driving1_interfaces::srv::NotifySoldout_Response>()
{
  return "driving1_interfaces/srv/NotifySoldout_Response";
}

template<>
struct has_fixed_size<driving1_interfaces::srv::NotifySoldout_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<driving1_interfaces::srv::NotifySoldout_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<driving1_interfaces::srv::NotifySoldout_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<driving1_interfaces::srv::NotifySoldout>()
{
  return "driving1_interfaces::srv::NotifySoldout";
}

template<>
inline const char * name<driving1_interfaces::srv::NotifySoldout>()
{
  return "driving1_interfaces/srv/NotifySoldout";
}

template<>
struct has_fixed_size<driving1_interfaces::srv::NotifySoldout>
  : std::integral_constant<
    bool,
    has_fixed_size<driving1_interfaces::srv::NotifySoldout_Request>::value &&
    has_fixed_size<driving1_interfaces::srv::NotifySoldout_Response>::value
  >
{
};

template<>
struct has_bounded_size<driving1_interfaces::srv::NotifySoldout>
  : std::integral_constant<
    bool,
    has_bounded_size<driving1_interfaces::srv::NotifySoldout_Request>::value &&
    has_bounded_size<driving1_interfaces::srv::NotifySoldout_Response>::value
  >
{
};

template<>
struct is_service<driving1_interfaces::srv::NotifySoldout>
  : std::true_type
{
};

template<>
struct is_service_request<driving1_interfaces::srv::NotifySoldout_Request>
  : std::true_type
{
};

template<>
struct is_service_response<driving1_interfaces::srv::NotifySoldout_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // DRIVING1_INTERFACES__SRV__DETAIL__NOTIFY_SOLDOUT__TRAITS_HPP_
