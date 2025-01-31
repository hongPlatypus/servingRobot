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
    def __init__(self, **config):
        self.config = config
        self.conn = None
        self.cursor = None
        self.connect_database()

    def connect_database(self):
        """MySQL 데이터베이스 연결"""
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            print("Database connection established.")
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
            self.conn = None
            self.cursor = None

    def get_current_stock(self, item_name):
        """현재 재고량 확인"""
        field_mapping = {
            '족발 중': 'jokbal_mid_stock',
            '족발 대': 'jokbal_lar_stock',
            '진로': 'jinro_stock',
            '참이슬': 'cham_stock'
        }
        field_name = field_mapping.get(item_name)
        if not field_name:
            raise ValueError(f"Invalid item name: {item_name}")

        query = f"SELECT {field_name} FROM STOCK WHERE stock_date = CURRENT_DATE"
        try:
            self.cursor.execute(query)
            stock = self.cursor.fetchone()
            return stock[0] if stock else 0
        except mysql.connector.Error as err:
            print(f"Error retrieving stock for {item_name}: {err}")
            return 0




    def close_connection(self):

        """Close database connection and cursor."""

        if self.cursor:

            self.cursor.close()

        if self.conn:

            self.conn.close()

        self.cursor = None

        self.conn = None

        

    def ensure_connection(self):
        """Ensure the database connection is active, and reconnect if needed."""
        if not self.conn or not self.conn.is_connected():
            print("Reconnecting to the database...")
            try:
                self.connect_database()
            except mysql.connector.Error as err:
                print(f"Failed to reconnect: {err}")

    def execute_query(self, query, params=None):

        """Execute a query with automatic connection handling."""

        try:

            self.ensure_connection()

            self.cursor.execute(query, params or ())

        except mysql.connector.Error as err:

            print(f"Query execution error: {err}")

            raise

        

    def get_soldout_items(self):

        """Retrieve sold-out items from the STOCK table."""

        try:

            self.ensure_connection()

            query = """

            SELECT jokbal_mid_stock, jokbal_lar_stock, jinro_stock, cham_stock

            FROM STOCK WHERE stock_date = CURRENT_DATE

            """

            self.cursor.execute(query)

            result = self.cursor.fetchone()

            if not result:

                return []



            soldout_items = []

            stock_fields = ['족발 중', '족발 대', '진로', '참이슬']

            for field, value in zip(stock_fields, result):

                if value <= 0:

                    soldout_items.append(field)



            return soldout_items

        except mysql.connector.Error as err:

            print(f"Error retrieving sold-out items: {err}")

            return []



    def create_tables(self):

        self.ensure_connection()

        """Create necessary database tables."""

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

        self.ensure_connection()

        """Insert order data into CUSTOMER and PRODUCT tables."""

        try:

            current_date = datetime.now().strftime('%Y-%m-%d')

            current_time = datetime.now().strftime('%H:%M:%S')

            card_info = random.randint(1000000000000000, 9999999999999999)



            # Open a new connection for this operation

            with mysql.connector.connect(**self.config) as conn:

                with conn.cursor() as cursor:

                    # Start transaction

                    conn.start_transaction()



                    # Insert into CUSTOMER table

                    customer_query = """

                    INSERT INTO CUSTOMER (order_table, order_date, order_time, card_info)

                    VALUES (%s, %s, %s, %s)

                    """

                    cursor.execute(customer_query, (table_id, current_date, current_time, card_info))



                    # Get the newly generated order_id

                    order_id = cursor.lastrowid



                    # Insert into PRODUCT table

                    product_query = """

                    INSERT INTO PRODUCT (order_id, order_table, jokbal_mid_num, jokbal_lar_num, jinro_num, cham_num)

                    VALUES (%s, %s, %s, %s, %s, %s)

                    """

                    jokbal_mid = items.get("족발 중", 0)

                    jokbal_lar = items.get("족발 대", 0)

                    jinro = items.get("진로", 0)

                    cham = items.get("참이슬", 0)



                    cursor.execute(product_query, (order_id, table_id, jokbal_mid, jokbal_lar, jinro, cham))



                    # Commit transaction

                    conn.commit()

                    print(f"Order successfully inserted for Table {table_id} with Order ID {order_id}.")

        except mysql.connector.Error as e:

            print(f"Error inserting order into database: {e}")



    def get_revenue_by_product(self, date=None):

        """Return the total revenue by product for a given date."""

        self.ensure_connection()

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

        

    def get_revenue_by_table(self, date):

        self.ensure_connection()

        query = """

        SELECT C.order_table, SUM(

            P.jokbal_mid_num * 36000 + 

            P.jokbal_lar_num * 42000 + 

            P.jinro_num * 5000 + 

            P.cham_num * 5000

        ) AS total_revenue

        FROM CUSTOMER C

        JOIN PRODUCT P ON C.order_id = P.order_id

        WHERE C.order_date = %s

        GROUP BY C.order_table

        """

        self.cursor.execute(query, (date,))

        result = {row['order_table']: row['total_revenue'] for row in self.cursor.fetchall()}

        return result

    

    def reset_stock(self, date):

        """Reset stock for the given date, overwriting any existing data."""

        try:

            self.ensure_connection()

            query = """

            INSERT INTO STOCK (stock_date, jokbal_mid_stock, jokbal_lar_stock, jinro_stock, cham_stock)

            VALUES (%s, 15, 15, 30, 30)

            ON DUPLICATE KEY UPDATE 

                jokbal_mid_stock = 15, 

                jokbal_lar_stock = 15, 

                jinro_stock = 30, 

                cham_stock = 30

            """

            self.cursor.execute(query, (date,))

            self.conn.commit()

            print(f"Stock forcibly reset for {date}.")

        except mysql.connector.Error as err:

            print(f"Error resetting stock: {err}")



            



    

