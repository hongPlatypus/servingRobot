# main.py

import rclpy

from ros_kitchen_nodes import KitchenClient

from PySide2.QtWidgets import QApplication

from kitchen_gui import KitchenGUI

from datetime import datetime

import sys

import threading

from db_handler import StockUpdate,DBHandler



def main():

    rclpy.init()
    # Initialize QApplication
    app = QApplication(sys.argv)

    db_config = {

        'user': 'jokbal',

        'password': 'JOKbal12345!!',

        'host': 'localhost',

        'database': 'jokDB',

    }
    db_handler = DBHandler(**db_config)

    # Ensure stock is updated for the day
    today_date = datetime.now().strftime('%Y-%m-%d')
    StockUpdate.update_stock(db_handler, today_date)
    
    executor = rclpy.executors.MultiThreadedExecutor()
    nodes = []

    # PublisherNode 및 KitchenClient 초기화
    kitchen_client = KitchenClient(db_handler, None)  # KitchenClient 초기화
    nodes.append(kitchen_client)
    executor.add_node(kitchen_client)

    

    # Create KitchenGUI

    gui = KitchenGUI(kitchen_client,db_handler)

    # ROS 실행을 별도 스레드에서 실행

    def ros_spin():
        try:
            executor.spin()  # MultiThreadedExecutor 사용
        except KeyboardInterrupt:
            print("ROS interrupted.")
        finally:
            for node in nodes:
                node.destroy_node()
            executor.shutdown()



    ros_thread = threading.Thread(target=ros_spin, daemon=True)
    ros_thread.start()



    # UI 실행

    try:
        gui.show()  # PySide2에서 GUI 표시
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("Application interrupted.")
    finally:
        rclpy.shutdown()

def check_and_notify_stock(db_handler, order_items):
    stock_exceed = []
    for item, quantity in order_items.items():
        current_stock = db_handler.get_stock(item)
        if quantity > current_stock:
            stock_exceed.append(item)
    if stock_exceed:
        db_handler.publish_exceed_alert('/exceed_alert', ', '.join(stock_exceed))


if __name__ == '__main__':

    main()