import rclpy
from rclpy.node import Node
from example_interfaces.srv import Trigger


class SoldoutServer(Node):
    def __init__(self):
        super().__init__('soldout_server')

        # Create a service for /soldout
        self.srv = self.create_service(Trigger, '/soldout', self.soldout_callback)
        self.get_logger().info('Soldout service is ready.')

    def soldout_callback(self, request, response):
        """
        Callback for the /soldout service.
        Handles the incoming sold-out notifications.

        :param request: Trigger.Request object containing the request data.
        :param response: Trigger.Response object to be sent back.
        :return: Trigger.Response
        """
        try:
            # Log the received soldout message
            soldout_message = request.message  # The sold-out message sent by the client
            self.get_logger().info(f"Received sold-out notification: {soldout_message}")

            # Process the soldout message (e.g., log to a database or update a display)
            # Example: Simply log the message and mark the response as successful
            response.success = True
            response.message = f"Sold-out notification for '{soldout_message}' received successfully."
        except Exception as e:
            self.get_logger().error(f"Error processing sold-out notification: {e}")
            response.success = False
            response.message = "Failed to process sold-out notification."

        return response


def main(args=None):
    rclpy.init(args=args)

    soldout_server = SoldoutServer()

    try:
        rclpy.spin(soldout_server)
    except KeyboardInterrupt:
        soldout_server.get_logger().info("Soldout server shutting down.")
    finally:
        soldout_server.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
