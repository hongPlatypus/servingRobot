// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from project3_interfaces:msg/TableCommand.idl
// generated code does not contain a copyright notice

#ifndef PROJECT3_INTERFACES__MSG__DETAIL__TABLE_COMMAND__STRUCT_HPP_
#define PROJECT3_INTERFACES__MSG__DETAIL__TABLE_COMMAND__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__project3_interfaces__msg__TableCommand __attribute__((deprecated))
#else
# define DEPRECATED__project3_interfaces__msg__TableCommand __declspec(deprecated)
#endif

namespace project3_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TableCommand_
{
  using Type = TableCommand_<ContainerAllocator>;

  explicit TableCommand_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->to_robot = "";
    }
  }

  explicit TableCommand_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : to_robot(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->to_robot = "";
    }
  }

  // field types and members
  using _to_robot_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _to_robot_type to_robot;

  // setters for named parameter idiom
  Type & set__to_robot(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->to_robot = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    project3_interfaces::msg::TableCommand_<ContainerAllocator> *;
  using ConstRawPtr =
    const project3_interfaces::msg::TableCommand_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<project3_interfaces::msg::TableCommand_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<project3_interfaces::msg::TableCommand_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      project3_interfaces::msg::TableCommand_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<project3_interfaces::msg::TableCommand_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      project3_interfaces::msg::TableCommand_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<project3_interfaces::msg::TableCommand_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<project3_interfaces::msg::TableCommand_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<project3_interfaces::msg::TableCommand_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__project3_interfaces__msg__TableCommand
    std::shared_ptr<project3_interfaces::msg::TableCommand_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__project3_interfaces__msg__TableCommand
    std::shared_ptr<project3_interfaces::msg::TableCommand_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TableCommand_ & other) const
  {
    if (this->to_robot != other.to_robot) {
      return false;
    }
    return true;
  }
  bool operator!=(const TableCommand_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TableCommand_

// alias to use template instance with default allocator
using TableCommand =
  project3_interfaces::msg::TableCommand_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace project3_interfaces

#endif  // PROJECT3_INTERFACES__MSG__DETAIL__TABLE_COMMAND__STRUCT_HPP_
