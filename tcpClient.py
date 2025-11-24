import socket
import time

HOST = "127.0.0.1"
PORT = 5050

DEVICE = "Sensor01"
TYPE = "temperature"

def start():
    # connect to hub
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
        print(f"{DEVICE} connected to hub")
        # send registration
        reg = f"DEVICE {DEVICE} TYPE {TYPE}"
        sock.sendall(reg.encode())

        # wait for commands
        while True:
            data = sock.recv(1024)
            if not data:
                break

            cmd = data.decode().strip()
            print(f"{DEVICE} received: {cmd}")

            # send ACK
            time.sleep(1)
            sock.sendall(b"ACK Command Executed")

    except ConnectionRefusedError:
        print("Hub not running")
    finally:
        sock.close()

if __name__ == "__main__":
    start()
