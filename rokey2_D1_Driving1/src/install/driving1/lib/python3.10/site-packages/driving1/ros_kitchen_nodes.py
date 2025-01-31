import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from driving1_interfaces.srv import NotifySoldout
from project3_interfaces.msg import TableCommand
from std_msgs.msg import String
from db_handler import DBHandler, InventoryManager
from PySide2.QtCore import QMetaObject, Qt, Signal, QObject


class KitchenClient(Node, QObject):
    soldout_signal = Signal(str)  # 신호 정의
    
    def __init__(self, db_config):
        Node.__init__(self, 'kitchen_client')
        QObject.__init__(self)  # QObject 초기화

        # DBHandler 초기화
        self.db_handler = DBHandler(**db_config)

        # StockClient 생성
        self.stock_client = StockClient(self)

        # InventoryManager 초기화
        self.inventory_manager = InventoryManager(self.db_handler, self.stock_client)
        
        # GUI 콜백 초기화
        self.gui_callback = None

        # NotifySoldout 서비스 클라이언트 생성
        self.client = self.create_client(NotifySoldout, '/soldout')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service /soldout not available, waiting...')

        # 이미 알림이 표시된 품절 항목을 저장할 집합
        self.notified_items = set()

        # Sold-out 알림 신호 연결
        self.soldout_signal.connect(self.handle_soldout_signal)

        # 타이머 설정 (10초마다 재고 확인)
        self.timer_period = 30.0
        self.timer = self.create_timer(self.timer_period, self.check_and_notify_soldout)

        # QoS 설정
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            depth=10
        )

        self.get_logger().info("KitchenPublisher initialized, publishing to 'to_robot'")

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

        self.publisher = self.create_publisher(
            TableCommand, 'to_robot', qos_profile
        )

        self.get_logger().info("KitchenClient is ready to send sold-out notifications.")

    def publish_to_robot(self, table_id, command):
        """
        로봇에게 명령을 보내는 메서드 (ROS2 Publisher 사용).
        :param table_id: 테이블 ID (int)
        :param command: 로봇에게 보낼 명령 (str)
        """
        try:
            # TableCommand 메시지 생성
            command_msg = TableCommand()
            command_msg.table_id = table_id
            command_msg.command = command

            # 메시지 발행
            self.publisher.publish(command_msg)
            self.get_logger().info(f"Published to_robot: table_id={table_id}, command={command}")
        except Exception as e:
            self.get_logger().error(f"Failed to publish to_robot: {e}")
            
    def set_order_callback(self, callback):
        """GUI에서 새로운 주문을 처리하기 위한 콜백 설정"""
        self.order_callback = callback

    def listener_callback(self, msg):
        """Handles messages received from table nodes."""
        self.get_logger().info(f"Received message from table: {msg.data}")
        self.process_received_message(msg.data)
        try:
            parsed_message = msg.data.split(',')
            table_id = int(parsed_message[0])
            items = {parsed_message[i]: int(parsed_message[i + 1]) for i in range(1, len(parsed_message), 2)}

            if self.order_callback:
                self.order_callback(table_id, items)
        except Exception as e:
            self.get_logger().error(f"Error processing message: {e}")

    def process_received_message(self, message):
        """Process the received message and update GUI."""
        try:
            parsed_message = message.split(',')
            if len(parsed_message) < 3 or len(parsed_message) % 2 == 0:
                raise ValueError(f"Invalid message format: {message}")

            table_id = int(parsed_message[0])  # First element is the table number
            order_details = parsed_message[1:]  # Remaining elements are item details

            # Convert to dictionary
            items = {order_details[i]: int(order_details[i + 1]) for i in range(0, len(order_details), 2)}

            # 데이터베이스에 주문 삽입
            self.db_handler.insert_order(table_id, items)

            # 재고 업데이트 및 품절 알림 처리
            if not self.inventory_manager.process_order(items):
                self.get_logger().warning(f"Some items are sold out for table {table_id}.")
        except Exception as e:
            self.get_logger().error(f"Error processing order message: {e}")

    def set_gui_callback(self, callback):
        """GUI 콜백 설정."""
        self.gui_callback = callback
        
    def handle_soldout_signal(self, message):
        """GUI에서 처리할 수 있도록 Sold-out 메시지를 전달"""
        if self.gui_callback:
            self.gui_callback(message)
            
    def check_and_notify_soldout(self):
        """Sold-out 아이템 확인 및 알림"""
        try:
            soldout_items = set(self.db_handler.get_soldout_items())  # `set`으로 변환
            new_soldout_items = soldout_items - self.notified_items  # 차집합 연산
            if new_soldout_items:
                message = ", ".join(new_soldout_items)
                self.notify_soldout(message)
                self.soldout_signal.emit(message)  # 신호를 통해 GUI로 전달
                
                # 새로운 품절 항목을 notified_items에 추가
                self.notified_items.update(new_soldout_items)
        except Exception as e:
            self.get_logger().error(f"Error during sold-out check: {e}")




    def notify_soldout(self, message):
        """Notify sold-out items using the NotifySoldout service."""
        try:
            request = NotifySoldout.Request()
            request.message = message
            self.get_logger().info(f"Sending sold-out notification: {message}")
            future = self.client.call_async(request)
            future.add_done_callback(self.handle_notify_response)
        except Exception as e:
            self.get_logger().error(f"Error in notify_soldout: {e}")

    def handle_notify_response(self, future):
        """Handle response from NotifySoldout service."""
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
