import pymysql
import pandas as pd
import matplotlib.pyplot as plt

# MySQL connection settings
config = {
    'user': 'jokbal',
    'password': 'JOKbal12345!!',
    'host': 'localhost',
    'database': 'jokDB',
}

class RevenueAnalysis:
    def __init__(self, config):
        """
        MySQL 데이터베이스 연결 초기화
        :param config: MySQL 연결 설정 (딕셔너리 형태)
        """
        self.connection = pymysql.connect(
            user=config['user'],
            password=config['password'],
            host=config['host'],
            database=config['database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()

    def get_revenue_by_table(self, date):
        """
        주어진 날짜의 테이블별 매출 데이터를 가져옵니다.
        :param date: 조회할 날짜 (문자열, 'YYYY-MM-DD' 형식)
        :return: 테이블 ID를 키로 하고 매출 합계를 값으로 가지는 딕셔너리
        """
        query = """
        SELECT table_id, SUM(revenue) as total_revenue
        FROM revenues
        WHERE date = %s
        GROUP BY table_id
        """
        self.cursor.execute(query, (date,))
        result = {row['table_id']: row['total_revenue'] for row in self.cursor.fetchall()}
        return result

    def get_revenue_by_product(self, date):
        """
        주어진 날짜의 제품별 매출 데이터를 가져옵니다.
        :param date: 조회할 날짜 (문자열, 'YYYY-MM-DD' 형식)
        :return: 제품 ID를 키로 하고 매출 합계를 값으로 가지는 딕셔너리
        """
        query = """
        SELECT product_id, SUM(revenue) as total_revenue
        FROM revenues
        WHERE date = %s
        GROUP BY product_id
        """
        self.cursor.execute(query, (date,))
        result = {row['product_id']: row['total_revenue'] for row in self.cursor.fetchall()}
        return result

    def close(self):
        """
        데이터베이스 연결 닫기
        """
        self.cursor.close()
        self.connection.close()

    def analyze_revenue_by_table(self, date):
        """
        테이블별 매출 데이터를 분석하고 시각화
        :param date: 분석할 날짜 (문자열, 'YYYY-MM-DD' 형식)
        """
        revenue_data = self.get_revenue_by_table(date)
        df = pd.DataFrame(list(revenue_data.items()), columns=["Table ID", "Revenue"])

        # 시각화
        plt.figure(figsize=(10, 6))
        plt.bar(df["Table ID"], df["Revenue"])
        plt.title(f"Revenue by Table on {date}")
        plt.xlabel("Table ID")
        plt.ylabel("Revenue")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def analyze_revenue_by_product(self, date):
        """
        제품별 매출 데이터를 분석하고 시각화
        :param date: 분석할 날짜 (문자열, 'YYYY-MM-DD' 형식)
        """
        revenue_data = self.get_revenue_by_product(date)
        df = pd.DataFrame(list(revenue_data.items()), columns=["Product ID", "Revenue"])

        # 시각화
        plt.figure(figsize=(10, 6))
        plt.bar(df["Product ID"], df["Revenue"])
        plt.title(f"Revenue by Product on {date}")
        plt.xlabel("Product ID")
        plt.ylabel("Revenue")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # RevenueAnalysis 인스턴스 생성
    analysis = RevenueAnalysis(config)

    # 오늘 날짜
    today = "2025-01-25"

    # 테이블별 매출 분석
    print("테이블별 매출 분석")
    analysis.analyze_revenue_by_table(today)

    # 제품별 매출 분석
    print("제품별 매출 분석")
    analysis.analyze_revenue_by_product(today)

    # 데이터베이스 연결 닫기
    analysis.close()
