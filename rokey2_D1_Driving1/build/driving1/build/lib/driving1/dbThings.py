import mysql.connector
import rclpy
from rclpy.node import Node
from datetime import datetime
import random
from driving1_interfaces.srv import NotifySoldout

# MySQL connection settings
config = {
    'user': 'jokbal',
    'password': 'JOKbal12345!!',
    'host': 'localhost',
    'database': 'jokDB',
}

class DBHandler:
    def __init__(self):
        self.config = config
        self.connect_database()

    def connect_database(self):
        """Connect to the MySQL database and create necessary tables."""
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            print("Database connection established.")

            self.create_tables()
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
        
    def create_tables(self):
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
        self.cursor.execute(create_customer_table)
        self.cursor.execute(create_product_table)
        self.cursor.execute(create_stock_table)
        print("Database tables created (if not exist).")

    def insert_order(self, table_id, items):
        """Insert order data into CUSTOMER and PRODUCT tables."""
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

            jokbal_mid = int(items.get("족발 중", 0))
            jokbal_lar = int(items.get("족발 대", 0))
            jinro = int(items.get("진로", 0))
            cham = int(items.get("참이슬", 0))

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
            SELECT 
                '족발 중' AS product_name, SUM(jokbal_mid_num * 36000) AS revenue
            FROM PRODUCT
            WHERE order_id IN (
                SELECT order_id FROM CUSTOMER WHERE order_date = %s
            )
            UNION ALL
            SELECT 
                '족발 대' AS product_name, SUM(jokbal_lar_num * 42000) AS revenue
            FROM PRODUCT
            WHERE order_id IN (
                SELECT order_id FROM CUSTOMER WHERE order_date = %s
            )
            UNION ALL
            SELECT 
                '진로' AS product_name, SUM(jinro_num * 5000) AS revenue
            FROM PRODUCT
            WHERE order_id IN (
                SELECT order_id FROM CUSTOMER WHERE order_date = %s
            )
            UNION ALL
            SELECT 
                '참이슬' AS product_name, SUM(cham_num * 5000) AS revenue
            FROM PRODUCT
            WHERE order_id IN (
                SELECT order_id FROM CUSTOMER WHERE order_date = %s
            )
            """
            self.cursor.execute(query, (date, date, date, date))
            result = self.cursor.fetchall()

            # Parse results
            revenue_by_product = {row[0]: row[1] or 0 for row in result}
            return revenue_by_product
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return {}

class StockUpdate:
    @staticmethod
    def update_stock():
        """Automatically update stock for today if not already updated."""
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            # Check if today's stock already exists
            cursor.execute("SELECT COUNT(*) FROM STOCK WHERE stock_date = CURRENT_DATE")
            result = cursor.fetchone()

            if result[0] == 0:
                update_query = """
                INSERT INTO STOCK (stock_date, jokbal_mid_stock, jokbal_lar_stock, jinro_stock, cham_stock)
                VALUES (CURRENT_DATE, 15, 15, 30, 30);
                """
                cursor.execute(update_query)
                conn.commit()
                print("Stock updated for the day.")
            else:
                print("Stock for today already exists. No update necessary.")
        except mysql.connector.Error as err:
            print(f"Error updating stock: {err}")
        finally:
            cursor.close()
            conn.close()
            
class InventoryManager:
    def __init__(self, stock_client):
        self.stock_client = stock_client

    def process_order(self, items):
        """Process the order and update stock."""
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            sold_out_products = []

            for item_name, quantity in items.items():
                quantity = int(quantity)
                stock_query = f"SELECT {item_name}_stock FROM STOCK WHERE stock_date = CURRENT_DATE"
                cursor.execute(stock_query)
                stock = cursor.fetchone()[0]

                if stock < quantity:
                    print(f"Not enough stock for {item_name}. Requested: {quantity}, Available: {stock}")
                    sold_out_products.append(item_name)  # Add to sold-out list
                else:
                    update_query = f"UPDATE STOCK SET {item_name}_stock = {item_name}_stock - %s WHERE stock_date = CURRENT_DATE"
                    cursor.execute(update_query, (quantity,))

            conn.commit()

            if sold_out_products:
                message = ", ".join(sold_out_products)
                self.stock_client.notify_soldout(message)

            return len(sold_out_products) == 0
        except mysql.connector.Error as err:
            print(f"Error processing order: {err}")
            return False
        finally:
            cursor.close()
            conn.close()



