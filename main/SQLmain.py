import pymysql
from pymysql import cursors
import serial
import time
from datetime import datetime
import requests
import keyboard

weekdays = ['mon','tue', 'wed', 'thu', 'fri', 'sat', 'sun']
# MySQL 데이터베이스 연결 함수
def connect_to_database():
    return pymysql.connect(
        host = "172.190.90.75",
        user = "pill",
        password = "qwer3249@",
        database = "pill_dispenser",
        charset = "utf8",
        autocommit = True
    )

def get_data(conn):
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute("select user_id, medicine, container, dosing_time, finished, `repeat` from notes_note where user_id=1")
    rows = cursor.fetchall()
    return rows, cursor
    

def check_and_send_signal(conn, curs ,rows):
    print("신호 확인 및 전송 시작")
    while True:     
        if keyboard.is_pressed('q'):
            rows = get_data(conn)
            print(rows)
            print('Get new data')
            
        current_time = datetime.now().strftime('%H:%M')
        current_date = weekdays[datetime.now().weekday()]
        
        #print(f"현재 시간: {current_time}")
        for row in rows:
            user_id, medicine, container, dosing_time, finished, repeat = row.values()
            if ('daily' in repeat) or current_date in repeat:
                if str(dosing_time).rstrip(':00') == str(current_time) and finished == 0:    
                    print(f"사용자: {user_id}, 약 이름: {medicine}, 약 통 번호: {container}, 시간: {dosing_time}")
                    curs.execute(f"UPDATE notes_note set finished=1 where container={container}")
                    row['finished'] = 1
                    ser.write(b'1') #아두이노로 신호 전송
                else:
                    continue
            else:
                print('오늘이 아님', repeat)
                continue
    print("신호 확인 및 전송 완료")

if __name__ == "__main__":
    # MySQL 데이터베이스에 연결
    conn = connect_to_database()
    rows, curs = get_data(conn)
    # 시리얼 포트와 통신 속도 설정
    ser = serial.Serial('/dev/ttyACM0', 9600)  # '/dev/ttyUSB0'는 아두이노가 연결된 포트
    time.sleep(2)  # 시리얼 통신 안정화 시간
    check_and_send_signal(conn, curs, rows)
    # 데이터베이스 연결 종료
    conn.close()
