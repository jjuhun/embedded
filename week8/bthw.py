import threading
import serial
import RPi.GPIO as GPIO
import time

# 시리얼 포트 초기화
bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)
gData = ""

# GPIO 핀 설정
PWMA = 18
AIN1 = 22
AIN2 = 27
PWMB = 23
BIN1 = 25
BIN2 = 24

# GPIO 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

# 각 모터에 대한 PWM 인스턴스 생성
L_Motor = GPIO.PWM(PWMA, 500)
R_Motor = GPIO.PWM(PWMB, 500)
L_Motor.start(0)
R_Motor.start(0)

# 모터 제어 함수 정의
def go():
    print("Go forward")
    GPIO.output(AIN1, 0)
    GPIO.output(AIN2, 1)
    GPIO.output(BIN1, 0)
    GPIO.output(BIN2, 1)
    L_Motor.ChangeDutyCycle(50)
    R_Motor.ChangeDutyCycle(50)

def back():
    print("Go backward")
    GPIO.output(AIN1, 1)
    GPIO.output(AIN2, 0)
    GPIO.output(BIN1, 1)
    GPIO.output(BIN2, 0)
    L_Motor.ChangeDutyCycle(50)
    R_Motor.ChangeDutyCycle(50)

def left():
    print("Turn left")
    GPIO.output(AIN1, 1)
    GPIO.output(AIN2, 0)
    GPIO.output(BIN1, 0)
    GPIO.output(BIN2, 1)
    L_Motor.ChangeDutyCycle(50)
    R_Motor.ChangeDutyCycle(30)

def right():
    print("Turn right")
    GPIO.output(AIN1, 0)
    GPIO.output(AIN2, 1)
    GPIO.output(BIN1, 1)
    GPIO.output(BIN2, 0)
    L_Motor.ChangeDutyCycle(30)
    R_Motor.ChangeDutyCycle(50)

def stop():
    print("Stop")
    L_Motor.ChangeDutyCycle(0)
    R_Motor.ChangeDutyCycle(0)

# 시리얼 데이터 수신 스레드
def serial_thread():
    global gData
    while True:
        data = bleSerial.readline()
        data = data.decode().strip()
        gData = data

# 명령에 따라 함수를 호출하는 메인 루프
def main():
    global gData
    try:
        while True:
            # gData 값을 확인하고 각 버튼에 맞는 함수 호출
            if gData == "B4":  # go
                go()
            elif gData == "B3":  # back
                back()
            elif gData == "B5":  # left
                left()
            elif gData == "B1":  # right
                right()
            elif gData == "B2":  # stop
                stop()
                
            gData = ""  # 명령을 수행한 후 gData 초기화
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    # 시리얼 데이터 수신 스레드 시작
    task1 = threading.Thread(target=serial_thread)
    task1.start()
    
    # 메인 함수 실행
    main()
    
    # 종료 시 클린업
   
