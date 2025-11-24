import socket
import logging

HOST = "127.0.0.1"
PORT = 6060
CYCLE = 10

logging.basicConfig(
    filename="logs/sensor_data_log.txt",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

state = {}

def parse(msg):
    try:
        p = msg.split(",")
        seq = int(p[4].replace("SEQ:", ""))
        return p[0], p[1], p[2], p[3], seq
    except:
        return None

def start():
    srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    srv.bind((HOST, PORT))

    print(f"UDP Server running on {HOST}:{PORT}")

    while True:
        data, addr = srv.recvfrom(4096)
        msg = data.decode().strip()

        parsed = parse(msg)
        if not parsed:
            continue

        dev, ts, stype, val, seq = parsed
        logging.info(f"{dev} {stype} {val} SEQ={seq}")

        if dev not in state:
            state[dev] = set()
        state[dev].add(seq)

        if len(state[dev]) >= CYCLE:
            missing = [i for i in range(1, CYCLE + 1) if i not in state[dev]]
            got = CYCLE - len(missing)
            resp = f"STATUS RECEIVED {got}/{CYCLE} PACKETS"
            srv.sendto(resp.encode(), addr)
            state[dev].clear()

if __name__ == "__main__":
    start()
