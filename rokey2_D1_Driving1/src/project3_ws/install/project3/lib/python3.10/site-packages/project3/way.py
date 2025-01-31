import sys
import rclpy
import threading
import signal
from rclpy.node import Node
from functools import partial
from geometry_msgs.msg import PoseStamped
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget


class WaypointNavigator(Node):
    def __init__(self):
        super().__init__('waypoint_navigator')
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Define waypoints
        self.waypoints = {
            1: self.create_pose(3.68965986130532, 1.498483202177901, 0.9962107742353471, 0.08697179598818436),  # Table 1
            2: self.create_pose(3.6206477878016208, 0.38018026738708965, 0.9976748795767512, 0.06815302386185901),  # Table 2
            3: self.create_pose(3.6279003456104704, -0.49848594152249687, -0.994453789409345, 0.10517443001696732),  # Table 3
            4: self.create_pose(2.58119983414975, 1.5035286334267473, -0.9995238635463126, 0.030855245930832376),  # Table 4
            5: self.create_pose(2.542072833175258, 0.44090932116091597, -0.99944958356542, 0.033174235649196915),  # Table 5
            6: self.create_pose(2.5866782472939067, -0.5453673465009153, -0.9969975832510041, 0.07743267392811198),  # Table 6
            7: self.create_pose(0.21373855062423944, 1.5778874581586089, 0.003315222117917795, 0.9999945046360549),  # Table 7
            8: self.create_pose(0.13548594906805056, 0.45124409939411064, 0.04494429443138941, 0.9989894946384895),  # Table 8
            9: self.create_pose(0.2636797387500241, -0.6292745969310705, 0.024301906915626573, 0.9997046650487654),  # Table 9
            "kitchen": self.create_pose(0.20480307321346577, 0.07663624845166352, -0.07352593307828481, 0.9972933054848847),  # Kitchen
        }

    def create_pose(self, x, y, z, w):
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.orientation.z = z
        pose.pose.orientation.w = w
        return pose

    def send_goal(self, pose):
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = pose
        self.get_logger().info(f"Navigating to ({pose.pose.position.x}, {pose.pose.position.y})...")

        self.action_client.wait_for_server()
        self._send_goal_future = self.action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected")
            return
        self.get_logger().info("Goal accepted")
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result()
        if result.status == 4:  # GoalStatus.STATUS_SUCCEEDED
            self.get_logger().info("Goal succeeded!")


class GUI(QMainWindow):
    def __init__(self, node):
        super().__init__()
        self.node = node
        self.image_paths = {
            1: "/home/yeonho/project3_ws/src/project3/project3/img/s1.png",
            2: "/home/yeonho/project3_ws/src/project3/project3/img/s2.png",
            3: "/home/yeonho/project3_ws/src/project3/project3/img/s3.png",
            4: "/home/yeonho/project3_ws/src/project3/project3/img/s4.png",
            5: "/home/yeonho/project3_ws/src/project3/project3/img/s5.png",
            6: "/home/yeonho/project3_ws/src/project3/project3/img/s6.png",
            7: "/home/yeonho/project3_ws/src/project3/project3/img/s7.png",
            8: "/home/yeonho/project3_ws/src/project3/project3/img/s8.png",
            9: "/home/yeonho/project3_ws/src/project3/project3/img/s9.png",
            "kitchen": "/home/yeonho/project3_ws/src/project3/project3/img/smile.png",
        }
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Serving Robot Controller")
        self.setGeometry(100, 100, 400, 600)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Buttons
        for i in range(1, 10):
            button = QPushButton(f"Go to Table {i}")
            button.clicked.connect(partial(self.go_to_table, i))
            layout.addWidget(button)

        kitchen_button = QPushButton("Serving Complete (Go to Kitchen)")
        kitchen_button.clicked.connect(partial(self.go_to_table, "kitchen"))
        layout.addWidget(kitchen_button)

        # Image display
        self.image_display = QLabel()
        self.image_display.setFixedSize(300, 300)
        self.image_display.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_display)

        self.setCentralWidget(central_widget)

    def go_to_table(self, table_number):
        if table_number in self.node.waypoints:
            self.update_image(table_number)
            self.node.send_goal(self.node.waypoints[table_number])

    def update_image(self, table_number):
        if table_number in self.image_paths:
            pixmap = QPixmap(self.image_paths[table_number])
            pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
            self.image_display.setPixmap(pixmap)


def main():
    rclpy.init()
    navigator = WaypointNavigator()

    app = QApplication(sys.argv)
    gui = GUI(navigator)

    ros_thread = threading.Thread(target=rclpy.spin, args=(navigator,))
    ros_thread.start()

    gui.show()
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        pass
    finally:
        navigator.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
