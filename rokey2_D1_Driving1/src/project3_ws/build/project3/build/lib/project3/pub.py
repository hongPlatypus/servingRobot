# import sys
# import threading
# import queue
# import rclpy
# import signal
# from rclpy.node import Node
# from rclpy.qos import QoSProfile

# from PySide2.QtCore import *
# from PySide2.QtGui import *
# from PySide2.QtWidgets import *

# from std_msgs.msg import String


# class NODE(Node):
#     def __init__(self):
#         super().__init__('publisher')
#         qos_profile = QoSProfile(depth=5)
#         self.message_publisher = self.create_publisher(
#             String, 'order', qos_profile
#         )
#         self.queue = queue.Queue()
#         self.timer = self.create_timer(0.1, self.publish_message)

#     def publish_message(self):
#         while not self.queue.empty():
#             message = self.queue.get()
#             msg = String()
#             msg.data = message
#             self.message_publisher.publish(msg)
#             self.get_logger().info(f'Published message: {message}')


# class GUI(QMainWindow):
#     def __init__(self, node):
#         super().__init__()
#         self.node = node
#         self.setup_ui()

#     def setup_ui(self):
#         if not self.objectName():
#             self.setObjectName("MainWindow")
#         self.resize(400, 300)

#         # Central Widget
#         self.centralwidget = QWidget(self)
#         self.setCentralWidget(self.centralwidget)

#         # Layout
#         self.layout = QVBoxLayout(self.centralwidget)

#         # Menu items
#         self.add_menu_item("짜장", "/home/yeonho/project3_ws/src/project3/project3/짜장.png")
#         self.add_menu_item("짬뽕", "/home/yeonho/project3_ws/src/project3/project3/짬뽕.png")
#         self.add_menu_item("탕수육", "/home/yeonho/project3_ws/src/project3/project3/탕수육.png")

#     def add_menu_item(self, menu_name, image_path):
#         # Horizontal layout for menu item
#         item_layout = QHBoxLayout()

#         # Image
#         image_label = QLabel()
#         pixmap = QPixmap(image_path)
#         pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio)
#         image_label.setPixmap(pixmap)

#         # Button
#         button = QPushButton(menu_name)
#         button.clicked.connect(lambda: self.button_clicked(menu_name))

#         # Add image and button to layout
#         item_layout.addWidget(image_label)
#         item_layout.addWidget(button)

#         # Add item layout to main layout
#         self.layout.addLayout(item_layout)

#     def button_clicked(self, menu_name):
#         self.node.queue.put(menu_name)


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
#         pass

#     finally:
#         node.destroy_node()
#         rclpy.shutdown()


# if __name__ == "__main__":
#     main()


######################################################################################################################################################

import sys
import threading
import queue
import rclpy
import signal
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from PySide2.QtWidgets import QApplication, QMainWindow


class NODE(Node):
    def __init__(self):
        super().__init__('publisher')
        qos_profile = QoSProfile(depth=5)
        self.message_publisher = self.create_publisher(String, 'table_number', qos_profile)
        self.current_number = 1
        self.is_ten_next = False
        self.timer = self.create_timer(2.0, self.publish_message)

    def publish_message(self):
        msg = String()
        if self.is_ten_next:
            msg.data = "10"  # Send "10" after every number
            self.is_ten_next = False
            self.timer.cancel()
            self.timer = self.create_timer(3.0, self.publish_message)  # 3-second delay after "10"
        else:
            msg.data = str(self.current_number)  # Send the current number
            self.current_number = self.current_number % 9 + 1  # Cycle through 1-9
            self.is_ten_next = True
            self.timer.cancel()
            self.timer = self.create_timer(2.0, self.publish_message)  # 2-second delay before numbers
        self.message_publisher.publish(msg)
        self.get_logger().info(f'Published message: {msg.data}')



def main():
    rclpy.init()
    node = NODE()
    ros_thread = threading.Thread(target=lambda: rclpy.spin(node))
    ros_thread.start()

    app = QApplication(sys.argv)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
