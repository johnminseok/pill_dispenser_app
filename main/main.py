# main.py

import serial
import sqlite3
import time
from datetime import datetime
import os

# 시리얼 포트와 통신 속도 설정
ser = serial.Serial('/dev/ttyACM0', 9600)  # '/dev/ttyUSB0'는 아두이노가 연결된 포트
time.sleep(2)  # 시리얼 통신 안정화 시간

def check_and_send_signal():
    # 현재 시간 가져오기
    current_time = datetime.now().strftime('%H:%M')
    print(f"현재 시간: {current_time}")

    # 프로젝트 디렉토리의 경로를 기반으로 데이터베이스 경로 설정
    db_path = os.path.join(os.path.dirname(__file__), '..', 'DB', 'DataBase.db')

    # 데이터베이스 연결
    conn = sqlite3.connect(db_path)
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
            print("신호 1 전송")

    conn.close()

# 일정 주기마다 확인 (1분마다)
while True:
    check_and_send_signal()
    time.sleep(60)  # 1분 대기
