// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from driving1_interfaces:srv/NotifySoldout.idl
// generated code does not contain a copyright notice

#ifndef DRIVING1_INTERFACES__SRV__DETAIL__NOTIFY_SOLDOUT__STRUCT_H_
#define DRIVING1_INTERFACES__SRV__DETAIL__NOTIFY_SOLDOUT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/NotifySoldout in the package driving1_interfaces.
typedef struct driving1_interfaces__srv__NotifySoldout_Request
{
  rosidl_runtime_c__String message;
} driving1_interfaces__srv__NotifySoldout_Request;

// Struct for a sequence of driving1_interfaces__srv__NotifySoldout_Request.
typedef struct driving1_interfaces__srv__NotifySoldout_Request__Sequence
{
  driving1_interfaces__srv__NotifySoldout_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} driving1_interfaces__srv__NotifySoldout_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'response_message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/NotifySoldout in the package driving1_interfaces.
typedef struct driving1_interfaces__srv__NotifySoldout_Response
{
  bool success;
  rosidl_runtime_c__String response_message;
} driving1_interfaces__srv__NotifySoldout_Response;

// Struct for a sequence of driving1_interfaces__srv__NotifySoldout_Response.
typedef struct driving1_interfaces__srv__NotifySoldout_Response__Sequence
{
  driving1_interfaces__srv__NotifySoldout_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} driving1_interfaces__srv__NotifySoldout_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DRIVING1_INTERFACES__SRV__DETAIL__NOTIFY_SOLDOUT__STRUCT_H_
