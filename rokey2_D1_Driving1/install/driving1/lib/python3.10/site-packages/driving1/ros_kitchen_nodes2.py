import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from driving1_interfaces.srv import NotifySoldout
from std_msgs.msg import String
from PySide2.QtCore import Signal, QObject
from db_handler import DBHandler, InventoryManager
from collections import deque
import asyncio


class ServiceClientManager(Node):
    def __init__(self, node_name="service_client_manager"):
        super().__init__(node_name)
        self.notify_clients = {}
        self.soldout_queues = {i: deque() for i in range(1, 10)}
        self.is_processing = {i: False for i in range(1, 10)}

        # 테이블별 서비스 클라이언트 생성
        for table_id in range(1, 10):
            service_name = f"/table_server_{table_id}/soldout"  # 서비스 이름 확인
            client = self.create_client(NotifySoldout, service_name)
            if client:
                self.notify_clients[table_id] = client
            else:
                self.get_logger().error(f"Failed to create service client for {service_name}")
    
    async def call_soldout_service(self, table_id, message):
        """비동기로 테이블 서비스 호출."""
        client = self.notify_clients.get(table_id)
        if not client:
            self.get_logger().error(f"Service client for Table {table_id} not initialized.")
            return

        try:
            # 서비스 연결 대기
            if not await client.wait_for_service(timeout_sec=2.0):
                self.get_logger().warning(f"Service for Table {table_id} not available.")
                return

            # 요청 생성 및 비동기 호출
            request = NotifySoldout.Request()
            request.message = message
            self.get_logger().info(f"Sending sold-out notification to Table {table_id}: {message}")
            future = client.call_async(request)
            response = await future

            # 응답 처리
            if response.success:
                self.get_logger().info(f"Response from Table {table_id}: {response.response_message}")
            else:
                self.get_logger().warning(f"Failed response from Table {table_id}: {response.response_message}")
        except Exception as e:
            self.get_logger().error(f"Error calling service for Table {table_id}: {e}")

    def queue_soldout_request(self, table_id, message):
        """테이블별 품절 알림 요청을 큐에 추가."""
        self.soldout_queues[table_id].append(message)
        if not self.is_processing[table_id]:
            self.process_soldout_queue(table_id)

    def process_soldout_queue(self, table_id):
        """큐에서 요청을 처리."""
        if not self.soldout_queues[table_id]:
            self.is_processing[table_id] = False
            return

        self.is_processing[table_id] = True
        message = self.soldout_queues[table_id].popleft()

        asyncio.create_task(self.call_soldout_service(table_id, message))  # 비동기 호출 처리
        self.is_processing[table_id] = False

    def send_soldout_notifications(self, message):
        """모든 테이블에 품절 알림을 전송."""
        for table_id in range(1, 10):
            self.queue_soldout_request(table_id, message)



class PublishSubscribeManager(Node, QObject):
    new_order_signal = Signal(int, dict)  # 테이블 주문 신호
    soldout_signal = Signal(str)  # 품절 알림 신호

    def __init__(self, db_config, service_client_manager):
        super().__init__('publish_subscribe_manager')
        QObject.__init__(self)
        
        # Initialize database handler and inventory manager
        self.db_handler = DBHandler(**db_config)
        self.inventory_manager = InventoryManager(self.db_handler, self.stock_client)
        self.service_client_manager = service_client_manager
        self.notified_items = set()

        # QoS 설정 및 구독 생성
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            depth=10
        )
        self.subscribers = []
        for table_id in range(1, 10):
            topic_name = f'/table{table_id}/message'
            subscription = self.create_subscription(
                String,
                topic_name,
                self.listener_callback,
                qos_profile
            )
            self.subscribers.append(subscription)

        # 15초 주기로 품절 상태 확인
        self.timer = self.create_timer(15.0, self.check_stock)
        self.get_logger().info("PublishSubscribeManager initialized.")

        # GUI Callback placeholders
        self.gui_callback = None
        self.order_callback = None
    
    def set_gui_callback(self, callback):
        """Set the GUI callback for updating sold-out items."""
        self.gui_callback = callback
        
    def set_order_callback(self, callback):
        """Set the GUI callback for handling new orders."""
        self.order_callback = callback

    def listener_callback(self, msg):
        """테이블 메시지 구독 처리."""
        try:
            message = msg.data
            parsed_message = message.split(',')
            if len(parsed_message) < 3 or len(parsed_message) % 2 == 0:
                self.get_logger().warning(f"Received invalid message format: {message}")
                return  # 잘못된 메시지 무시
            
            table_id = int(parsed_message[0])
            items = {parsed_message[i]: int(parsed_message[i + 1]) for i in range(1, len(parsed_message), 2)}

            self.get_logger().info(f"Processing order for Table {table_id}: {items}")
            self.inventory_manager.process_order(items)
            self.db_handler.insert_order(table_id, items)
            self.new_order_signal.emit(table_id, items)  # GUI에 주문 정보 전달
        except Exception as e:
            self.get_logger().error(f"Error processing message: {e}")

    def check_stock(self):
        """15초마다 품절 상태를 확인하고 알림."""
        try:
            soldout_items = set(self.db_handler.get_soldout_items())
            new_items = soldout_items - self.notified_items

            if new_items:
                message = ", ".join(new_items)
                self.soldout_signal.emit(message)  # GUI에 팝업 알림
                self.notified_items.update(new_items)

                # 모든 테이블에 알림 요청
                for table_id in range(1, 10):
                    self.service_client_manager.queue_soldout_request(table_id, message)
        except Exception as e:
            self.get_logger().error(f"Error in stock check: {e}")

