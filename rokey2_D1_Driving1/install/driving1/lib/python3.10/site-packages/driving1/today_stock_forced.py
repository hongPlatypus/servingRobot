import mysql.connector
from datetime import datetime

# MySQL 설정
config = {
    'user': 'jokbal',
    'password': 'JOKbal12345!!',
    'host': 'localhost',
    'database': 'jokDB'
}

class StockUpdate:
    @staticmethod
    def force_reset_stock():
        """오늘 날짜의 재고를 강제로 초기화 (기존 데이터 무시하고 덮어씀)"""
        try:
            # 데이터베이스 연결
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            # 오늘 날짜 가져오기
            today_date = datetime.today().strftime('%Y-%m-%d')

            # 기존 데이터를 삭제 (필요한 경우)
            cursor.execute("DELETE FROM STOCK WHERE stock_date = %s", (today_date,))

            # 무조건 새로운 재고 삽입
            query_insert = """
            INSERT INTO STOCK (stock_date, jokbal_mid_stock, jokbal_lar_stock, jinro_stock, cham_stock)
            VALUES (%s, 15, 15, 30, 30)
            """
            cursor.execute(query_insert, (today_date,))
            conn.commit()
            print(f"✅ Stock forcibly reset for {today_date}.")

        except mysql.connector.Error as err:
            print(f"❌ Error resetting stock: {err}")
        finally:
            # 연결 닫기
            if cursor:
                cursor.close()
            if conn:
                conn.close()

# 실행 예제
if __name__ == "__main__":
    StockUpdate.force_reset_stock()
