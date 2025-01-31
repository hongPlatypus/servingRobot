# import sys
# import rclpy
# import threading
# import signal
# from rclpy.node import Node
# from std_msgs.msg import String
# from PySide2.QtCore import *
# from PySide2.QtWidgets import *


# class NODE(Node):
#     def __init__(self):
#         super().__init__('subscriber')
#         self.emit_signal = None
#         self.subscription = self.create_subscription(
#             String, 'order', self.subscription_callback, 10
#         )

#     def subscription_callback(self, msg):
#         order = msg.data
#         self.get_logger().info(f"Received order: {order}")
#         if self.emit_signal is not None:
#             self.emit_signal(order)
#         else:
#             self.get_logger().info("Node-GUI not connected")

#     def set_emit_signal(self, emit_func):
#         self.emit_signal = emit_func


# class GUI(QMainWindow):
#     order_received = Signal(str)

#     def __init__(self, node):
#         super().__init__()
#         self.node = node
#         self.order_received.connect(self.update_order)

#         # Initialize order data
#         self.orders = {"짜장": 0, "짬뽕": 0, "탕수육": 0}
#         self.prices = {"짜장": 4000, "짬뽕": 5000, "탕수육": 10000}
#         self.setup_ui()
#         self.initialize_signal()

#     def setup_ui(self):
#         if not self.objectName():
#             self.setObjectName("MainWindow")
#         self.resize(400, 500)

#         # Central Widget
#         self.centralwidget = QWidget(self)
#         self.setCentralWidget(self.centralwidget)

#         # Layout
#         self.layout = QVBoxLayout(self.centralwidget)

#         # Order List
#         self.textBrowser = QTextBrowser(self.centralwidget)
#         self.textBrowser.setFixedHeight(250)
#         self.layout.addWidget(self.textBrowser)

#         # Summary Section
#         self.summaryBrowser = QTextBrowser(self.centralwidget)
#         self.layout.addWidget(self.summaryBrowser)

#     def update_order(self, order):
#         # Update order list
#         self.textBrowser.append(order)

#         # Update order count
#         if order in self.orders:
#             self.orders[order] += 1

#         # Update summary
#         self.update_summary()

#     def update_summary(self):
#         total_price = sum(self.orders[item] * self.prices[item] for item in self.orders)
#         for item, count in self.orders.items():
#             price = self.prices[item]
#             summary_text = f"{item}: {count}개 (총액: {count * price}원)\n"
#         summary_text += f"\n총 주문 금액: {total_price}원"

#         self.summaryBrowser.setText(summary_text)

#     def initialize_signal(self):
#         self.node.set_emit_signal(self.order_received.emit)


# def main():
#     rclpy.init()
#     node = NODE()
#     ros_thread = threading.Thread(target=lambda: rclpy.spin(node))
#     ros_thread.start()

#     app = QApplication(sys.argv)
#     gui = GUI(node)
#     gui.show()

#     signal.signal(signal.SIGINT, signal.SIG_DFL)

#     try:
#         sys.exit(app.exec_())

#     except KeyboardInterrupt:
#         sys.exit(0)

#     finally:
#         node.destroy_node()
#         rclpy.shutdown()


# if __name__ == "__main__":
#     main()

######################################################################################################################################################



        
import sys
import rclpy
import threading
import signal
from rclpy.node import Node
from std_msgs.msg import String

from PySide2.QtCore import Signal, Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication, QMainWindow, QTextBrowser, QWidget, QVBoxLayout, QLabel




class NODE(Node):
    def __init__(self):
        super().__init__('subscriber')
        self.emit_signal = None

        self.subscription = self.create_subscription(
            String, 'table_number', self.subscription_callback, 10
        )

    def subscription_callback(self, msg):
        message = msg.data
        self.get_logger().info(f'Received message: {message}')

        if self.emit_signal is not None:
            self.emit_signal(message)
        else:
            self.get_logger().info('Node-Gui not connected')

    def set_emit_signal(self, emit_func):
        self.emit_signal = emit_func


class GUI(QMainWindow):
    message_received = Signal(str)

    def __init__(self, node):
        super().__init__()
        self.node = node
        self.message_received.connect(self.add_message)
        self.setup_ui()
        self.initialize_signal()

        # Dictionary for image paths
        self.image_paths = {
            "1": "/home/yeonho/project3_ws/src/project3/project3/img/s1.png",
            "2": "/home/yeonho/project3_ws/src/project3/project3/img/s2.png",
            "3": "/home/yeonho/project3_ws/src/project3/project3/img/s3.png",
            "4": "/home/yeonho/project3_ws/src/project3/project3/img/s4.png",
            "5": "/home/yeonho/project3_ws/src/project3/project3/img/s5.png",
            "6": "/home/yeonho/project3_ws/src/project3/project3/img/s6.png",
            "7": "/home/yeonho/project3_ws/src/project3/project3/img/s7.png",
            "8": "/home/yeonho/project3_ws/src/project3/project3/img/s8.png",
            "9": "/home/yeonho/project3_ws/src/project3/project3/img/s9.png",
            "10": "/home/yeonho/project3_ws/src/project3/project3/img/smile.png",
        }


    def setup_ui(self):
        self.setObjectName("MainWindow")
        self.resize(800, 600)

    # Central widget and layout
        self.centralwidget = QWidget(self)
        self.main_layout = QVBoxLayout(self.centralwidget)

    # Upper part: Display messages (reduced height)
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setFixedHeight(100)  # Reduced height
        self.main_layout.addWidget(self.textBrowser)

    # Lower part: Image display (increased size)
        self.image_display = QLabel(self.centralwidget)
        self.image_display.setFixedHeight(500)  # Increased height
        self.image_display.setStyleSheet("background-color: lightgray;")
        self.image_display.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.image_display)

        self.setCentralWidget(self.centralwidget)


    def add_message(self, message):
        self.textBrowser.append(f"Message received: {message}")
        self.update_image(message)

    def update_image(self, message):
        # Update the image based on the message
        if message in self.image_paths:
            pixmap = QPixmap(self.image_paths[message])
            pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)
            self.image_display.setPixmap(pixmap)
        else:
            self.image_display.clear()

    def initialize_signal(self):
        self.node.set_emit_signal(self.message_received.emit)


def main():
    rclpy.init()
    node = NODE()
    ros_thread = threading.Thread(target=lambda: rclpy.spin(node))
    ros_thread.start()

    app = QApplication(sys.argv)
    gui = GUI(node)
    gui.show()

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
