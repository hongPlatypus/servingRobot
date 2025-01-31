from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QTextBrowser, QMessageBox
from PySide2.QtCore import QRect, Signal,Slot
from datetime import datetime
from db_handler import DBHandler  # DBHandler 가져오기
from functools import partial
import sys
from ros_kitchen_nodes import KitchenClient


class KitchenGUI(QMainWindow):
    new_order_signal = Signal(int, dict)  # 신호 정의: 테이블 ID와 주문 정보


    def __init__(self, kitchen_client):
        super().__init__()
        self.setWindowTitle("Kitchen Order GUI")
        self.setGeometry(100, 100, 800, 800)
        db_config = {'user': 'jokbal','password': 'JOKbal12345!!','host': 'localhost','database': 'jokDB',}
        
        # KitchenClient 객체 생성
        self.kitchen_client = kitchen_client
        self.kitchen_client.set_gui_callback(self.update_sold_out_items)
        self.kitchen_client.set_order_callback(self.handle_new_order)  # 새로운 주문 콜백 설정

        # DBHandler 인스턴스 생성
        self.db_handler = DBHandler()
        
        self.order_list = []
        self.sold_out_items = set()
        self.price_list = {
            '족발 중': 36000,
            '족발 대': 42000,
            '진로': 5000,
            '참이슬': 5000
        }

        self.setupUi()
        self.new_order_signal.connect(self.update_table_order)  # 신호 연결

    def setupUi(self):
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.textBrowsers = []
        self.resetButtons = []
        self.cookingCompleteButtons = []
        
        self.soldOutBrowser = QTextBrowser(self.centralwidget)
        self.soldOutBrowser.setGeometry(QRect(20, 20, 760, 100))
        self.soldOutBrowser.setPlainText("No sold-out items.")
        
        for i in range(1, 10):
            browser = QTextBrowser(self.centralwidget)
            browser.setGeometry(QRect(20 + ((i - 1) % 3) * 260, 20 + ((i - 1) // 3) * 220, 240, 160))
            browser.setPlainText(f"Table {i}")
            self.textBrowsers.append(browser)

            reset_button = QPushButton(self.centralwidget)
            reset_button.setGeometry(QRect(20 + ((i - 1) % 3) * 260, 190 + ((i - 1) // 3) * 220, 240, 30))
            reset_button.setText(f"Reset Table {i}")
            reset_button.clicked.connect(partial(self.reset_table,i))
            self.resetButtons.append(reset_button)

            cooking_complete_button = QPushButton(self.centralwidget)
            cooking_complete_button.setGeometry(QRect(20 + ((i - 1) % 3) * 260, 230 + ((i - 1) // 3) * 220, 240, 30))
            cooking_complete_button.setText(f"Cooking Complete Table {i}")
            cooking_complete_button.clicked.connect(partial(self.on_cooking_complete, table = i))
            self.cookingCompleteButtons.append(cooking_complete_button)

        self.revenueButton = QPushButton(self.centralwidget)
        self.revenueButton.setGeometry(QRect(20, 700, 240, 50))
        self.revenueButton.setText("Show Revenue (By Table)")
        self.revenueButton.clicked.connect(self.show_revenue_by_table)

        self.productRevenueButton = QPushButton(self.centralwidget)
        self.productRevenueButton.setGeometry(QRect(280, 700, 240, 50))
        self.productRevenueButton.setText("Show Revenue (By Product)")
        self.productRevenueButton.clicked.connect(self.show_revenue_by_product)

        self.allResetButton = QPushButton(self.centralwidget)
        self.allResetButton.setGeometry(QRect(540, 700, 240, 50))
        self.allResetButton.setText("All Reset")
        self.allResetButton.clicked.connect(self.reset_all_tables)

        self.soldOutButton = QPushButton(self.centralwidget)
        self.soldOutButton.setGeometry(QRect(20,630,240,50))
        self.soldOutButton.setText("Notify Sold-Out")
        self.soldOutButton.clicked.connect(self.notify_sold_out_items)
        
        self.resetStockButton = QPushButton(self.centralwidget)
        self.resetStockButton.setGeometry(QRect(540, 630, 240, 50))  # 위치 및 크기 설정
        self.resetStockButton.setText("Reset Stock")
        self.resetStockButton.clicked.connect(self.reset_stock)  # 버튼 클릭 시 메서드 연결

        
        
    def reset_stock(self):
        """Reset stock levels for all items."""
        today = datetime.today().strftime('%Y-%m-%d')
        try:
            self.db_handler.reset_stock(today)  # DBHandler에서 재고 초기화
            QMessageBox.information(self, "Stock Reset", "Stock levels have been reset successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to reset stock: {e}")

    def on_cooking_complete(self, table_id):
        """Cooking Complete 버튼 클릭 시 로봇을 해당 테이블로 보내는 Topic Publish"""
        QMessageBox.information(self, "Cooking Complete", f"Cooking completed for Table {table_id}")
        # KitchenPublisher를 사용하여 로봇에게 명령 발행
        command = "go_to_table"
        self.kitchen_client.publish_to_robot(table_id, command)

    def reset_table(self,table_id):
        "특정 테이블의 주문 정보와 GUI 초기화"
        #주문 정보 초기화
        self.order_list = [order for order in self.order_list if order['table_id'] !=table_id]
        #GUI 초기화
        browser = self.textBrowsers[table_id -1]
        browser.clear()
        browser.setPlainText(f"Table {table_id} Reset")
        
    def reset_all_tables(self):
        """모든 테이블의 주문 정보와 gui 초기화"""
        self.order_list.clear()
        for i, browser in enumerate(self.textBrowsers):
            browser.clear()
            browser.setPlainText(f"Table {i+1} Reset")

    
    def show_revenue_by_table(self):
        """오늘의 테이블별 매출 정보를 팝업창에 표시."""
        today = datetime.today().strftime('%Y-%m-%d')  # 오늘 날짜
        try:
            result = self.db_handler.get_revenue_by_table(today)  # DBHandler에서 테이블별 매출 가져오기
            if not result:
                QMessageBox.information(self, "Revenue by Table", "No revenue data found for today.")
                return
            
            # 매출 데이터를 포맷팅
            revenue_message = "\n".join([f"Table {table_id}: {revenue:,}원" for table_id, revenue in result.items()])
            QMessageBox.information(self, "Revenue by Table", revenue_message)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to retrieve revenue by table: {e}")

    def show_revenue_by_product(self):
        """오늘의 제품별 매출 정보를 팝업창에 표시."""
        today = datetime.today().strftime('%Y-%m-%d')  # 오늘 날짜
        try:
            result = self.db_handler.get_revenue_by_product(today)  # DBHandler에서 제품별 매출 가져오기
            if not result:
                QMessageBox.information(self, "Revenue by Product", "No revenue data found for today.")
                return

            # 매출 데이터를 포맷팅
            revenue_message = "\n".join([f"{product}: {revenue:,}원" for product, revenue in result.items()])
            QMessageBox.information(self, "Revenue by Product", revenue_message)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to retrieve revenue by product: {e}")

    def notify_sold_out_items(self):
        soldout_items = self.db_handler.get_soldout_items()
        if soldout_items:
            message = ", ".join(soldout_items)
            QMessageBox.information(self, "Sold-Out Notification", f"Notifying sold-out items: {message}")
            self.kitchen_client.notify_soldout(message)
        else:
            QMessageBox.information(self,"No Sold-out Items", "All items are in stock.")
            
    @Slot(str)
    def update_sold_out_items(self, message):
        """메인 스레드에서 실행되는 GUI 업데이트"""
        self.soldOutBrowser.clear()
        self.soldOutBrowser.setPlainText(f"Sold-out items: {message}")
        QMessageBox.information(self, "Sold-Out Notification", f"Sold-out items detected:\n{message}")
    
    @Slot(int, dict)
    def update_table_order(self, table_id, items):
        """테이블의 주문 정보를 GUI에 업데이트"""
        browser = self.textBrowsers[table_id - 1]
        order_details = "\n".join([f"{item}: {quantity}" for item, quantity in items.items()])
        browser.setPlainText(f"Table {table_id} Order:\n{order_details}")

    def handle_new_order(self, table_id, items):
        """KitchenClient에서 전달된 주문 정보를 처리"""
        self.new_order_signal.emit(table_id, items)