// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from project3_interfaces:msg/TableCommand.idl
// generated code does not contain a copyright notice

#ifndef PROJECT3_INTERFACES__MSG__DETAIL__TABLE_COMMAND__STRUCT_H_
#define PROJECT3_INTERFACES__MSG__DETAIL__TABLE_COMMAND__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'to_robot'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/TableCommand in the package project3_interfaces.
typedef struct project3_interfaces__msg__TableCommand
{
  rosidl_runtime_c__String to_robot;
} project3_interfaces__msg__TableCommand;

// Struct for a sequence of project3_interfaces__msg__TableCommand.
typedef struct project3_interfaces__msg__TableCommand__Sequence
{
  project3_interfaces__msg__TableCommand * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project3_interfaces__msg__TableCommand__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PROJECT3_INTERFACES__MSG__DETAIL__TABLE_COMMAND__STRUCT_H_
