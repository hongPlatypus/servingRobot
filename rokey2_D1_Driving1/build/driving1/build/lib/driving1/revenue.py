# revenue.py
from db_module import DBHandler
from datetime import datetime

class RevenueManager:
    def __init__(self):
        self.db_handler = DBHandler()  # DBHandler 인스턴스 생성

    def get_revenue_by_table(self, date=None):
        """Return the total revenue by table for a given date."""
        if not date:
            date = datetime.today().strftime('%Y-%m-%d')
        
        revenue_data = self.db_handler.get_revenue_by_table(date)
        return revenue_data

    def get_revenue_by_product(self, date=None):
        """Return the total revenue by product for a given date."""
        if not date:
            date = datetime.today().strftime('%Y-%m-%d')
        
        revenue_data = self.db_handler.get_revenue_by_product(date)
        return revenue_data
