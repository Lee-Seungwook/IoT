import picamera
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import datetime # 파이썬 내장 모듈
from RPLCD.i2c import CharLCD
GPIO.setmode(GPIO.BCM)

# GPIO.setup(16,GPIO.OUT) #LED R1
# GPIO.setup(20,GPIO.OUT) #LED G1

GPIO.setup(21,GPIO.OUT) #LED B1

#GPIO.setup(13,GPIO.OUT) #LED R2
#GPIO.setup(19,GPIO.OUT) #LED G2

GPIO.setup(26,GPIO.OUT) #LED B2

GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_UP) # BUTTON
GPIO.setup(24,GPIO.IN) #PIR
GPIO.setup(25,GPIO.IN) #BUZZER
GPIO.setup(25,GPIO.OUT) #BUZZER
lcd = CharLCD("PCF8574", 0X27)
camera = picamera.PiCamera()
camera.resolution = (2592, 1944)
intrusion_control = 0
timer = 0
dht_type = 11
bcm_pin = 23
def buzz():
    pitch = 1000
    duration = 0.1
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(25,True)
        time.sleep(delay)
        GPIO.output(25,False)
        time.sleep(delay)
try:
    while True:
        if GPIO.input(24) == True:
            print("SENSOR ON!!")
            while True:
                buzz()
                GPIO.output(21,True)
                time.sleep(0.1)
                GPIO.output(21,False)
                time.sleep(0.1)
                GPIO.output(26,True)
                time.sleep(0.1)
                GPIO.output(26,False)
                time.sleep(0.1)
                
                if intrusion_control == 0:
                    lcd.clear()
                    camera.capture("thief.jpg") #사진 파일명
                    lcd.write_string('LeeSeungwook') #lcd 첫번째 줄
                    lcd.crlf()
                    lcd.write_string('201636030') #lcd 두번째 줄
                    intrusion_control += 1
                    
                if GPIO.input(12) == False: #버튼이 입력되었을 때
                    print("button pressed")
                    lcd.clear() #화면의 글씨 지움
                    GPIO.output(21,False) #LED B1 OFF
                    GPIO.output(26,False) #LED B2 OFF
                    intrusion_control = 0
                    time.sleep(2)
                    break
                time.sleep(0.3)
        else:
            GPIO.output(25,False)
            GPIO.output(21,False)
            # GPIO.output(21,False)
            if timer > 3:
                timer = 0
                lcd.clear()
                now = datetime.datetime.now()
                # nowDate = now.strftime('%Y-%m-%d')
                nowTime = now.strftime('%H:%M:%S')
                humidity, temperature =Adafruit_DHT.read_retry(dht_type, bcm_pin) # DHT에서 값을 가져옴
                humid = round(humidity,1)
                temp = round(temperature,1) #온도
                print(now, nowTime, temp)
                lcd.write_string('TIME ')
                lcd.write_string(nowTime) #현재 시각
                lcd.crlf()
                lcd.write_string('TEMP ')
                lcd.write_string(str(temp)) #현재 온도
                lcd.write_string('C ')
            timer+=0.3
            time.sleep(0.3)
            
except KeyboardInterrupt:
    lcd.clear()
    GPIO.cleanup()
finally:
    GPIO.cleanup()