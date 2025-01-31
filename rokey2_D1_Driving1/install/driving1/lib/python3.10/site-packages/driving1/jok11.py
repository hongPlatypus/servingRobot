from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidget, QPushButton, QLabel
from PySide2.QtGui import QPixmap
import sys
import threading
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from std_msgs.msg import String
from driving1_interfaces.srv import NotifySoldout  # Custom ROS2 service type
from ui_order import Ui_MainWindow

class SoldoutServer(Node):
    def __init__(self):
        super().__init__('soldout_server')

        # Create a service for /soldout
        self.srv = self.create_service(NotifySoldout, '/soldout', self.soldout_callback)
        self.get_logger().info('Soldout service is ready.')

    def soldout_callback(self, request, response):
        """
        Callback for the /soldout service.
        Handles the incoming sold-out notifications.

        :param request: NotifySoldout.Request object containing the request data.
        :param response: NotifySoldout.Response object to be sent back.
        :return: NotifySoldout.Response
        """
        try:
            self.get_logger().info(f"Received /soldout request: {request.message}")

            # Simulate sold-out items
            soldout_items = request.message.split(',')
            self.get_logger().info(f"Sold-out items: {soldout_items}")

            response.success = True
            response.response_message = f"Handled sold-out items: {', '.join(soldout_items)}"
        except Exception as e:
            self.get_logger().error(f"Error in handling /soldout: {e}")
            response.success = False
            response.response_message = "Failed to handle sold-out notification."
        return response

class TableServer(Node):
    def __init__(self, table_number):
        super().__init__(f'table_server_{table_number}')
        self.table_number = table_number
        self.gui = None

        # Create the /soldout service
        self.soldout_service = self.create_service(
            NotifySoldout,  # Service type
            f'/soldout_table{table_number}',  # Service name
            self.handle_soldout  # Request handler callback
        )
        self.get_logger().info(f"Service '/soldout_table{table_number}' for Table {table_number} is ready.")

    def handle_soldout(self, request, response):
        try:
            self.get_logger().info(f"Received /soldout request: {request.message}")

            # Simulate sold-out items
            soldout_items = request.message.split(',')

            # Update the GUI with sold-out items
            if self.gui:
                self.gui.update_soldout_items(soldout_items)

            response.success = True
            response.response_message = f"Sold-out items processed: {', '.join(soldout_items)}"
        except Exception as e:
            self.get_logger().error(f"Error in handling /soldout: {e}")
            response.success = False
            response.response_message = "Failed to process sold-out notification."
        return response

class PublisherNode(Node):
    def __init__(self, table_number):
        super().__init__(f'publisher_table_{table_number}')
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            depth=10
        )
        self.publisher_ = self.create_publisher(String, f'/table{table_number}/message', qos_profile)

    def publish_message(self, message):
        msg = String()
        msg.data = message
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published: {message}")

class TableApp(QMainWindow):
    def __init__(self, ros_node, table_number):
        super().__init__()
        self.ros_node = ros_node
        self.table_number = table_number
        self.cart = {}
        self.soldout_items = set()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(f"Table {table_number}")
        self.setup_ui()

    def setup_ui(self):
        """Initialize the UI and connect signals."""
        self.ui.label.setPixmap(QPixmap("/home/junyong/t1_ws/p3/jok_l.jpg"))
        self.ui.label_2.setPixmap(QPixmap("/home/junyong/t1_ws/p3/images.jpeg"))
        self.ui.label_3.setPixmap(QPixmap("/home/junyong/t1_ws/p3/jinro.jpg"))
        self.ui.label_4.setPixmap(QPixmap("/home/junyong/t1_ws/p3/cham.jpeg"))

        self.ui.radioButton.clicked.connect(lambda: self.add_to_cart("족발 중", 36000))
        self.ui.radioButton_2.clicked.connect(lambda: self.add_to_cart("족발 대", 42000))
        self.ui.radioButton_3.clicked.connect(lambda: self.add_to_cart("진로", 5000))
        self.ui.radioButton_4.clicked.connect(lambda: self.add_to_cart("참이슬", 5000))

        self.ui.pushButton_3.clicked.connect(self.checkout)
        self.ui.pushButton.clicked.connect(self.checkout)

    def add_to_cart(self, item_name, price):
        """Add an item to the cart."""
        if item_name in self.soldout_items:
            QMessageBox.warning(self, "품절", f"{item_name}은(는) 품절되었습니다!")
            return

        if item_name in self.cart:
            self.cart[item_name]["quantity"] += 1
        else:
            self.cart[item_name] = {"price": price, "quantity": 1}

        self.update_cart_ui()
        self.ros_node.get_logger().info(f"Added to cart: {item_name} - {price}원")
        QMessageBox.information(self, "장바구니", f"{item_name}이(가) 추가되었습니다!")

    def update_cart_ui(self):
        """Update the cart UI."""
        self.ui.listWidget_cart.clear()
        for item_name, details in self.cart.items():
            quantity = details["quantity"]
            price = details["price"] * quantity
            self.ui.listWidget_cart.addItem(f"{item_name} x{quantity} - {price}원")

    def checkout(self):
        """Handle checkout and publish ROS messages."""
        if not self.cart:
            QMessageBox.warning(self, "결제 실패", "장바구니가 비어 있습니다!")
            return

        order_items = [f"{item},{details['quantity']}" for item, details in self.cart.items()]
        order_message = f"{self.table_number},{','.join(order_items)}"
        self.ros_node.publish_message(order_message)

        self.ros_node.get_logger().info(f"Checkout message: {order_message}")
        total_price = sum(details['price'] * details['quantity'] for details in self.cart.values())
        QMessageBox.information(self, "결제 완료", f"결제 완료!\n총 금액: {total_price}원\n{order_message}")

        self.cart.clear()
        self.update_cart_ui()

    def update_soldout_items(self, soldout_items):
        """Update the UI to reflect sold-out items."""
        self.soldout_items.update(soldout_items)

        if "족발 중" in self.soldout_items:
            self.ui.radioButton.setEnabled(False)
        if "족발 대" in self.soldout_items:
            self.ui.radioButton_2.setEnabled(False)
        if "진로" in self.soldout_items:
            self.ui.radioButton_3.setEnabled(False)
        if "참이슬" in self.soldout_items:
            self.ui.radioButton_4.setEnabled(False)

# Main function

def main():
    rclpy.init()
    app = QApplication(sys.argv)

    nodes = []
    windows = []

    screen = QApplication.primaryScreen()
    screen_geometry = screen.geometry()
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()

    rows, cols = 3, 3
    window_width = screen_width // cols
    window_height = screen_height // rows

    soldout_server = SoldoutServer()
    nodes.append(soldout_server)

    threading.Thread(target=rclpy.spin, args=(soldout_server,), daemon=True).start()

    for table_number in range(1, 10):
        table_server = TableServer(table_number)
        publisher_node = PublisherNode(table_number)

        nodes.append(table_server)
        nodes.append(publisher_node)

        window = TableApp(publisher_node, table_number)
        table_server.gui = window
        windows.append(window)

        x_position = ((table_number - 1) % cols) * window_width
        y_position = ((table_number - 1) // cols) * window_height

        window.setGeometry(x_position, y_position, window_width, window_height)
        window.show()

        threading.Thread(target=rclpy.spin, args=(table_server,), daemon=True).start()
        threading.Thread(target=rclpy.spin, args=(publisher_node,), daemon=True).start()

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("Program interrupted.")
    finally:
        for node in nodes:
            node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
