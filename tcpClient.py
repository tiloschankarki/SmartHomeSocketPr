import socket
import time

HOST = "127.0.0.1"
PORT = 5050

DEVICE = "Sensor01"
TYPE = "temperature"

def start():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
        print(f"{DEVICE} connected to hub")

        reg = f"DEVICE {DEVICE} TYPE {TYPE}"
        sock.sendall(reg.encode())

        while True:
            data = sock.recv(1024)
            if not data:
                break

            cmd = data.decode().strip()
            print(f"{DEVICE} received: {cmd}")

            time.sleep(1)
            sock.sendall(b"ACK Command Executed")

    except ConnectionRefusedError:
        print("Hub not running")
    finally:
        sock.close()

if __name__ == "__main__":
    start()