class InventoryManager:
    def __init__(self, db_handler, stock_client):
        self.db_handler = db_handler
        self.stock_client = stock_client

    def process_order(self, items):
        """Process the order and update stock."""
        try:
            self.db_handler.ensure_connection()  # 연결 확인 및 재연결

            field_mapping = {
                '족발 중': 'jokbal_mid_stock',
                '족발 대': 'jokbal_lar_stock',
                '진로': 'jinro_stock',
                '참이슬': 'cham_stock'
            }

            sold_out_products = []
            for item_name, quantity in items.items():
                field_name = field_mapping.get(item_name)
                if not field_name:
                    continue

                # 현재 재고 확인
                stock_query = f"SELECT {field_name} FROM STOCK WHERE stock_date = CURRENT_DATE"
                self.db_handler.cursor.execute(stock_query)
                stock = self.db_handler.cursor.fetchone()
                stock_value = stock[0] if stock else 0

                if stock_value < quantity:
                    sold_out_products.append((item_name, stock_value))
                else:
                    # 재고 감소
                    update_query = f"""
                    UPDATE STOCK SET {field_name} = {field_name} - %s
                    WHERE stock_date = CURRENT_DATE
                    """
                    self.db_handler.cursor.execute(update_query, (quantity,))

            self.db_handler.conn.commit()

            # 부족한 재고 알림
            if sold_out_products:
                self.notify_insufficient_stock(sold_out_products)

            return len(sold_out_products) == 0  # 모든 주문이 처리되었는지 여부 반환
        except mysql.connector.Error as e:
            print(f"Error processing order: {e}")
            return False

    def notify_insufficient_stock(self, sold_out_products):
        """부족한 재고를 ROS2 토픽으로 알림"""
        message = "재고 부족: "
        for item_name, stock in sold_out_products:
            message += f"{item_name} (재고: {stock}개), "
        message = message.strip(", ")

        # ROS2 메시지 발행
        self.stock_client.publish_message(message)
        print(f"Published insufficient stock alert: {message}")




class StockUpdate:

    @staticmethod

    def update_stock(db_handler, date):

        """Update stock for the given date only if no stock data exists."""

        try:

            db_handler.ensure_connection()  # 연결 확인 및 재연결

            db_handler.cursor.execute("SELECT COUNT(*) FROM STOCK WHERE stock_date = %s", (date,))

            result = db_handler.cursor.fetchone()



            if result[0] == 0:

                query_insert = """

                INSERT INTO STOCK (stock_date, jokbal_mid_stock, jokbal_lar_stock, jinro_stock, cham_stock)

                VALUES (%s, 15, 15, 30, 30)

                """

                db_handler.cursor.execute(query_insert, (date,))

                db_handler.conn.commit()

                print(f"Stock added for {date}.")

            else:

                print(f"Stock already exists for {date}. No update performed.")

        except mysql.connector.Error as err:

            print(f"Error updating stock: {err}")