import socket
import time
from datetime import datetime

HOST = "127.0.0.1"
PORT = 6060

DEVICE = "Sensor01"
TYPE = "temperature"
CYCLE = 10

def get_value(i):
    # generate simple sensor value
    return 24 + 0.2 * i

def start():
    # start UDP client
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    # send Packets
    for i in range(1, CYCLE + 1):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        val = get_value(i)
        msg = f"{DEVICE},{ts},{TYPE},{val:.1f},SEQ:{i}"
        sock.sendto(msg.encode(), (HOST, PORT))
        print(f"{DEVICE} sent SEQ:{i}")
        time.sleep(1)

    # wait for sever summary
    try:
        status, _ = sock.recvfrom(4096)
        print(status.decode().strip())
    except socket.timeout:
        print("No status received")

    sock.close()

if __name__ == "__main__":
    start()
