#!/usr/bin/python3

import socket
import argparse

HOST = "127.0.0.1"
PORT = 9091


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--protocol", choices=["TCP", "UDP"], required=True)
    parser.add_argument("-b", "--buffer-size", type=int, default=1024)
    parser.add_argument("-m", "--mode", choices=["STREAM", "ACK"], required=True)

    args = parser.parse_args()

    if args.protocol == "UDP":
        udp_server(args)
    else:
        tcp_server(args)


def tcp_server(args):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f"TCP server listening at address: {HOST}:{PORT}")

        while True:
            try:
                (conn, address) = s.accept()
            except KeyboardInterrupt:
                break

            all_data = b''
            messages = 0

            print(f"Accepted a connection request from {address[0]}:{address[1]}")

            while data := conn.recv(args.buffer_size):
                all_data += data
                messages += 1

                if args.mode == "ACK":
                    conn.sendall(b"ACK")

            print(f"Done with request from {address[0]}:{address[1]}")
            print(f"Received {messages} messages and {len(all_data)} bytes")
            if len(all_data) <= 50:
                print(all_data.decode())


def udp_server(args):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))

        print(f"UDP server listening at address: {HOST}:{PORT}")

        all_data = b''
        messages = 0

        while True:
            try:
                (data, address) = s.recvfrom(args.buffer_size)
            except KeyboardInterrupt:
                break

            all_data += data
            messages += 1

            if args.mode == "ACK":
                s.sendto(b"ACK", address)

        print(f"Done with request from {address[0]}:{address[1]}")
        print(f"Received {messages} messages and {len(all_data)} bytes")
        if len(all_data) <= 50:
            print(all_data.decode())


if __name__ == '__main__':
    main()
