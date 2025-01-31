from rclpy.node import Node
from std_msgs.msg import String
from PySide2.QtWidgets import QApplication, QMainWindow, QTextBrowser, QWidget, QPushButton, QMessageBox
from PySide2.QtCore import QRect, Signal
import sys
import rclpy
import sqlite3
import threading
from functools import partial
import argparse
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from datetime import datetime

class NODE(Node):
    def __init__(self, args):
        super().__init__('Jokkitchen')
        self.args = args
        self.table_num = int(self.args.table_num)
        self.emit_signal = None

        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            depth=10
        )

        # Subscribe to the "/order" topic
        self.subscription = self.create_subscription(
            String,
            '/order',
            self.subscription_callback,
            qos_profile
        )

    def subscription_callback(self, msg):
        message = msg.data
        self.get_logger().info(f"Received order: {message}")

        try:
            message_list = message.split(',')
            table_id = int(message_list[0])
            items = message_list[1:]
            if len(items) % 2 != 0:
                self.get_logger().error(f"Invalid message format: {message}")
            else:
                if self.emit_signal:
                    self.get_logger().info(f"Emitting signal: {message}")
                    self.emit_signal(message)
        except Exception as e:
            self.get_logger().error(f"Error parsing message: {e}")

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
        }  # 메뉴별 가격 설정

        self.setupUi()
        self.connect_database()

    def setupUi(self):
        self.setWindowTitle("Kitchen")
        self.resize(800, 800)
        self.centralwidget = QWidget(self)

        self.textBrowsers = []
        self.resetButtons = []

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

        self.revenueButton = QPushButton(self.centralwidget)
        self.revenueButton.setGeometry(QRect(20, 700, 240, 50))
        self.revenueButton.setText("Show Revenue")
        self.revenueButton.clicked.connect(self.button_clicked_showrevenue)

        self.allResetButton = QPushButton(self.centralwidget)
        self.allResetButton.setGeometry(QRect(280, 700, 240, 50))
        self.allResetButton.setText("All Reset")
        self.allResetButton.clicked.connect(self.button_clicked_all_reset)

        self.setCentralWidget(self.centralwidget)

    def connect_database(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_number INTEGER NOT NULL,
                manu TEXT NOT NULL,
                num INTEGER NOT NULL,
                time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def received_message(self, message):
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
                self.insert_data(table_id, items)
        except Exception as e:
            print(f"Error processing message in UI: {e}")

    def insert_data(self, table_id, items):
        try:
            if not (1 <= table_id <= self.node.table_num):
                print(f"Invalid table_id: {table_id}")
                return

            for i in range(0, len(items), 2):
                manu = items[i]
                num = int(items[i + 1])
                if manu not in self.price_list or num <= 0:
                    print(f"Invalid item or quantity: {manu}, {num}")
                    continue

                self.cursor.execute("INSERT INTO orders (table_number, manu, num) VALUES (?, ?, ?)", 
                                    (table_id, manu, num))
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting data into database: {e}")

    def button_clicked_showrevenue(self):
        try:
            today_date = datetime.now().strftime('%Y-%m-%d')
            self.cursor.execute("SELECT table_number, manu, num FROM orders WHERE strftime('%Y-%m-%d', time) = ?", (today_date,))
            rows = self.cursor.fetchall()

            print(f"Filtered Rows: {rows}")  # 오늘 날짜 데이터 디버깅

            total_revenue = 0
            table_revenues = {i: 0 for i in range(1, self.node.table_num + 1)}

            for table_number, manu, num in rows:
                if manu in self.price_list:
                    revenue = self.price_list[manu] * num
                    table_revenues[table_number] += revenue
                    total_revenue += revenue

            print(f"Table Revenues Debug: {table_revenues}")  # 테이블별 매출 디버깅

            details = "\n".join([
                f"Table {table}: {revenue} KRW" 
                for table, revenue in table_revenues.items() if revenue > 0
            ])

            messagebox = QMessageBox()
            messagebox.setWindowTitle("Today's Revenue")
            messagebox.setText(f"Revenue by Table:\n{details}\n\nTotal Revenue: {total_revenue} KRW")
            messagebox.exec_()
        except Exception as e:
            print(f"Error calculating revenue: {e}")

    def button_clicked_all_reset(self):
        try:
            self.cursor.execute("DELETE FROM orders")
            self.conn.commit()

            for browser in self.textBrowsers:
                browser.clear()
                browser.setPlainText("Table Reset")

            print("All data has been reset.")
        except Exception as e:
            print(f"Error resetting all data: {e}")

    def reset_table(self, table_id):
        if 1 <= table_id <= len(self.textBrowsers):
            browser = self.textBrowsers[table_id - 1]
            browser.clear()
            browser.setPlainText(f"Table {table_id} Reset")

            try:
                self.cursor.execute("DELETE FROM orders WHERE table_number = ?", (table_id,))
                self.conn.commit()
                print(f"Deleted all data for Table {table_id}")
            except Exception as e:
                print(f"Error resetting table {table_id}: {e}")

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
