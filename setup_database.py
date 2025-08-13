import pandas as pd
import sqlite3
import os

# 새 데이터베이스 파일 이름
DB_FILE = "books.db"
# 읽어올 CSV 파일 이름
CSV_FILE = "lawlib.csv" 
# 데이터베이스에 생성할 테이블 이름
TABLE_NAME = "books"

# --- 스크립트 시작 ---

# 1. 기존 DB 파일이 있다면 삭제 (새로운 데이터로 완전히 교체하기 위함)
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"기존 '{DB_FILE}' 파일을 삭제했습니다.")

# 2. lawlib.csv 파일을 pandas로 읽기
try:
    df = pd.read_csv(CSV_FILE)
    print(f"'{CSV_FILE}' 파일을 성공적으로 읽었습니다.")
except FileNotFoundError:
    print(f"오류: '{CSV_FILE}' 파일을 찾을 수 없습니다. 파일이 올바른 위치에 있는지 확인하세요.")
    exit()

# 3. SQLite 데이터베이스에 연결하고 데이터 넣기
conn = sqlite3.connect(DB_FILE)
print(f"'{DB_FILE}' 데이터베이스에 연결했습니다.")

# pandas 데이터프레임을 SQL 테이블로 저장
# to_sql 함수는 데이터를 테이블에 삽입하는 역할을 합니다.
# if_exists='replace'는 테이블이 이미 존재하면 기존 내용을 지우고 새로 만듭니다.
df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)

print(f"'{TABLE_NAME}' 테이블에 데이터를 성공적으로 저장했습니다.")

# 4. 연결 종료
conn.close()
print(f"'{DB_FILE}' 파일이 성공적으로 생성되었고, 데이터베이스 연결을 닫았습니다.")
