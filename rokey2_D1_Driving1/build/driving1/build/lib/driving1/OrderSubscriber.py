import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class OrderSubscriber(Node):
    def __init__(self):
        super().__init__('order_subscriber')
        self.subscription = self.create_subscription(
            String,
            'order',  # 'order' 토픽을 구독
            self.listener_callback,
            10
        )
        self.get_logger().info("Order Subscriber Node has been started.")

    def listener_callback(self, msg):
        self.get_logger().info(f"Received: {msg.data}")  # 받은 메시지를 출력

def main(args=None):
    rclpy.init(args=args)
    node = OrderSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
