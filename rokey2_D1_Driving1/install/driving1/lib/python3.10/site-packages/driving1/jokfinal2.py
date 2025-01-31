import rclpy

from rclpy.node import Node

from rclpy.executors import MultiThreadedExecutor

from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidget, QPushButton, QLabel

from PySide2.QtGui import QPixmap

from std_msgs.msg import String

from driving1_interfaces.srv import NotifySoldout

from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

from ui_order import Ui_MainWindow

import threading

import sys
from PySide2.QtCore import Signal, Slot
import asyncio
import mysql.connector

class TableServer(Node):
    def __init__(self, table_number):
        super().__init__(f'table_server_{table_number}')
        self.table_number = table_number
        # 서비스 서버 설정
        self.soldout_service = self.create_service(NotifySoldout, '/soldout', self.handle_soldout)

    def handle_soldout(self, request, response):
        """ /soldout 요청 처리 """
        try:
            self.get_logger().info(f"Handling /soldout service request: {request.message}")

            soldout_items = request.message.split(", ")

            # GUI 업데이트를 신호를 통해 전달
            if hasattr(self, 'gui') and self.gui:

                self.gui.signal_update_soldout_items.emit(soldout_items)

            response.success = True

            response.response_message = "Handled sold-out items."

        except Exception as e:

            self.get_logger().error(f"Error in handling /soldout: {e}")

            response.success = False

            response.response_message = "Failed to handle sold-out notification."

        return response

    def handle_soldout_approve(self, request, response):

        """ /soldout_approve 요청 처리 """

        self.get_logger().info(f"Sold-out approval received: {request.message}")

        response.success = True

        response.response_message = "Sold-out approval acknowledged"

        return response

    async def process_soldout_items(self):

        """ 비동기로 품절 항목을 처리 """

        self.get_logger().info("Processing sold-out items...")

        await asyncio.sleep(1)  # 비동기 작업 예제

        self.get_logger().info("Sold-out items processed.")

class PublisherNode(Node):

    def __init__(self, table_number):

        super().__init__(f'publisher_table_{table_number}')

        qos_profile = QoSProfile(

            reliability=ReliabilityPolicy.RELIABLE,

            durability=DurabilityPolicy.VOLATILE,

            depth=10

        )

        self.publisher_ = self.create_publisher(String, f'/table{table_number}/message', qos_profile)

    def get_current_stock(self, item_name):

        """현재 재고량 확인 (MySQL 서버에서 데이터 가져오기)"""

        try:
            conn = mysql.connector.connect(
                host="192.168.123.61",
                user="jokbal",
                password="JOKbal12345!!",
                database="jokDB"
            )
            if conn.is_connected():
                self.get_logger().info("MySQL 서버에 성공적으로 연결되었습니다.")
            cursor = conn.cursor()
            cursor.execute("SELECT jokbal_mid_stock, jokbal_lar_stock, jinro_stock, cham_stock FROM STOCK ORDER BY stock_date DESC LIMIT 1;")
            result = cursor.fetchone()

            if item_name == "족발 중":
                return result[0]
            elif item_name == "족발 대":
                return result[1]
            elif item_name == "진로":
                return result[2]
            elif item_name == "참이슬":
                return result[3]
            else:
                return 0
        except mysql.connector.Error as e:
            self.get_logger().error(f"MySQL 연결 실패: {e}")
            return 0
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
                self.get_logger().info("MySQL 연결이 종료되었습니다.")

    def publish_message(self, message):

        """ ROS 메시지 발행 """

        msg = String()

        msg.data = message

        self.publisher_.publish(msg)

        self.get_logger().info(f"Published: {message}")

class TableApp(QMainWindow):

    signal_update_soldout_items = Signal(list)

    def __init__(self, ros_node, table_number):

        super().__init__()

        self.ros_node = ros_node

        self.table_number = table_number

        self.cart = {}

        self.soldout_items = set()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.setWindowTitle(f"Table {table_number}")

        self.signal_update_soldout_items.connect(self.update_soldout_items)

        self.setup_ui()

    def setup_ui(self):

        """ UI 초기화 및 연결 """

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

        exceeded_items = []

        for item_name, details in list(self.cart.items()):

            quantity = details["quantity"]

            current_stock = self.ros_node.get_current_stock(item_name)

            if quantity > current_stock:

                QMessageBox.warning(

                    self,

                    "재고 초과",

                    f"{item_name}의 현재 재고는 {current_stock}개입니다.\n재고를 초과하여 주문할 수 없습니다."

                )

                if current_stock > 0:

                    self.cart[item_name]["quantity"] = current_stock

                else:

                    exceeded_items.append(item_name)

        for item in exceeded_items:

            del self.cart[item]

        self.update_cart_ui()

        if not self.cart:

            QMessageBox.information(self, "결제 취소", "모든 품목이 재고를 초과하여 결제가 취소되었습니다.")

            return

        order_items = [f"{item},{details['quantity']}" for item, details in self.cart.items()]

        order_message = f"{self.table_number},{','.join(order_items)}"

        self.ros_node.publish_message(order_message)

        self.ros_node.get_logger().info(f"Checkout message: {order_message}")

        total_price = sum(details['price'] * details['quantity'] for details in self.cart.values())

        QMessageBox.information(self, "결제 완료", f"결제 완료!\n총 금액: {total_price}원\n{order_message}")

        self.cart.clear()

        self.update_cart_ui()

    @Slot(list)

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

class InsufficientStockSubscriber(Node):

    def __init__(self, gui):

        super().__init__('insufficient_stock_subscriber')

        self.subscription = self.create_subscription(

            String,

            '/insufficient_stock',

            self.handle_insufficient_stock,

            10

        )

        self.gui = gui

    def handle_insufficient_stock(self, msg):

        """재고 부족 메시지를 GUI로 전달"""

        QMessageBox.warning(self.gui, "재고 부족", msg.data)

def main():
    rclpy.init()
    app = QApplication(sys.argv)

    executor = rclpy.executors.MultiThreadedExecutor()
    nodes = []
    windows = []

    # Screen 정보 초기화
    screen = QApplication.primaryScreen()
    screen_geometry = screen.geometry()  # 여기에서 초기화

    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()

    rows, cols = 3, 3
    window_width = screen_width // cols
    window_height = screen_height // rows

    for table_number in range(1, 10):
        table_server = TableServer(table_number)
        publisher_node = PublisherNode(table_number)

        nodes.extend([table_server, publisher_node])
        executor.add_node(table_server)
        executor.add_node(publisher_node)

        gui = TableApp(publisher_node, table_number)
        windows.append(gui)

        x_position = ((table_number - 1) % cols) * window_width
        y_position = ((table_number - 1) // cols) * window_height
        gui.setGeometry(x_position, y_position, window_width, window_height)
        gui.show()

    executor_thread = threading.Thread(target=executor.spin, daemon=True)
    executor_thread.start()

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("Program interrupted.")
    finally:
        for node in nodes:
            node.destroy_node()
        executor.shutdown()
        rclpy.shutdown()






if __name__ == "__main__":

    main()