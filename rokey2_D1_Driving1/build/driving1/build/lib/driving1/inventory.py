from dbStock import StockClient  # Import StockClient for interacting with the stock database

class InventoryManager:
    def __init__(self):
        # Initialize the StockClient instance
        self.stock_client = StockClient()

    def check_stock(self, product_name):
        """Check if the product is in stock"""
        # get_stock should return a dictionary with product names as keys and stock as values
        stock = self.stock_client.get_stock()  # Assuming get_stock returns a dictionary
        return stock.get(product_name, 0)  # Get stock for the specific product, default to 0 if not found

    def update_stock(self, product_name, quantity):
        """Update the stock of a given product after an order"""
        current_stock = self.check_stock(product_name)
        if current_stock >= quantity:
            new_stock = current_stock - quantity
            self.stock_client.update_stock(product_name, new_stock)  # Assuming this method exists in StockClient
            return True
        else:
            return False

    def process_order(self, items):
        """Process the order and update stock"""
        for item_name, quantity in items:
            quantity = int(quantity)
            if not self.update_stock(item_name, quantity):
                print(f"Not enough stock for {item_name}")
                return False
        return True
