// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from project3_interfaces:msg/TableCommand.idl
// generated code does not contain a copyright notice

#ifndef PROJECT3_INTERFACES__MSG__DETAIL__TABLE_COMMAND__TRAITS_HPP_
#define PROJECT3_INTERFACES__MSG__DETAIL__TABLE_COMMAND__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "project3_interfaces/msg/detail/table_command__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace project3_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const TableCommand & msg,
  std::ostream & out)
{
  out << "{";
  // member: to_robot
  {
    out << "to_robot: ";
    rosidl_generator_traits::value_to_yaml(msg.to_robot, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TableCommand & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: to_robot
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "to_robot: ";
    rosidl_generator_traits::value_to_yaml(msg.to_robot, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TableCommand & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace project3_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use project3_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const project3_interfaces::msg::TableCommand & msg,
  std::ostream & out, size_t indentation = 0)
{
  project3_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use project3_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const project3_interfaces::msg::TableCommand & msg)
{
  return project3_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<project3_interfaces::msg::TableCommand>()
{
  return "project3_interfaces::msg::TableCommand";
}

template<>
inline const char * name<project3_interfaces::msg::TableCommand>()
{
  return "project3_interfaces/msg/TableCommand";
}

template<>
struct has_fixed_size<project3_interfaces::msg::TableCommand>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<project3_interfaces::msg::TableCommand>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<project3_interfaces::msg::TableCommand>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PROJECT3_INTERFACES__MSG__DETAIL__TABLE_COMMAND__TRAITS_HPP_
