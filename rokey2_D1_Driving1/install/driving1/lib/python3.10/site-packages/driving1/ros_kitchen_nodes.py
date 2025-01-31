import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from driving1_interfaces.srv import NotifySoldout
from project3_interfaces.msg import TableCommand
from std_msgs.msg import String
from db_handler import DBHandler
from PySide2.QtCore import Qt, Signal, QObject, QMetaObject, Slot
from PySide2.QtWidgets import QMessageBox


class KitchenClient(Node, QObject):
    def __init__(self, db_handler,publisher_node):
        Node.__init__(self, 'kitchen_client')
        QObject.__init__(self)  # QObject 초기화

        # DBHandler 초기화
        self.db_handler = db_handler
        self.publisher_node = publisher_node  # PublisherNode를 KitchenClient에 전달받음
        self.soldout_items = set()  # 품절된 항목을 저장할 속성
        self.notified_items = set()  # 이미 알림이 표시된 품목
        self.order_callback = None  # ✅ 주문 처리 콜백 추가

        # NotifySoldout 서비스 클라이언트 생성
        self.client = self.create_client(NotifySoldout, '/soldout')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service /soldout not available, waiting...')


        #테이블별 메시지 구독
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            depth=10
        )

        self.get_logger().info("KitchenClient:initialized(sold-out)")

        # 각 테이블 메시지 토픽 동적으로 구독
        self.table_subscriptions = []
        for table_number in range(1, 10):  # 테이블 1번부터 9번까지
            topic_name = f'/table{table_number}/message'
            subscription = self.create_subscription(
                String,
                topic_name,
                self.listener_callback,
                qos_profile
            )
            self.table_subscriptions.append(subscription)
        
        self.publisher = self.create_publisher(TableCommand, 'to_robot', qos_profile)

        self.get_logger().info("KitchenPublisher:initialized(insert-order)")

    def publish_to_robot(self, table_id, command):
        """
        로봇에게 명령을 보내는 메서드 (ROS2 Publisher 사용).
        `TableCommand.msg`가 `string to_robot` 형식이므로, 데이터를 문자열로 변환하여 전송해야 함.
        """
        try:
            command_msg = TableCommand()

            # ✅ 올바른 데이터 변환: "table_id,command" 형식의 문자열로 변환
            command_msg.to_robot = str(table_id)

            # 메시지 발행
            self.publisher.publish(command_msg)
            self.get_logger().info(f"Published to_robot: {command_msg.to_robot}")
        except Exception as e:
            self.get_logger().error(f"Failed to publish to_robot: {e}")

    def set_order_callback(self, callback):
        """GUI에서 새로운 주문을 처리하기 위한 콜백 설정"""
        self.order_callback = callback

    def listener_callback(self, msg):
        """테이블에서 수신된 주문 메시지를 처리."""
        self.get_logger().info(f"Received message from table: {msg.data}")
        try:
            parsed_message = msg.data.split(',')
            table_id = int(parsed_message[0])
            items = {parsed_message[i]: int(parsed_message[i + 1]) for i in range(1, len(parsed_message), 2)}

            if self.order_callback is not None:
                self.order_callback(table_id, items)  # ✅ 수정됨
            # ✅ 여기 추가!
            self.process_received_message(msg.data)  # 주문을 DB에 반영하도록 실행

        except Exception as e:
            self.get_logger().error(f"Error processing message: {e}")


    def process_received_message(self, message):
        """Process the received message and update GUI."""
        try:
            self.get_logger().info(f"Raw message received: {message}")
            parsed_message = message.split(',')
            self.get_logger().info(f"Parsed message: {parsed_message}")

            if len(parsed_message) < 3 or len(parsed_message) % 2 == 0:
                self.get_logger().error(f"Invalid message format: {parsed_message}")
                raise ValueError(f"Invalid message format: {message}")

            try:
                table_id = int(parsed_message[0])  # First element is the table number
            except ValueError:
                self.get_logger().error(f"Invalid table ID: {parsed_message[0]}")
                raise ValueError(f"Invalid table ID: {parsed_message[0]}")

            order_details = parsed_message[1:]  # Remaining elements are item details

            # Convert to dictionary
            items = {}
            for i in range(0, len(order_details), 2):
                try:
                    item = order_details[i]
                    quantity = int(order_details[i + 1])
                    items[item] = quantity
                except ValueError as e:
                    self.get_logger().error(f"Invalid quantity for item '{order_details[i]}': {e}")
                    raise ValueError(f"Invalid quantity: {order_details[i + 1]}")

            self.get_logger().info(f"Inserting order for table_id={table_id}, items={items}")
            self.db_handler.insert_order(table_id, items)
        except Exception as e:
            self.get_logger().error(f"Error processing order message: {e}")
            
    def process_manual_soldout(self):
        """
        수동으로 품절 상태를 확인하고, 품절된 항목과 현재 재고를 반환.
        :return: (set of soldout_items, dict of current_stock)
        """
        try:
            # 전체 재고 가져오기
            all_stock = self.db_handler.get_current_stock()
            self.get_logger().info(f"Current stock: {all_stock}")

            # 품절 항목 계산
            soldout_items = {item for item, stock in all_stock.items() if stock <= 0}
            self.get_logger().info(f"Sold-out items: {soldout_items}")

            # 새로운 품절 항목 확인
            new_soldout_items = soldout_items - self.soldout_items
            if new_soldout_items:
                self.soldout_items.update(new_soldout_items)
                self.get_logger().info(f"New sold-out items: {new_soldout_items}")

            return soldout_items, all_stock
        except Exception as e:
            self.get_logger().error(f"Error in manual sold-out processing: {e}")
            return set(), {}

        
    def notify_sold_out_items(self):
        """현재 품절 품목을 /soldout 서비스로 전송"""
        soldout_items, _ = self.process_manual_soldout()
        if not soldout_items:
            QMessageBox.information(None, "No Sold-Out Items", "현재 품절된 품목이 없습니다.")
            return

        soldout_message = ", ".join(soldout_items)
        self.notify_soldout(soldout_message)
        
    @Slot()
    def _show_soldout_popup(self):
        print("[DEBUG] _show_soldout_popup called!")  # 호출 여부 확인
        """
        Actual logic for showing the popup in the GUI thread.
        """
        try:
            soldout_items, current_stock = self.process_manual_soldout()

            if not soldout_items:
                stock_message = "\n".join([f"{item}: {stock}" for item, stock in current_stock.items()])
                QMessageBox.information(
                    None,  # Parent window is set to None to avoid threading issues
                    "No Sold-Out Items",
                    f"현재 재고:\n\n{stock_message}\n\n품절된 제품이 없습니다."
                )
            else:
                soldout_message = "\n".join([f"{item}: 0 (품절)" for item in soldout_items])
                remaining_stock_message = "\n".join(
                    [f"{item}: {stock}" for item, stock in current_stock.items() if item not in soldout_items]
                )
                QMessageBox.information(
                    None,  # Parent window is set to None
                    "Sold-Out Notification",
                    f"{', '.join(soldout_items)}이(가) 품절되었습니다.\n\n"
                    f"품절된 항목:\n{soldout_message}\n\n"
                    f"현재 재고:\n{remaining_stock_message}"
                )

            # 품절된 항목을 알리는 ROS2 서비스 호출
            message = ", ".join(soldout_items)
            self.notify_soldout(message)

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to notify sold-out items: {e}")

    def notify_soldout(self, message):
        """NotifySoldout 서비스 요청."""
        try:
            request = NotifySoldout.Request()
            request.message = message
            self.get_logger().info(f"Sending sold-out notification: {message}")
            future = self.client.call_async(request)
            future.add_done_callback(self.handle_notify_response)
        except Exception as e:
            self.get_logger().error(f"Error in notify_soldout: {e}")

    def handle_notify_response(self, future):
        """NotifySoldout 서비스 응답 처리"""
        try:
            response = future.result()
            self.get_logger().info(f"NotifySoldout response: {response.response_message}")
        except Exception as e:
            self.get_logger().error(f"Failed to receive NotifySoldout response: {e}")




class StockClient:
    def __init__(self, node):
        self.node = node
        self.client = node.create_client(NotifySoldout, '/soldout')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.node.get_logger().info('Waiting for /soldout service...')

    def notify_soldout(self, message):
        """ROS2 service to notify sold-out items."""
        request = NotifySoldout.Request()
        request.message = message
        future = self.client.call_async(request)

        def callback(fut):
            try:
                response = fut.result()
                self.node.get_logger().info(f"NotifySoldout response: {response.response_message}")
            except Exception as e:
                self.node.get_logger().error(f"Service call failed: {e}")

        future.add_done_callback(callback)
