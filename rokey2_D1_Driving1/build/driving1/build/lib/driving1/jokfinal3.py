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

import asyncio

from PySide2.QtCore import QObject, Signal

import mysql.connector


class CentralServer(Node, QObject):
    # 신호 정의: GUI에 실시간 업데이트 알림
    soldout_signal = Signal(list)
    
    def __init__(self):
        Node.__init__(self, 'central_server')
        QObject.__init__(self)  # QObject 초기화

        self.soldout_items = set()  # 품절 항목 저장

        # NotifySoldout 서비스 생성
        self.soldout_service = self.create_service(
            NotifySoldout,
            '/soldout',
            self.handle_soldout
        )
        
        # 품절 상태를 GUI로 브로드캐스트하기 위한 토픽 생성
        self.publisher = self.create_publisher(String, '/soldout_updates', 10)

    def handle_soldout(self, request, response):
        """품절 요청 처리"""
        try:
            # 요청에서 품절 항목 가져오기 (공백 및 불필요한 항목 제거)
            items = [item.strip() for item in request.message.split(",") if item.strip()]
            self.soldout_items.update(items)
            self.get_logger().info(f"Updated sold-out items: {self.soldout_items}")

            # 품절 상태를 브로드캐스트
            self.broadcast_soldout_items()

            # 품절 상태 신호를 통해 GUI에 알림
            self.soldout_signal.emit(list(self.soldout_items))

            # 성공 응답 생성
            response.success = True
            response.response_message = "Sold-out items updated successfully."
        except Exception as e:
            self.get_logger().error(f"Error handling sold-out request: {e}")
            response.success = False
            response.response_message = "Failed to update sold-out items."
        return response


    def broadcast_soldout_items(self):
        """품절 상태를 모든 GUI에 브로드캐스트"""
        soldout_message = ", ".join(self.soldout_items)
        msg = String()
        msg.data = soldout_message
        self.publisher.publish(msg)
        self.get_logger().info(f"Broadcasted sold-out items: {soldout_message}")


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
        
    


from PySide2.QtCore import Signal


class TableApp(QMainWindow):
    # 신호 정의
    def __init__(self, central_server, publisher_node, table_number):
        super().__init__()
        self.central_server = central_server  # CentralServer 인스턴스
        self.publisher_node = publisher_node  # PublisherNode 인스턴스
        self.table_number = table_number
        self.soldout_items = set()

        
        # 중앙 서버의 신호 연결
        self.central_server.soldout_signal.connect(self.update_soldout_items)

        # `/soldout_updates` 토픽 구독
        self.subscription = self.central_server.create_subscription(
            String,
            '/soldout_updates',
            self.handle_soldout_broadcast,
            10
        )
        
        self.cart = {}
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(f"Table {table_number}")

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
        self.central_server.get_logger().info(f"Added to cart: {item_name} - {price}원")
        QMessageBox.information(self, "장바구니", f"{item_name}이(가) 추가되었습니다!")



    def update_cart_ui(self):
        """장바구니 UI 업데이트"""
        self.ui.listWidget_cart.clear()
        for item_name, details in self.cart.items():
            quantity = details["quantity"]
            price = details["price"] * quantity
            self.ui.listWidget_cart.addItem(f"{item_name} x{quantity} - {price}원")



#####품절 관련 상태 업데이트
    def update_soldout_items(self, items):
        """GUI에서 신호로 받은 품절 상태를 업데이트"""
        self.soldout_items.update(items)
        self.update_ui_soldout_state()
        
    def handle_soldout_broadcast(self, msg):
        """브로드캐스트 메시지를 통해 품절 상태 업데이트"""
        items = msg.data.split(", ")
        self.soldout_items.update(items)
        self.update_ui_soldout_state()

    def update_ui_soldout_state(self):
        """UI에서 품절 상태 반영"""
        button_mapping = {
            "족발 중": self.ui.radioButton,
            "족발 대": self.ui.radioButton_2,
            "진로": self.ui.radioButton_3,
            "참이슬": self.ui.radioButton_4,
        }

        for item, button in button_mapping.items():
            if item in self.soldout_items:
                button.setEnabled(False)
                
                
                
#####결제 관련  topic 발행
    def checkout(self):
        """결제 및 ROS 메시지 발행"""
        if not self.cart:
            QMessageBox.warning(self, "결제 실패", "장바구니가 비어 있습니다!")
            return

        # 초과된 재고를 제거하는 플래그
        exceeded_items = []

        # MySQL 재고 확인
        for item_name, details in list(self.cart.items()):  # 리스트 복사로 안전한 반복문
            quantity = details["quantity"]
            current_stock = self.central_server.get_current_stock(item_name)  # 재고 확인 메서드 호출
            if quantity > current_stock:
                QMessageBox.warning(
                    self,
                    "재고 초과",
                    f"{item_name}의 현재 재고는 {current_stock}개입니다.\n재고를 초과하여 주문할 수 없습니다."
                )
                # 초과된 재고는 재고 수량으로 조정
                if current_stock > 0:
                    self.cart[item_name]["quantity"] = current_stock
                else:
                    exceeded_items.append(item_name)

        # 초과된 항목 제거
        for item in exceeded_items:
            del self.cart[item]

        self.update_cart_ui()  # UI 업데이트

        if not self.cart:
            QMessageBox.information(self, "결제 취소", "모든 품목이 재고를 초과하여 결제가 취소되었습니다.")
            return

        order_items = [f"{item},{details['quantity']}" for item, details in self.cart.items()]
        order_message = f"{self.table_number},{','.join(order_items)}"
        self.publisher_node.publish_message(order_message)  # PublisherNode 사용

        self.publisher_node.get_logger().info(f"Checkout message: {order_message}")
        total_price = sum(details['price'] * details['quantity'] for details in self.cart.values())
        QMessageBox.information(self, "결제 완료", f"결제 완료!\n총 금액: {total_price}원\n{order_message}")

        self.cart.clear()
        self.update_cart_ui()


        

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
    # ROS2 초기화
    rclpy.init()
    app = QApplication(sys.argv)

    executor = rclpy.executors.MultiThreadedExecutor()
    nodes = []
    windows = []

    # **CentralServer 초기화 및 추가**
    central_server = CentralServer()
    nodes.append(central_server)
    executor.add_node(central_server)
    
    screen = QApplication.primaryScreen()
    screen_geometry = screen.geometry()
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()

    rows, cols = 3, 3
    window_width = screen_width // cols
    window_height = screen_height // rows

    for table_number in range(1, 10):
        publisher_node = PublisherNode(table_number)
        nodes.append(publisher_node)
        executor.add_node(publisher_node)
        
        # 각 테이블의 GUI 생성
        gui = TableApp(central_server, publisher_node, table_number)  # CentralServer 및 PublisherNode 연결
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