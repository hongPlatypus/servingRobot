import mysql.connector
from rclpy.node import Node
from example_interfaces.srv import Trigger  # ROS2 Trigger service type

# MySQL connection settings
config = {
    'user': 'jokbal',
    'password': 'JOKbal12345!!',
    'host': 'localhost',
    'database': 'jokDB',
}

class StockClient(Node):
    def __init__(self):
        super().__init__('stock_client')

        # Service clients for sold-out services
        self.soldout_client = self.create_client(Trigger, '/soldout')
        self.soldout_approve_client = self.create_client(Trigger, '/soldout_approve')

        # Timer to periodically check stock and publish sold-out message
        self.timer = self.create_timer(5.0, self.check_and_publish_soldout)

        # Connect to MySQL
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()


    def check_and_publish_soldout(self):
        """Check stock from DB and publish sold-out products"""
        try:
            self.cursor.execute("SELECT * FROM STOCK WHERE stock_date = CURDATE()")
            stocks = self.cursor.fetchall()

            sold_out_products = []
            for stock in stocks:
                stock_id, stock_date, jokbal_mid_stock, jokbal_lar_stock, jinro_stock, cham_stock = stock
                if jokbal_mid_stock == 0:
                    sold_out_products.append("족발 중")
                if jokbal_lar_stock == 0:
                    sold_out_products.append("족발 대")
                if jinro_stock == 0:
                    sold_out_products.append("진로")
                if cham_stock == 0:
                    sold_out_products.append("참이슬")

            if sold_out_products:
                message = ", ".join(sold_out_products)
                self.call_soldout_service(message)
            else:
                self.get_logger().info("All products are in stock")

        except mysql.connector.Error as err:
            self.get_logger().error(f"Database error: {err}")

    def call_soldout_service(self, soldout_message):
        """Call the /soldout service to notify sold-out items"""
        if not self.soldout_client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error("Service /soldout is not available")
            return

        request = Trigger.Request()
        request.message = soldout_message

        future = self.soldout_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            response = future.result()
            self.get_logger().info(f"Sold-out response: {response.message}")
        else:
            self.get_logger().error("Failed to call /soldout service")

    def get_stock(self):
        """Retrieve current stock status from the database for today."""
        try:
            self.cursor.execute("SELECT * FROM STOCK WHERE stock_date = CURDATE()")
            stocks = self.cursor.fetchall()

            stock_status = {}
            for stock in stocks:
                stock_id, stock_date, jokbal_mid_stock, jokbal_lar_stock, jinro_stock, cham_stock = stock
                stock_status["족발 중"] = jokbal_mid_stock
                stock_status["족발 대"] = jokbal_lar_stock
                stock_status["진로"] = jinro_stock
                stock_status["참이슬"] = cham_stock

            return stock_status  # Returns a dictionary of today's stock status
        except mysql.connector.Error as err:
            self.get_logger().error(f"Database error: {err}")
            return {}

    def check_stock(self, product_name):
        """Check if the product is in stock (by product name)."""
        stock_status = self.get_stock()  # Get all stock data
        return stock_status.get(product_name, 0)  # Return stock for the specific product, default to 0 if not found
class StockUpdate:
    @staticmethod
    def update_stock():
        """Automatically update stock for today if not already updated"""
        try:
            # Connect to MySQL
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            # Check if there's already data for today
            cursor.execute("SELECT COUNT(*) FROM STOCK WHERE stock_date = CURRENT_DATE")
            result = cursor.fetchone()

            if result[0] == 0:
                update_stock_query = """
                INSERT INTO STOCK (stock_date, jokbal_mid_stock, jokbal_lar_stock, jinro_stock, cham_stock)
                VALUES (CURRENT_DATE, 15, 15, 30, 30);
                """
                cursor.execute(update_stock_query)
                conn.commit()
                print("Stock updated for the day.")
            else:
                print("Stock for today already exists. No update necessary.")
            
            # Close connection
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Error updating stock: {err}")