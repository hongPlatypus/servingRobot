from rclpy.node import Node
from std_msgs.msg import String
from PySide2.QtWidgets import QApplication, QMainWindow, QTextBrowser, QWidget, QPushButton, QMessageBox
from PySide2.QtCore import QRect, Signal
import sys
import rclpy
import threading
from functools import partial
import argparse
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from datetime import datetime
import random
from db_module import DBHandler
from inventory import InventoryManager  # Use InventoryManager
from revenue import RevenueManager  # Import RevenueManager

class NODE(Node):
    def __init__(self, args):
        super().__init__('Jokkitchen')
        self.args = args
        self.table_num = int(self.args.table_num)
        self.emit_signal = None
        self.db_handler = DBHandler()# DBHandler 인스턴스 생성
        self.inventory_manager = InventoryManager()  # InventoryManager instance


        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            depth=10
        )

        # Create subscriptions for each table
        self.subscription_list = [
            self.create_subscription(
                String,
                f'/table{i}/message',
                partial(self.subscription_callback, id=i),
                qos_profile
            ) for i in range(1, self.table_num + 1)
        ]

        # Publisher for /table_number
        self.publisher = self.create_publisher(String, '/table_number', qos_profile)

    def subscription_callback(self, msg, id):
        """Process incoming messages from tables."""
        message = msg.data
        self.get_logger().info(f"Received message from table {id}: {message}")

        try:
            message_list = message.split(',')
            table_id = int(message_list[0])
            items = message_list[1:]
            if len(items) % 2 != 0:
                self.get_logger().error(f"Invalid message format: {message}")
            else:
                # Prepare items for order processing
                order_items = [(items[i], items[i + 1]) for i in range(0, len(items), 2)]

                # Check stock for each item individually
                for item, quantity in order_items:
                    stock_status = self.inventory_manager.check_stock(item)  # 수정된 부분
                    if stock_status < int(quantity):
                        self.get_logger().error(f"Insufficient stock for {item}")
                        return  # If any item has insufficient stock, return early

                # Process the order and update stock
                if self.inventory_manager.process_order(order_items):
                    # If stock is sufficient, insert into database and continue
                    if self.emit_signal:
                        self.get_logger().info(f"Emitting signal: {message}")
                        self.emit_signal(message)
                    self.db_handler.insert_order(table_id, items)
                else:
                    self.get_logger().error(f"Failed to process order for table {table_id}")
        except Exception as e:
            self.get_logger().error(f"Error parsing message: {e}")
            
    def publish_cooking_complete(self, table_id):
        """Publish table number when cooking is complete."""
        msg = String()
        msg.data = str(table_id)
        self.get_logger().info(f"Publishing cooking complete for Table {table_id}")
        self.publisher.publish(msg)


