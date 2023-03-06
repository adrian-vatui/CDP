#!/usr/bin/python3

import argparse
import socket
import time

HOST = "127.0.0.1"
PORT = 9091


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--protocol", choices=["TCP", "UDP"], required=True)
    parser.add_argument("-b", "--buffer-size", type=int, default=1024)
    parser.add_argument("-m", "--mode", choices=["STREAM", "ACK"], required=True)
    parser.add_argument("-f", "--file", required=True)

    args = parser.parse_args()

    with open(args.file, "rb") as f:
        data_to_send = f.read()

    print(f"Actual file size: {len(data_to_send)}")

    if args.protocol == "UDP":
        udp_client(args, data_to_send)
    else:
        tcp_client(args, data_to_send)


def tcp_client(args, data_to_send):
    data_sent, messages_sent = (0, 0)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # send data in chunks of `args.buffer_size` length
        for i in range(0, len(data_to_send), args.buffer_size):
            s.sendall(data_to_send[i:i + args.buffer_size])
            data_sent += len(data_to_send[i:i+args.buffer_size])
            messages_sent += 1

            if args.mode == "ACK":
                # get ACK message from server
                ack = s.recv(3)

                if ack != b'ACK':
                    raise Exception(f"Unexpected ACK message! Got {ack}")
    print(f"Sent {messages_sent} messages and {data_sent} bytes")


def udp_client(args, data_to_send):
    data_sent, messages_sent = (0, 0)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # send data in chunks of `args.buffer_size` length
        for i in range(0, len(data_to_send), args.buffer_size):
            s.sendto(data_to_send[i:i + args.buffer_size], (HOST, PORT))
            data_sent += len(data_to_send[i:i+args.buffer_size])
            messages_sent += 1

            if args.mode == "ACK":
                # get ACK message from server
                ack = s.recv(3)

                if ack != b'ACK':
                    raise Exception(f"Unexpected ACK message! Got {ack}")
    print(f"Sent {messages_sent} messages and {data_sent} bytes")


if __name__ == '__main__':
    t = time.perf_counter()

    main()

    print(f"Sending data took {time.perf_counter() - t:.3f} seconds")
