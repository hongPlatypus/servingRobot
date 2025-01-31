# ui_handler.py
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QMainWindow, QMessageBox, QPushButton, QTextBrowser, QWidget
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QRect
from functools import partial
from datetime import datetime

class GUI(QMainWindow):
    message_received = Signal(str)

    def __init__(self, node):
        super().__init__()
        self.node = node
        self.message_received.connect(self.received_message)
        self.sold_out_items = set()
        self.node.gui = self  # Link the GUI to KitchenClient
        self.setupUi()
        
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

        for i in range(1, 10):  # Adjusted to create a fixed number of table widgets
            browser = QTextBrowser(self.centralwidget)
            browser.setGeometry(QRect(20 + ((i - 1) % 3) * 260, 20 + ((i - 1) // 3) * 220, 240, 160))
            browser.setObjectName(f"textBrowser_table{i}")
            browser.setPlainText(f"Table {i}")
            self.textBrowsers.append(browser)

            reset_button = QPushButton(self.centralwidget)
            reset_button.setGeometry(QRect(20 + ((i - 1) % 3) * 260, 190 + ((i - 1) // 3) * 220, 240, 30))
            reset_button.setText(f"Reset Table {i}")
            reset_button.clicked.connect(partial(self.reset_table, i))
            self.resetButtons.append(reset_button)

            cooking_complete_button = QPushButton(self.centralwidget)
            cooking_complete_button.setGeometry(QRect(20 + ((i - 1) % 3) * 260, 230 + ((i - 1) // 3) * 220, 240, 30))
            cooking_complete_button.setText(f"Cooking Complete Table {i}")
            cooking_complete_button.clicked.connect(partial(self.on_cooking_complete, i))
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
        revenue_data = self.node.get_revenue_by_table(today)  # DBHandler에서 데이터 가져오기
        revenue_message = "\n".join([f"Table {table}: {revenue}원" for table, revenue in revenue_data.items()])
        QMessageBox.information(self, "Revenue by Table", revenue_message)

    def button_clicked_showrevenue_by_product(self):
        """Show revenue by product."""
        today = datetime.today().strftime('%Y-%m-%d')
        revenue_data = self.node.get_revenue_by_product(today)  # DBHandler에서 데이터 가져오기
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
        
    def update_order_display(self, table_id, items):
        """Update the GUI with only the new order data."""
        try:
            # Find the text browser corresponding to the table
            browser = self.textBrowsers[table_id - 1]  # Assuming textBrowsers is a list of QTextBrowsers for each table

            # Format the new order data
            display_text = "\n".join([f"{item}: {quantity}" for item, quantity in items.items()])

            # Append only the new order details
            browser.append(f"New Order:\n{display_text}")
        except IndexError:
            print(f"Invalid table ID: {table_id}")
        except Exception as e:
            print(f"Error updating order display: {e}")
