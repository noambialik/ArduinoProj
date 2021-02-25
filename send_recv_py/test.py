import serial
import logging
from threading import Thread

ser = serial.Serial('COM3', timeout=1000)

def init_log():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter("")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

def get_from_ser():
    s = ser.read_until().decode("utf-8")
    if s != "\r\n" and s != "" and not s.startswith("OK-"):
        return s

# def get_from_ser_loop():
#     logging.info("Welcome!")
#     while True:
#         get_from_ser()  


def send_to_ser(msg_to_send):
    msg = "Noam: {}".format(msg_to_send)
    try:
        msg = bytes(msg, 'utf8')
    except Exception:
        logging.error("cannot convert to bytes. message")
    ser.write(msg)

def run_get_thread():
    t1 = Thread(target=get_from_ser_loop)
    t1.setDaemon(True)
    t1.start()

if __name__ =="__main__":
    init_log()
    t1 = Thread(target=get_from_ser_loop)
    t1.setDaemon(True)
    t1.start()

    while True:
        # msg_to_send = input("Send:")
        # send_to_ser(msg_to_send)
        pass
