import mysql.connector
from mysql.connector import errorcode

# MySQL 연결 설정
config = {
    'user': 'jokbal',         # MySQL 사용자 이름
    'password': 'JOKbal12345!!',  # MySQL 비밀번호
    'host': 'localhost',    # MySQL 서버 주소
    'database': 'jokDB',  # 사용할 데이터베이스 이름
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

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
        jokbal_mid_num INT NOT NULL,
        jokbal_lar_num INT NOT NULL,
        jinro_num INT NOT NULL,
        cham_num INT NOT NULL,
        PRIMARY KEY (product_id),
        FOREIGN KEY (order_id) REFERENCES CUSTOMER(order_id)
    );
    """

    create_stock_table = """
    CREATE TABLE IF NOT EXISTS STOCK (
        stock_id INT NOT NULL AUTO_INCREMENT,
        stock_date DATE NOT NULL,
        jokbal_mid_stock INT NOT NULL,
        jokbal_lar_stock INT NOT NULL,
        jinro_stock INT NOT NULL,
        cham_stock INT NOT NULL,
        PRIMARY KEY (stock_id),
        UNIQUE (stock_date)  -- stock_date를 유니크하게 설정하여 하루에 한 번만 저장되도록 함
    );
    """

    # 테이블 생성 실행
    cursor.execute(create_customer_table)
    cursor.execute(create_product_table)
    cursor.execute(create_stock_table)

    # 데이터 삽입 SQL
    insert_customer = """
    INSERT INTO CUSTOMER (order_table, order_date, order_time, card_info)
    VALUES (5, '2025-01-23', '14:30:00', 1234567890123456);
    """
    
    # 먼저 CUSTOMER 테이블에 데이터 삽입
    cursor.execute(insert_customer)
    conn.commit()

    # 방금 삽입한 order_id 가져오기
    order_id = cursor.lastrowid

    insert_product = """
    INSERT INTO PRODUCT (order_id, order_table, jokbal_mid_num, jokbal_lar_num, jinro_num, cham_num)
    VALUES (%s, 5, 50, 30, 100, 200);
    """

    # PRODUCT 테이블에 데이터 삽입
    cursor.execute(insert_product, (order_id,))
    conn.commit()

    print("Tables created and data inserted successfully.")

    # STOCK 자동 업데이트 스케줄링 함수
    def update_stock():
        try:
            # 이미 오늘 날짜의 데이터가 있는지 확인
            cursor.execute("SELECT COUNT(*) FROM STOCK WHERE stock_date = CURRENT_DATE")
            result = cursor.fetchone()

            # 오늘 날짜의 데이터가 없다면 삽입
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
        except mysql.connector.Error as err:
            print("Error updating stock:", err)

    # 매일 자동 업데이트 (시뮬레이션)
    for i in range(5):  # 예: 5일 동안 업데이트
        update_stock()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Access denied: Check your user name or password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist.")
    else:
        print(err)

finally:
    # 커서 및 연결 종료
    try:
        if cursor:
            cursor.close()
    except NameError:
        pass

    try:
        if conn:
            conn.close()
    except NameError:
        pass
