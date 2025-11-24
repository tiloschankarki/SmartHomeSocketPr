import socket
import threading
import logging

HOST = "127.0.0.1"
PORT = 5050

logging.basicConfig(
    filename="logs/server_log.txt",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

devices = {}
lock = threading.Lock()

def parse_registration(msg):
    parts = msg.strip().split()
    if len(parts) == 4 and parts[0] == "DEVICE" and parts[2] == "TYPE":
        return parts[1], parts[3]
    return None, None

def handle_client(conn, addr):
    ip, port = addr
    logging.info(f"Connected: {ip}:{port}")

    try:
        reg = conn.recv(1024)
        if not reg:
            return

        reg = reg.decode().strip()
        device, dtype = parse_registration(reg)
        if not device:
            return

        with lock:
            devices[device] = {"type": dtype, "addr": addr}

        logging.info(f"Registered {device} ({dtype})")

        commands = ["SET_INTERVAL 3", "ACTIVATE_ALARM"]
        for c in commands:
            conn.sendall(c.encode())
            logging.info(f"Sent to {device}: {c}")

            ack = conn.recv(1024)
            if not ack:
                break
            logging.info(f"ACK from {device}: {ack.decode().strip()}")

    except:
        pass
    finally:
        conn.close()
        logging.info(f"Disconnected: {addr}")

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"TCP Server running on {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()

if __name__ == "__main__":
    start()
