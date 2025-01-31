from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidget, QPushButton, QLabel
from PySide2.QtGui import QPixmap
import sys
import threading
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from std_msgs.msg import String
from example_interfaces.srv import Trigger  # ROS2 Trigger 서비스 타입
from ui_order import Ui_MainWindow

class TableServer(Node):
    def __init__(self, table_number):
        super().__init__(f'table_server_{table_number}')
        self.table_number = table_number

        # 서비스 서버 설정
        self.soldout_service = self.create_service(Trigger, '/soldout', self.handle_soldout)
        self.soldout_approve_service = self.create_service(Trigger, '/soldout_approve', self.handle_soldout_approve)

    def handle_soldout(self, request, response):
        """/soldout 요청 처리"""
        soldout_items = request.message.split(", ")
        response.success = True
        response.message = f"Received sold-out items: {', '.join(soldout_items)}"
        self.get_logger().info(f"Received sold-out items: {', '.join(soldout_items)}")

        # GUI에 품절 항목 전달
        self.gui.update_soldout_items(soldout_items)
        return response

    def handle_soldout_approve(self, request, response):
        """/soldout_approve 요청 처리"""
        self.get_logger().info("Sold-out approval acknowledged")
        response.success = True
        response.message = "Sold-out approval received"
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
        """ROS 메시지 발행"""
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
        """UI 초기화 및 연결"""
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
        """장바구니에 아이템 추가"""
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
        """장바구니 UI 업데이트"""
        self.ui.listWidget_cart.clear()
        for item_name, details in self.cart.items():
            quantity = details["quantity"]
            price = details["price"] * quantity
            self.ui.listWidget_cart.addItem(f"{item_name} x{quantity} - {price}원")

    def checkout(self):
        """결제 및 ROS 메시지 발행"""
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
        """GUI에 품절 상태 반영"""
        self.soldout_items.update(soldout_items)
        if "족발 중" in self.soldout_items:
            self.ui.radioButton.setEnabled(False)
        if "족발 대" in self.soldout_items:
            self.ui.radioButton_2.setEnabled(False)
        if "진로" in self.soldout_items:
            self.ui.radioButton_3.setEnabled(False)
        if "참이슬" in self.soldout_items:
            self.ui.radioButton_4.setEnabled(False)


def main():
    rclpy.init()
    app = QApplication(sys.argv)

    nodes = []
    windows = []

    # 전체 화면 크기 가져오기
    screen = QApplication.primaryScreen()
    screen_geometry = screen.geometry()
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()

    # 3x3 레이아웃으로 창 크기 계산
    rows, cols = 3, 3
    window_width = screen_width // cols
    window_height = screen_height // rows

    # 각 창의 위치 계산
    for table_number in range(1, 10):
        ros_node = TableServer(table_number)
        nodes.append(ros_node)

        # GUI 생성 및 연결
        window = TableApp(ros_node, table_number)
        ros_node.gui = window
        windows.append(window)

        # 창 위치 설정
        x_position = ((table_number - 1) % cols) * window_width
        y_position = ((table_number - 1) // cols) * window_height

        window.setGeometry(x_position, y_position, window_width, window_height)
        window.show()

        threading.Thread(target=rclpy.spin, args=(ros_node,), daemon=True).start()

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
