from rclpy.node import Node
from std_msgs.msg import String
from PySide2.QtWidgets import QApplication, QMainWindow, QTextBrowser, QWidget, QPushButton, QMessageBox
from PySide2.QtCore import QRect, Signal
from functools import partial
from dbThings import DBHandler, InventoryManager, StockUpdate
import rclpy

from project3_interfaces.msg import TableCommand

class KitchenNODE(Node):
    def __init__(self, args):
        super().__init__('Jokkitchen_node')
        self.db_handler = DBHandler()
        self.inventory_manager = InventoryManager()
        self.subscription_list = [
            self.create_subscription(
                String, f'/table{i}/message', partial(self.process_order, i), 10
            ) for i in range(1, table_count + 1)
        ]


        
        # Update stock at the start of the program
        stock_updater = StockUpdate() 
        stock_updater.update_stock()  # Static method call without creating an instance


    # Publisher for cooking completion
        self.publisher = self.create_publisher(TableCommand, '/to_robot', qos_profile)
        
    def subscription_callback(self, msg, id):
        """Process incoming messages from tables."""
        #message = msg.data
        self.get_logger().info(f"Received message from table {id}: {message}")

        try:
            message_list = message.split(',')
            table_id = int(message_list[0])
            items = message_list[1:]
            if len(items) % 2 != 0:
                self.get_logger().error(f"Invalid message format: {message}")
            else:
                # Prepare items for order processing
                order_items = {items[i]: int(items[i + 1]) for i in range(0, len(items), 2)}

                # Check stock and process order
                if self.inventory_manager.process_order(order_items):
                    if self.emit_signal:
                        self.emit_signal(message)
                    self.db_handler.insert_order(table_id, order_items)
                else:
                    self.get_logger().error(f"Order processing failed for Table {table_id}")
        except Exception as e:
            self.get_logger().error(f"Error in subscription callback: {e}")
            
    def call_notify_soldout_service(self, message):
        """Call the /notify_soldout service with a message."""
        if not self.notify_soldout_client.wait_for_service(timeout_sec=2.0):
            self.get_logger().error("Service /notify_soldout not available")
            return

        request = NotifySoldout.Request()
        request.message = message  # Set the message to send
        future = self.notify_soldout_client.call_async(request)
        future.add_done_callback(self.notify_soldout_response_callback)

    def notify_soldout_response_callback(self, future):
        """Handle the response from /notify_soldout service."""
        try:
            response = future.result()
            if response.success:
                self.get_logger().info(f"Service responded: {response.response_message}")
            else:
                self.get_logger().error(f"Service failed: {response.response_message}")
        except Exception as e:
            self.get_logger().error(f"Error calling /notify_soldout service: {e}")


    def publish_cooking_complete(self, table_id):
        """Publish table completion with TableCommand message."""
        # Create TableCommand message
        msg = TableCommand()
        msg.to_robot = table_id  # Set the table_id field
        self.get_logger().info(f"Publishing cooking complete for Table {table_id}")
        self.publisher.publish(msg)


class GUI(QMainWindow):
    message_received = Signal(str)

    def __init__(self, node):
        super().__init__()
        self.node = node
        self.message_received.connect(self.received_message)
        self.sold_out_items = set()
        
        self.price_list = {
            '족발 중': 36000,
            '족발 대': 42000,
            '진로': 5000,
            '참이슬': 5000
        }

        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Kitchen")
        self.resize(800, 800)
        self.centralwidget = QWidget(self)

        self.textBrowsers = []
        self.resetButtons = []
        self.cookingCompleteButtons = []

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

    def notify_soldout(self):
        """Send a message to the /notify_soldout service."""
        message = "Item X is sold out."  # Example message
        self.node.call_notify_soldout_service(message)
        
    def received_message(self, message):
        try:
            message_list = message.split(',')
            table_id = int(message_list[0])
            items = message_list[1:]
            if len(items) % 2 == 0 and 1 <= table_id <= len(self.textBrowsers):
                browser = self.textBrowsers[table_id - 1]
                browser.append("\n".join([f"{items[i]} x{items[i + 1]}" for i in range(0, len(items), 2)]))
        except Exception as e:
            print(f"Error processing message in UI: {e}")

    def button_clicked_showrevenue_by_table(self):
        """Show revenue by table."""
        today = datetime.today().strftime('%Y-%m-%d')
        revenue_data = self.db_handler.get_revenue_by_table(today)  # DBHandler에서 데이터 가져오기
        revenue_message = "\n".join([f"Table {table}: {revenue}원" for table, revenue in revenue_data.items()])
        QMessageBox.information(self, "Revenue by Table", revenue_message)

    def button_clicked_showrevenue_by_product(self):
        """Show revenue by product."""
        today = datetime.today().strftime('%Y-%m-%d')
        revenue_data = self.db_handler.get_revenue_by_product(today)  # DBHandler에서 데이터 가져오기
        revenue_message = "\n".join([f"{product}: {revenue}원" for product, revenue in revenue_data.items()])
        QMessageBox.information(self, "Revenue by Product", revenue_message)
    
    def button_clicked_all_reset(self):
        for browser in self.textBrowsers:
            browser.clear()
            browser.setPlainText("Table Reset")
        print("All data has been reset.")

    def reset_table(self, table_id):
        if 1 <= table_id <= len(self.textBrowsers):
            browser = self.textBrowsers[table_id - 1]
            browser.clear()
            browser.setPlainText(f"Table {table_id} Reset")

    def on_cooking_complete(self, table_id):
        print(f"Cooking completed for Table {table_id}")
        self.node.publish_cooking_complete(str(table_id))
        
def clean_up(node, executor, executor_thread):
    executor.shutdown()
    node.destroy_node()
    rclpy.shutdown()
    executor_thread.join()

def main(args=sys.argv):
    rclpy.init(args=args)
    args = rclpy.utilities.remove_ros_args(args)

    parser = argparse.ArgumentParser()
    parser.add_argument('-table_num', type=int, default=9, help='Number of tables')
    args = parser.parse_args(args[1:])

    node = NODE(args)
    executor = MultiThreadedExecutor()  
    executor.add_node(node)
    
    app = QApplication(sys.argv)
    gui = GUI(node)
    gui.show()

    executor_thread = threading.Thread(target=executor.spin, daemon=True)
    executor_thread.start()
    

    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
    finally:
        clean_up(node, executor, executor_thread)

if __name__ == "__main__":
    main()
