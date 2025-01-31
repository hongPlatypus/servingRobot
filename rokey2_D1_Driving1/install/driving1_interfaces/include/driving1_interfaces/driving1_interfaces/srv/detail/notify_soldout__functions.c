// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from driving1_interfaces:srv/NotifySoldout.idl
// generated code does not contain a copyright notice
#include "driving1_interfaces/srv/detail/notify_soldout__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

bool
driving1_interfaces__srv__NotifySoldout_Request__init(driving1_interfaces__srv__NotifySoldout_Request * msg)
{
  if (!msg) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    driving1_interfaces__srv__NotifySoldout_Request__fini(msg);
    return false;
  }
  return true;
}

void
driving1_interfaces__srv__NotifySoldout_Request__fini(driving1_interfaces__srv__NotifySoldout_Request * msg)
{
  if (!msg) {
    return;
  }
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
driving1_interfaces__srv__NotifySoldout_Request__are_equal(const driving1_interfaces__srv__NotifySoldout_Request * lhs, const driving1_interfaces__srv__NotifySoldout_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
driving1_interfaces__srv__NotifySoldout_Request__copy(
  const driving1_interfaces__srv__NotifySoldout_Request * input,
  driving1_interfaces__srv__NotifySoldout_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

driving1_interfaces__srv__NotifySoldout_Request *
driving1_interfaces__srv__NotifySoldout_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  driving1_interfaces__srv__NotifySoldout_Request * msg = (driving1_interfaces__srv__NotifySoldout_Request *)allocator.allocate(sizeof(driving1_interfaces__srv__NotifySoldout_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(driving1_interfaces__srv__NotifySoldout_Request));
  bool success = driving1_interfaces__srv__NotifySoldout_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
driving1_interfaces__srv__NotifySoldout_Request__destroy(driving1_interfaces__srv__NotifySoldout_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    driving1_interfaces__srv__NotifySoldout_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
driving1_interfaces__srv__NotifySoldout_Request__Sequence__init(driving1_interfaces__srv__NotifySoldout_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  driving1_interfaces__srv__NotifySoldout_Request * data = NULL;

  if (size) {
    data = (driving1_interfaces__srv__NotifySoldout_Request *)allocator.zero_allocate(size, sizeof(driving1_interfaces__srv__NotifySoldout_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = driving1_interfaces__srv__NotifySoldout_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        driving1_interfaces__srv__NotifySoldout_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
driving1_interfaces__srv__NotifySoldout_Request__Sequence__fini(driving1_interfaces__srv__NotifySoldout_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      driving1_interfaces__srv__NotifySoldout_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

driving1_interfaces__srv__NotifySoldout_Request__Sequence *
driving1_interfaces__srv__NotifySoldout_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  driving1_interfaces__srv__NotifySoldout_Request__Sequence * array = (driving1_interfaces__srv__NotifySoldout_Request__Sequence *)allocator.allocate(sizeof(driving1_interfaces__srv__NotifySoldout_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = driving1_interfaces__srv__NotifySoldout_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
driving1_interfaces__srv__NotifySoldout_Request__Sequence__destroy(driving1_interfaces__srv__NotifySoldout_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    driving1_interfaces__srv__NotifySoldout_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
driving1_interfaces__srv__NotifySoldout_Request__Sequence__are_equal(const driving1_interfaces__srv__NotifySoldout_Request__Sequence * lhs, const driving1_interfaces__srv__NotifySoldout_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!driving1_interfaces__srv__NotifySoldout_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
driving1_interfaces__srv__NotifySoldout_Request__Sequence__copy(
  const driving1_interfaces__srv__NotifySoldout_Request__Sequence * input,
  driving1_interfaces__srv__NotifySoldout_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(driving1_interfaces__srv__NotifySoldout_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    driving1_interfaces__srv__NotifySoldout_Request * data =
      (driving1_interfaces__srv__NotifySoldout_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!driving1_interfaces__srv__NotifySoldout_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          driving1_interfaces__srv__NotifySoldout_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!driving1_interfaces__srv__NotifySoldout_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `response_message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
driving1_interfaces__srv__NotifySoldout_Response__init(driving1_interfaces__srv__NotifySoldout_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // response_message
  if (!rosidl_runtime_c__String__init(&msg->response_message)) {
    driving1_interfaces__srv__NotifySoldout_Response__fini(msg);
    return false;
  }
  return true;
}

void
driving1_interfaces__srv__NotifySoldout_Response__fini(driving1_interfaces__srv__NotifySoldout_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // response_message
  rosidl_runtime_c__String__fini(&msg->response_message);
}

bool
driving1_interfaces__srv__NotifySoldout_Response__are_equal(const driving1_interfaces__srv__NotifySoldout_Response * lhs, const driving1_interfaces__srv__NotifySoldout_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // response_message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->response_message), &(rhs->response_message)))
  {
    return false;
  }
  return true;
}

bool
driving1_interfaces__srv__NotifySoldout_Response__copy(
  const driving1_interfaces__srv__NotifySoldout_Response * input,
  driving1_interfaces__srv__NotifySoldout_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // response_message
  if (!rosidl_runtime_c__String__copy(
      &(input->response_message), &(output->response_message)))
  {
    return false;
  }
  return true;
}

driving1_interfaces__srv__NotifySoldout_Response *
driving1_interfaces__srv__NotifySoldout_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  driving1_interfaces__srv__NotifySoldout_Response * msg = (driving1_interfaces__srv__NotifySoldout_Response *)allocator.allocate(sizeof(driving1_interfaces__srv__NotifySoldout_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(driving1_interfaces__srv__NotifySoldout_Response));
  bool success = driving1_interfaces__srv__NotifySoldout_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
driving1_interfaces__srv__NotifySoldout_Response__destroy(driving1_interfaces__srv__NotifySoldout_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    driving1_interfaces__srv__NotifySoldout_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
driving1_interfaces__srv__NotifySoldout_Response__Sequence__init(driving1_interfaces__srv__NotifySoldout_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  driving1_interfaces__srv__NotifySoldout_Response * data = NULL;

  if (size) {
    data = (driving1_interfaces__srv__NotifySoldout_Response *)allocator.zero_allocate(size, sizeof(driving1_interfaces__srv__NotifySoldout_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = driving1_interfaces__srv__NotifySoldout_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        driving1_interfaces__srv__NotifySoldout_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
driving1_interfaces__srv__NotifySoldout_Response__Sequence__fini(driving1_interfaces__srv__NotifySoldout_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      driving1_interfaces__srv__NotifySoldout_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

driving1_interfaces__srv__NotifySoldout_Response__Sequence *
driving1_interfaces__srv__NotifySoldout_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  driving1_interfaces__srv__NotifySoldout_Response__Sequence * array = (driving1_interfaces__srv__NotifySoldout_Response__Sequence *)allocator.allocate(sizeof(driving1_interfaces__srv__NotifySoldout_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = driving1_interfaces__srv__NotifySoldout_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
driving1_interfaces__srv__NotifySoldout_Response__Sequence__destroy(driving1_interfaces__srv__NotifySoldout_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    driving1_interfaces__srv__NotifySoldout_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
driving1_interfaces__srv__NotifySoldout_Response__Sequence__are_equal(const driving1_interfaces__srv__NotifySoldout_Response__Sequence * lhs, const driving1_interfaces__srv__NotifySoldout_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!driving1_interfaces__srv__NotifySoldout_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
driving1_interfaces__srv__NotifySoldout_Response__Sequence__copy(
  const driving1_interfaces__srv__NotifySoldout_Response__Sequence * input,
  driving1_interfaces__srv__NotifySoldout_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(driving1_interfaces__srv__NotifySoldout_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    driving1_interfaces__srv__NotifySoldout_Response * data =
      (driving1_interfaces__srv__NotifySoldout_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!driving1_interfaces__srv__NotifySoldout_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          driving1_interfaces__srv__NotifySoldout_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!driving1_interfaces__srv__NotifySoldout_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