class GUI(QMainWindow):
    message_received = Signal(str)

    def __init__(self, node):
        super().__init__()
        self.node = node
        self.message_received.connect(self.received_message)

        self.price_list = {
            '족발 중': 36000,
            '족발 대': 42000,
            '진로': 5000,
            '참이슬': 5000
        }  # Menu price settings

        # Create instance of RevenueManager
        self.revenue_manager = RevenueManager()
        
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Kitchen")
        self.resize(800, 800)
        self.centralwidget = QWidget(self)

        self.textBrowsers = []
        self.resetButtons = []
        self.cookingCompleteButtons = []  # List to store cooking complete buttons

        for i in range(self.node.table_num):
            browser = QTextBrowser(self.centralwidget)
            browser.setGeometry(QRect(20 + (i % 3) * 260, 20 + (i // 3) * 220, 240, 160))
            browser.setObjectName(f"textBrowser_table{i + 1}")
            browser.setPlainText(f"Table {i + 1}")
            self.textBrowsers.append(browser)

            reset_button = QPushButton(self.centralwidget)
            reset_button.setGeometry(QRect(20 + (i % 3) * 260, 190 + (i // 3) * 220, 240, 30))
            reset_button.setText(f"Reset Table {i + 1}")
            reset_button.clicked.connect(partial(self.reset_table, i + 1))
            self.resetButtons.append(reset_button)

            cooking_complete_button = QPushButton(self.centralwidget)
            cooking_complete_button.setGeometry(QRect(20 + (i % 3) * 260, 230 + (i // 3) * 220, 240, 30))
            cooking_complete_button.setText(f"Cooking Complete Table {i + 1}")
            cooking_complete_button.clicked.connect(partial(self.on_cooking_complete, i + 1))
            self.cookingCompleteButtons.append(cooking_complete_button)

        # Buttons for revenue and reset
        self.revenueButton = QPushButton(self.centralwidget)
        self.revenueButton.setGeometry(QRect(20, 700, 240, 50))
        self.revenueButton.setText("Show Revenue (By Table)")
        self.revenueButton.clicked.connect(self.button_clicked_showrevenue_by_table)

        self.productRevenueButton = QPushButton(self.centralwidget)
        self.productRevenueButton.setGeometry(QRect(280, 700, 240, 50))
        self.productRevenueButton.setText("Show Revenue (By Product)")
        self.productRevenueButton.clicked.connect(self.button_clicked_showrevenue_by_product)

        self.allResetButton = QPushButton(self.centralwidget)
        self.allResetButton.setGeometry(QRect(540, 700, 240, 50))
        self.allResetButton.setText("All Reset")
        self.allResetButton.clicked.connect(self.button_clicked_all_reset)

        self.setCentralWidget(self.centralwidget)

    def received_message(self, message):
        """Handle received messages and update the GUI."""
        try:
            message_list = message.split(',')
            table_id = int(message_list[0])
            items = message_list[1:]

            if len(items) % 2 != 0:
                print(f"Invalid items list: {items}")
                return

            if 1 <= table_id <= len(self.textBrowsers):
                browser = self.textBrowsers[table_id - 1]
                browser.append("\n".join([f"{items[i]} x{items[i + 1]}" for i in range(0, len(items), 2)]))
        except Exception as e:
            print(f"Error processing message in UI: {e}")

    def button_clicked_showrevenue_by_table(self):
        """Show revenue by table."""
        today = datetime.today().strftime('%Y-%m-%d')
        revenue_data = self.revenue_manager.get_revenue_by_table(today)
        
        revenue_message = "\n".join([f"Table {table}: {revenue}원" for table, revenue in revenue_data.items()])
        QMessageBox.information(self, "Revenue by Table", revenue_message)

    def button_clicked_showrevenue_by_product(self):
        """Show revenue by product."""
        today = datetime.today().strftime('%Y-%m-%d')
        revenue_data = self.revenue_manager.get_revenue_by_product(today)

        revenue_message = "\n".join([f"{product}: {revenue}원" for product, revenue in revenue_data.items()])
        QMessageBox.information(self, "Revenue by Product", revenue_message)

    def button_clicked_all_reset(self):
        """Reset all tables."""
        for browser in self.textBrowsers:
            browser.clear()
            browser.setPlainText("Table Reset")
        print("All data has been reset.")

    def reset_table(self, table_id):
        """Reset the table display."""
        if 1 <= table_id <= len(self.textBrowsers):
            browser = self.textBrowsers[table_id - 1]
            browser.clear()
            browser.setPlainText(f"Table {table_id} Reset")

    def on_cooking_complete(self, table_id):
        """Handle cooking complete action."""
        print(f"Cooking completed for Table {table_id}")
        self.node.publish_cooking_complete(table_id)


def main(args=sys.argv):
    rclpy.init(args=args)
    args = rclpy.utilities.remove_ros_args(args)

    parser = argparse.ArgumentParser()
    parser.add_argument('-table_num', type=int, default=9, help='Number of tables')
    args = parser.parse_args(args[1:])

    node = NODE(args)
    ros_thread = threading.Thread(target=lambda: rclpy.spin(node), daemon=True)
    ros_thread.start()
    
    
    app = QApplication(sys.argv)
    gui = GUI(node)
    gui.show()

    node.emit_signal = gui.message_received.emit

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("Program interrupted.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
