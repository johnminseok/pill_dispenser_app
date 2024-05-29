import sqlite3
import serial
import time
from datetime import datetime

def init_db():
    print("데이터베이스 초기화 시작")
    # 데이터베이스 연결
    conn = sqlite3.connect('DB/DataBase.db')
    c = conn.cursor()

    # 테이블 생성
    c.execute('''CREATE TABLE IF NOT EXISTS medication (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    medication_name TEXT,
                    container_number INTEGER,
                    time TEXT)''')
    print("테이블 생성 완료")

    # 기존 데이터 삭제
    c.execute('DELETE FROM medication')
    print("기존 데이터 삭제 완료")

    # 예시 데이터 삽입
    c.execute("INSERT INTO medication (name, medication_name, container_number, time) VALUES ('User1', 'Med1', 1, '22:51')")
    c.execute("INSERT INTO medication (name, medication_name, container_number, time) VALUES ('User2', 'Med2', 2, '22:44')")
    print("예시 데이터 삽입 완료")

    conn.commit()
    conn.close()
    print("데이터베이스 초기화 완료")

def check_and_send_signal():
    print("신호 확인 및 전송 시작")
    # 현재 시간 가져오기
    current_time = datetime.now().strftime('%H:%M')

    # 데이터베이스 연결
    conn = sqlite3.connect('DB/DataBase.db')
    c = conn.cursor()

    # 현재 시간과 일치하는 항목 조회
    c.execute("SELECT name, medication_name, container_number FROM medication WHERE time=?", (current_time,))
    rows = c.fetchall()

    # 일치하는 항목이 있으면 신호 전송
    if rows:
        for row in rows:
            name, medication_name, container_number = row
            print(f"사용자: {name}, 약 이름: {medication_name}, 약 통 번호: {container_number}, 시간: {current_time}")
            ser.write(b'1')  # 아두이노로 신호 전송

    conn.close()
    print("신호 확인 및 전송 완료")

if __name__ == "__main__":
    # 시리얼 포트와 통신 속도 설정
    ser = serial.Serial('/dev/ttyACM0', 9600)  # '/dev/ttyUSB0'는 아두이노가 연결된 포트
    time.sleep(2)  # 시리얼 통신 안정화 시간

    # 데이터베이스 초기화
    init_db()

    # 일정 주기마다 확인 (1분마다)
    while True:
        check_and_send_signal()
        time.sleep(60)  # 1분 대기
