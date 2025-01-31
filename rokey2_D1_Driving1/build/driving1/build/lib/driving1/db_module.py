import mysql.connector
import rclpy
from rclpy.node import Node
from example_interfaces.srv import Trigger  # ROS2 Trigger service type
from datetime import datetime
import random

# MySQL connection settings
config = {
    'user': 'jokbal',
    'password': 'JOKbal12345!!',
    'host': 'localhost',
    'database': 'jokDB',
}

class DBHandler:
    def __init__(self):
        self.config = {
            'user': 'jokbal',
            'password': 'JOKbal12345!!',
            'host': 'localhost',
            'database': 'jokDB',
        }
        self.connect_database()

    def connect_database(self):
        """Connect to the MySQL database and create necessary tables."""
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            print("Database connection established.")

            # 테이블 생성 SQL
            create_customer_table = """
            CREATE TABLE IF NOT EXISTS CUSTOMER (
                order_id INT NOT NULL AUTO_INCREMENT,
                order_table TINYINT NOT NULL CHECK (order_table BETWEEN 1 AND 9),
                order_date DATE NOT NULL,
                order_time TIME NOT NULL,
                card_info BIGINT NOT NULL,
                PRIMARY KEY (order_id)
            );
            """
            
            create_product_table = """
            CREATE TABLE IF NOT EXISTS PRODUCT (
                product_id INT NOT NULL AUTO_INCREMENT,
                order_id INT NOT NULL,
                order_table TINYINT NOT NULL CHECK (order_table BETWEEN 1 AND 9),
                jokbal_mid_num INT NOT NULL DEFAULT 0,
                jokbal_lar_num INT NOT NULL DEFAULT 0,
                jinro_num INT NOT NULL DEFAULT 0,
                cham_num INT NOT NULL DEFAULT 0,
                PRIMARY KEY (product_id),
                FOREIGN KEY (order_id) REFERENCES CUSTOMER(order_id)
            );
            """
            
            create_stock_table = """
            CREATE TABLE IF NOT EXISTS STOCK (
                stock_id INT NOT NULL AUTO_INCREMENT,
                stock_date DATE NOT NULL,
                jokbal_mid_stock INT NOT NULL DEFAULT 0,
                jokbal_lar_stock INT NOT NULL DEFAULT 0,
                jinro_stock INT NOT NULL DEFAULT 0,
                cham_stock INT NOT NULL DEFAULT 0,
                PRIMARY KEY (stock_id),
                UNIQUE (stock_date)
            );
            """
            
            # Execute table creation
            self.cursor.execute(create_customer_table)
            self.cursor.execute(create_product_table)
            self.cursor.execute(create_stock_table)

            print("Database tables created (if not exist).")
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")

    def insert_order(self, table_id, items):
        """Insert order data into the CUSTOMER and PRODUCT tables."""
        try:
            current_date = datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.now().strftime('%H:%M:%S')
            card_info = random.randint(1000000000000000, 9999999999999999)

            self.conn.start_transaction()

            customer_query = """
            INSERT INTO CUSTOMER (order_table, order_date, order_time, card_info)
            VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(customer_query, (table_id, current_date, current_time, card_info))
            order_id = self.cursor.lastrowid

            jokbal_mid = int(items[items.index('족발 중') + 1]) if '족발 중' in items else 0
            jokbal_lar = int(items[items.index('족발 대') + 1]) if '족발 대' in items else 0
            jinro = int(items[items.index('진로') + 1]) if '진로' in items else 0
            cham = int(items[items.index('참이슬') + 1]) if '참이슬' in items else 0

            product_query = """
            INSERT INTO PRODUCT (order_id, order_table, jokbal_mid_num, jokbal_lar_num, jinro_num, cham_num)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(product_query, (order_id, table_id, jokbal_mid, jokbal_lar, jinro, cham))

            self.conn.commit()
            print(f"Order successfully inserted for Table {table_id}.")
        except Exception as e:
            self.conn.rollback()
            print(f"Error inserting order into database: {e}")

    def get_revenue_by_product(self, date=None):
        """Return the total revenue by product for a given date."""
        if not date:
            date = datetime.today().strftime('%Y-%m-%d')

        try:
            query = """
            SELECT product_name, SUM(quantity * price) AS revenue
            FROM orders
            WHERE order_date = %s
            GROUP BY product_name
            """
            self.cursor.execute(query, (date,))
            result = self.cursor.fetchall()

            revenue_by_product = {}
            for row in result:
                product_name = row[0]
                revenue = row[1]
                revenue_by_product[product_name] = revenue

            return revenue_by_product
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return {}

class StockClient(Node):
    def __init__(self):
        super().__init__('stock_client')

        # Connect to MySQL
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()

    def update_stock(self):
        """Automatically update stock for today if not already updated"""
        try:
            # Check if there's already data for today
            self.cursor.execute("SELECT COUNT(*) FROM STOCK WHERE stock_date = CURRENT_DATE")
            result = self.cursor.fetchone()

            if result[0] == 0:
                update_stock_query = """
                INSERT INTO STOCK (stock_date, jokbal_mid_stock, jokbal_lar_stock, jinro_stock, cham_stock)
                VALUES (CURRENT_DATE, 15, 15, 30, 30);
                """
                self.cursor.execute(update_stock_query)
                self.conn.commit()
                self.get_logger().info("Stock updated for the day.")
            else:
                self.get_logger().info("Stock for today already exists. No update necessary.")
        except mysql.connector.Error as err:
            self.get_logger().error(f"Error updating stock: {err}")


class InventoryManager:
    def __init__(self):
        # Initialize the StockClient instance
        self.stock_client = StockClient()

    def check_stock(self, product_name):
        """Check if the product is in stock"""
        stock = self.stock_client.get_stock()
        return stock.get(product_name, 0)


    def process_order(self, items):
        """Process the order and update stock"""
        for item_name, quantity in items:
            quantity = int(quantity)
        return True

