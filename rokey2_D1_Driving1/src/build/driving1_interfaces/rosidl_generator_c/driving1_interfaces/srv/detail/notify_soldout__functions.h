// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from driving1_interfaces:srv/NotifySoldout.idl
// generated code does not contain a copyright notice

#ifndef DRIVING1_INTERFACES__SRV__DETAIL__NOTIFY_SOLDOUT__FUNCTIONS_H_
#define DRIVING1_INTERFACES__SRV__DETAIL__NOTIFY_SOLDOUT__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "driving1_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "driving1_interfaces/srv/detail/notify_soldout__struct.h"

/// Initialize srv/NotifySoldout message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * driving1_interfaces__srv__NotifySoldout_Request
 * )) before or use
 * driving1_interfaces__srv__NotifySoldout_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
bool
driving1_interfaces__srv__NotifySoldout_Request__init(driving1_interfaces__srv__NotifySoldout_Request * msg);

/// Finalize srv/NotifySoldout message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
void
driving1_interfaces__srv__NotifySoldout_Request__fini(driving1_interfaces__srv__NotifySoldout_Request * msg);

/// Create srv/NotifySoldout message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * driving1_interfaces__srv__NotifySoldout_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
driving1_interfaces__srv__NotifySoldout_Request *
driving1_interfaces__srv__NotifySoldout_Request__create();

/// Destroy srv/NotifySoldout message.
/**
 * It calls
 * driving1_interfaces__srv__NotifySoldout_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
void
driving1_interfaces__srv__NotifySoldout_Request__destroy(driving1_interfaces__srv__NotifySoldout_Request * msg);

/// Check for srv/NotifySoldout message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
bool
driving1_interfaces__srv__NotifySoldout_Request__are_equal(const driving1_interfaces__srv__NotifySoldout_Request * lhs, const driving1_interfaces__srv__NotifySoldout_Request * rhs);

/// Copy a srv/NotifySoldout message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
bool
driving1_interfaces__srv__NotifySoldout_Request__copy(
  const driving1_interfaces__srv__NotifySoldout_Request * input,
  driving1_interfaces__srv__NotifySoldout_Request * output);

/// Initialize array of srv/NotifySoldout messages.
/**
 * It allocates the memory for the number of elements and calls
 * driving1_interfaces__srv__NotifySoldout_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
bool
driving1_interfaces__srv__NotifySoldout_Request__Sequence__init(driving1_interfaces__srv__NotifySoldout_Request__Sequence * array, size_t size);

/// Finalize array of srv/NotifySoldout messages.
/**
 * It calls
 * driving1_interfaces__srv__NotifySoldout_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
void
driving1_interfaces__srv__NotifySoldout_Request__Sequence__fini(driving1_interfaces__srv__NotifySoldout_Request__Sequence * array);

/// Create array of srv/NotifySoldout messages.
/**
 * It allocates the memory for the array and calls
 * driving1_interfaces__srv__NotifySoldout_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
driving1_interfaces__srv__NotifySoldout_Request__Sequence *
driving1_interfaces__srv__NotifySoldout_Request__Sequence__create(size_t size);

/// Destroy array of srv/NotifySoldout messages.
/**
 * It calls
 * driving1_interfaces__srv__NotifySoldout_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
void
driving1_interfaces__srv__NotifySoldout_Request__Sequence__destroy(driving1_interfaces__srv__NotifySoldout_Request__Sequence * array);

/// Check for srv/NotifySoldout message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
bool
driving1_interfaces__srv__NotifySoldout_Request__Sequence__are_equal(const driving1_interfaces__srv__NotifySoldout_Request__Sequence * lhs, const driving1_interfaces__srv__NotifySoldout_Request__Sequence * rhs);

/// Copy an array of srv/NotifySoldout messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
bool
driving1_interfaces__srv__NotifySoldout_Request__Sequence__copy(
  const driving1_interfaces__srv__NotifySoldout_Request__Sequence * input,
  driving1_interfaces__srv__NotifySoldout_Request__Sequence * output);

/// Initialize srv/NotifySoldout message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * driving1_interfaces__srv__NotifySoldout_Response
 * )) before or use
 * driving1_interfaces__srv__NotifySoldout_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
bool
driving1_interfaces__srv__NotifySoldout_Response__init(driving1_interfaces__srv__NotifySoldout_Response * msg);

/// Finalize srv/NotifySoldout message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
void
driving1_interfaces__srv__NotifySoldout_Response__fini(driving1_interfaces__srv__NotifySoldout_Response * msg);

/// Create srv/NotifySoldout message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * driving1_interfaces__srv__NotifySoldout_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
driving1_interfaces__srv__NotifySoldout_Response *
driving1_interfaces__srv__NotifySoldout_Response__create();

/// Destroy srv/NotifySoldout message.
/**
 * It calls
 * driving1_interfaces__srv__NotifySoldout_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
void
driving1_interfaces__srv__NotifySoldout_Response__destroy(driving1_interfaces__srv__NotifySoldout_Response * msg);

/// Check for srv/NotifySoldout message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
bool
driving1_interfaces__srv__NotifySoldout_Response__are_equal(const driving1_interfaces__srv__NotifySoldout_Response * lhs, const driving1_interfaces__srv__NotifySoldout_Response * rhs);

/// Copy a srv/NotifySoldout message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
bool
driving1_interfaces__srv__NotifySoldout_Response__copy(
  const driving1_interfaces__srv__NotifySoldout_Response * input,
  driving1_interfaces__srv__NotifySoldout_Response * output);

/// Initialize array of srv/NotifySoldout messages.
/**
 * It allocates the memory for the number of elements and calls
 * driving1_interfaces__srv__NotifySoldout_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
bool
driving1_interfaces__srv__NotifySoldout_Response__Sequence__init(driving1_interfaces__srv__NotifySoldout_Response__Sequence * array, size_t size);

/// Finalize array of srv/NotifySoldout messages.
/**
 * It calls
 * driving1_interfaces__srv__NotifySoldout_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
void
driving1_interfaces__srv__NotifySoldout_Response__Sequence__fini(driving1_interfaces__srv__NotifySoldout_Response__Sequence * array);

/// Create array of srv/NotifySoldout messages.
/**
 * It allocates the memory for the array and calls
 * driving1_interfaces__srv__NotifySoldout_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
driving1_interfaces__srv__NotifySoldout_Response__Sequence *
driving1_interfaces__srv__NotifySoldout_Response__Sequence__create(size_t size);

/// Destroy array of srv/NotifySoldout messages.
/**
 * It calls
 * driving1_interfaces__srv__NotifySoldout_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
void
driving1_interfaces__srv__NotifySoldout_Response__Sequence__destroy(driving1_interfaces__srv__NotifySoldout_Response__Sequence * array);

/// Check for srv/NotifySoldout message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
bool
driving1_interfaces__srv__NotifySoldout_Response__Sequence__are_equal(const driving1_interfaces__srv__NotifySoldout_Response__Sequence * lhs, const driving1_interfaces__srv__NotifySoldout_Response__Sequence * rhs);

/// Copy an array of srv/NotifySoldout messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_driving1_interfaces
bool
driving1_interfaces__srv__NotifySoldout_Response__Sequence__copy(
  const driving1_interfaces__srv__NotifySoldout_Response__Sequence * input,
  driving1_interfaces__srv__NotifySoldout_Response__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // DRIVING1_INTERFACES__SRV__DETAIL__NOTIFY_SOLDOUT__FUNCTIONS_H_
