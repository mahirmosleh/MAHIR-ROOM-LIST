import requests, os, psutil, sys, jwt, pickle, json, binascii, time, urllib3, xZRcdx, base64, datetime, re, socket, threading, ssl, gzip, asyncio, gc
from io import BytesIO
import http
import http.client
from protobuf_decoder.protobuf_decoder import Parser
from M4H1R import *
from datetime import datetime, timedelta
from google.protobuf.timestamp_pb2 import Timestamp
from http.server import HTTPServer, BaseHTTPRequestHandler
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from cfonts import render, say
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
import uuid
import webbrowser
import random
from Pb2 import MajoRLoGinrEq_pb2

# Cryptography modules for real packet encryption
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Global tracking dict for bot details
bot_status = {}
bot_lock = threading.Lock()

# Dynamic Bot Tracking
running_bots = set()
running_bots_lock = threading.Lock()

console = Console()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Master Static Key & IV
Key, Iv = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56]), bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

# ============ SAFE FALLBACK & PACKET ENGINE HELPERS ============
def log_terminal(msg, msg_type="info"):
    """টার্মিনাল আউটপুট প্রিন্ট করার জন্য হেলপার ফাংশন"""
    if msg_type == "info":
        console.print(f"[bold cyan]▪[/bold cyan] [white]{msg}[/white]")
    elif msg_type == "success":
        console.print(f"[bold green]✅[/bold green] [bold white]{msg}[/bold white]")
    elif msg_type == "warning":
        console.print(f"[bold yellow]⚠️[/bold yellow] [yellow]{msg}[/yellow]")
    elif msg_type == "error":
        console.print(f"[bold red]❌[/bold red] [red]{msg}[/red]")
    elif msg_type == "bot":
        console.print(f"[bold magenta]🤖[/bold magenta] [bold cyan]{msg}[/bold cyan]")

def update_bot_info(uid, **kwargs):
    with bot_lock:
        if uid not in bot_status:
            bot_status[uid] = {
                "guest_uid": uid,
                "account_uid": "Loading...",
                "status": "🔄 Initializing...",
                "last_room_id": "None",
                "last_active": "N/A"
            }
        bot_status[uid].update(kwargs)

def ResTarTinG():
    log_terminal("Restarting script process...", "warning")
    try:
        p = psutil.Process(os.getpid())
        for f in p.open_files():
            try: os.close(f.fd)
            except: pass
        for conn in p.net_connections(kind='inet'):
            try:
                if conn.fd != -1: os.close(conn.fd)
            except: pass
    except: pass
    time.sleep(0.5)
    os.execv(sys.executable, ['python'] + sys.argv)

def AuTo_ResTartinG():
    while True:
        time.sleep(3600)  # Restart every 1 hour to prevent memory leaks
        log_terminal("Auto restarting process...", "warning")
        ResTarTinG()

# Real Crypto / Packet Processing Helpers
def EnC_AEs(HeX):
    cipher = AES.new(Key, AES.MODE_CBC, Iv)
    return cipher.encrypt(pad(bytes.fromhex(HeX), AES.block_size)).hex()

def DEc_AEs(HeX):
    cipher = AES.new(Key, AES.MODE_CBC, Iv)
    return unpad(cipher.decrypt(bytes.fromhex(HeX)), AES.block_size).hex()

def EnC_PacKeT(HeX, K, V): 
    return AES.new(K, AES.MODE_CBC, V).encrypt(pad(bytes.fromhex(HeX), 16)).hex()

def DEc_PacKeT(HeX, K, V):
    return unpad(AES.new(K, AES.MODE_CBC, V).decrypt(bytes.fromhex(HeX)), 16).hex()

def EnC_Vr(N):
    if N < 0: return b''
    H = []
    while True:
        BesTo = N & 0x7F
        N >>= 7
        if N: BesTo |= 0x80
        H.append(BesTo)
        if not N: break
    return bytes(H)

def CrEaTe_VarianT(field_number, value):
    field_header = (field_number << 3) | 0
    return EnC_Vr(field_header) + EnC_Vr(value)

def CrEaTe_LenGTh(field_number, value):
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return EnC_Vr(field_header) + EnC_Vr(len(encoded_value)) + encoded_value

def CrEaTe_ProTo(fields):
    packet = bytearray()    
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = CrEaTe_ProTo(value)
            packet.extend(CrEaTe_LenGTh(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(CrEaTe_VarianT(field, value))           
        elif isinstance(value, (str, bytes)):
            packet.extend(CrEaTe_LenGTh(field, value))           
    return packet

def DecodE_HeX(H):
    R = hex(H) 
    F = str(R)[2:]
    return "0" + F if len(F) == 1 else F

def Fix_PackEt(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {'wire_type': result.wire_type}
        if result.wire_type in ["varint", "string", "bytes"]:
            field_data['data'] = result.data
        elif result.wire_type == 'length_delimited':
            field_data["data"] = Fix_PackEt(result.data.results)
        result_dict[result.field] = field_data
    return result_dict

def DeCode_PackEt(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_dict = Fix_PackEt(parsed_results)
        return json.dumps(parsed_results_dict)
    except Exception:
        return None

def xBunnEr():
    avatar_list = [
        '902000016', '902000031', '902000011', '902000065',
        '902000204', '902000192', '902000191', '902000179',
        '902000133', '902045001', '902038023', '902048004',
        '902039014', '902000063', '902000306', '902047009'
    ]
    return int(random.choice(avatar_list))

def GeneRaTePk(Pk, N, K, V):
    PkEnc = EnC_PacKeT(Pk, K, V)
    _ = DecodE_HeX(int(len(PkEnc) // 2))
    if len(_) == 2: HeadEr = N + "000000"
    elif len(_) == 3: HeadEr = N + "00000"
    elif len(_) == 4: HeadEr = N + "0000"
    elif len(_) == 5: HeadEr = N + "000"
    else: HeadEr = N + "00"
    return bytes.fromhex(HeadEr + _ + PkEnc)

def Room(room_name, K, V):
    fields = {
        1: 2,
        2: {
            1: 1, 2: 15, 3: 3, 4: room_name,
            6: 8, 7: 30, 8: 1, 9: 1, 11: 1, 12: 2,
            14: 36981056,
            15: [
                {1: "IDC1", 2: 3000, 3: "BD"},
                {1: "IDC2", 2: 3000, 3: "BD"}
            ]
        }
    }
    return GeneRaTePk(CrEaTe_ProTo(fields).hex(), '0e0b', K, V)

def Ua():
    return "Dalvik/2.1.0 (Linux; U; Android 13; SM-S901B Build/TP1A.220624.014)"

def GeT_Time(exp):
    if not exp: return 0, 0, 0
    now = int(time.time())
    diff = exp - now
    if diff <= 0: return 0, 0, 0
    h, rem = divmod(diff, 3600)
    m, s = divmod(rem, 60)
    return h, m, s

# ============ PACKET / BOT LOGIC ============
async def Mahir_OpeN_RoOm_ChaT(room_id: int, chat_code: str, key: bytes, iv: bytes):
    try:
        fields = {
            1: 3,
            2: {
                1: int(room_id),
                2: 3,
                3: "en",
                4: str(chat_code)
            }
        }
        proto_bytes = CrEaTe_ProTo(fields)
        return GeneRaTePk(proto_bytes.hex(), '1215', key, iv)
    except Exception as e:
        log_terminal(f"Mahir_OpeN_RoOm_ChaT error: {e}", "error")
        return None

async def Mahir_SEnd_RoOm_MsG(room_id: int, message: str, bot_uid: int, key: bytes, iv: bytes):
    try:
        timestamp = int(datetime.now().timestamp())
        avatar = xBunnEr()
        fields = {
            1: 1,
            2: {
                1: int(bot_uid),
                2: int(room_id),
                3: 3,
                4: message,
                5: timestamp,
                7: 6,
                9: {
                    1: f"[C][FF0000]{message[:15]}",
                    2: avatar,
                    3: 2,
                    4: 330,
                    5: 800000304,
                    6: 66,
                    7: 66,
                    8: "MAHIR",
                    9: 66,
                    10: 1,
                    11: 1,
                    13: {1: 68, 2: 67},
                    14: {
                        1: 1158053040,
                        2: 8,
                        3: b"\x10\x15\x08\x0A\x0B\x15\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
                    }
                },
                10: "en",
                13: {3: 1},
                14: {}
            }
        }
        proto_bytes = CrEaTe_ProTo(fields)
        return GeneRaTePk(proto_bytes.hex(), '1215', key, iv)
    except Exception as e:
        log_terminal(f"Room message error: {e}", "error")
        return None

def G_AccEss(U, P):
    UrL = "https://100067.connect.garena.com/oauth/guest/token/grant"
    HE = {
        "Host": "100067.connect.garena.com",
        "User-Agent": Ua(),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close",
    }
    dT = {
        "uid": f"{U}",
        "password": f"{P}",
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067",
    }
    try:
        R = requests.post(UrL, headers=HE, data=dT, timeout=10)
        if R.status_code == 200: 
            json_data = R.json()
            if 'access_token' in json_data and 'open_id' in json_data:
                return json_data['access_token'], json_data['open_id']
            else:
                log_terminal(f"Missing token in response for {U}", "warning")
                return None, None
        else: 
            log_terminal(f"Token request failed for {U}: {R.status_code}", "error")
            return None, None
    except Exception as e: 
        log_terminal(f"Error in G_AccEss: {e}", "error")
        return None, None

def MajorLoGin(PyL):
    context = ssl._create_unverified_context()
    max_retries = 3
    for attempt in range(max_retries):
        try:
            conn = http.client.HTTPSConnection("loginbp.ggpolarbear.com", context=context, timeout=15)    
            headers = {
                'X-Unity-Version': '2018.4.11f1',
                'ReleaseVersion': 'OB54',
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-GA': 'v1 1',
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 13; SM-S901B Build/TP1A.220624.014)',
                'Host': 'loginbp.ggpolarbear.com',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip'}

            conn.request("POST", "/MajorLogin", body=PyL, headers=headers)
            response = conn.getresponse()
            
            if response.status == 503:
                log_terminal(f"Server Busy (503). Retrying in 10s... (Attempt {attempt+1})", "warning")
                time.sleep(10)
                continue
                
            raw_data = response.read()
            if response.getheader('Content-Encoding') == 'gzip':
                with gzip.GzipFile(fileobj=BytesIO(raw_data)) as f:
                    raw_data = f.read()                
            
            return raw_data.hex() if response.status in [200, 201] else None
        except Exception as e:
            log_terminal(f"MajorLoGin Error: {e}", "error")
            time.sleep(5)
        finally:
            try: conn.close()
            except: pass
    return None

Thread(target=AuTo_ResTartinG, daemon=True).start()

class FF_CLient():
    def __init__(self, U, P):  
        self.U = str(U)
        self.P = P
        update_bot_info(self.U, status="🔄 Initializing...")
        self.empty_count = 0  
        self.reader = None 
        self.writer = None          
        try:
            self.Get_FiNal_ToKen_0115(U, P)
        except Exception as e:
            log_terminal(f"Error initializing client for {U}: {e}", "error")
            update_bot_info(self.U, status="❌ Failed")

    async def STarT(self, JwT_ToKen, AutH_ToKen, ip, port, ip2, port2, key, iv, bot_uid):
        update_bot_info(self.U, status="✅ Connected & Online")
        R = asyncio.Event()
        task1 = asyncio.create_task(self.ChaT(self.JwT_ToKen, self.AutH_ToKen, ip, port, key, iv, bot_uid, R))  
        await R.wait()
        await asyncio.sleep(0.5)
        task2 = asyncio.create_task(self.OnLinE(self.JwT_ToKen, self.AutH_ToKen, ip2, port2, key, iv, bot_uid))
        await asyncio.gather(task1, task2)

    async def sF(self):
        if self.writer:
            try: 
                self.writer.close() 
                await asyncio.sleep(0.1) 
                await self.writer.wait_closed()
            except Exception: 
                pass
        self.reader = None 
        self.writer = None
        gc.collect()

    def dec_to_hex(self, n):
        h = hex(n)[2:]
        return h if len(h) % 2 == 0 else '0' + h

    async def send_store_shortcut(self, target_id):
        try:
            map1_json = '{"WorkshopCode":"#FREEFIREEFEA38678BAE600F301D25D0D39DD6E64471","type":"UGCMapShare"}'
            map_json = '{"WorkshopCode":"#FREEFIREF63E5AB9D1C9BECFEF06BBF1AD75D3E1K200","type":"UGCMapShare"}'

            for raw_json in [map1_json, map_json]:
                fields = {
                    1: 1, 
                    2: {
                        1: int(self.bot_uid),
                        2: int(target_id),
                        3: 3, 
                        5: int(time.time()),
                        7: 1,
                        8: raw_json, 
                        9: { 
                            1: "[B][C][00FFFF]ᎷAH!Ꮢ ᏰOᎿ SYSTEM", 
                            2: xBunnEr(), 
                            4: 330,
                            5: 801046518,
                            8: "ᎷAH!Ꮢ TEAM",
                            10: 1,
                            14: {
                                1: 1158053040,
                                2: 8,
                                3: b"\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"
                            }
                        },
                        10: "en",
                        13: {2: 2, 3: 1}
                    }
                }

                packet = GeneRaTePk(CrEaTe_ProTo(fields).hex(), '1215', self.key, self.iv)

                if self.writer:
                    self.writer.write(packet)
                    await self.writer.drain()
                    await asyncio.sleep(0.5) 
            
            log_terminal(f"STORE & MAP SHORTCUTS SENT TO: {target_id}", "success")
            return True

        except Exception as e:
            log_terminal(f"Shortcut Error: {e}", "error")
            return False

    async def Auto_Room_Welcome(self, room_id, chat_code, user_name="Player"):
        try:
            curr_time = datetime.now().strftime("%I:%M:%S %p")
            update_bot_info(self.U, last_room_id=str(room_id), last_active=curr_time)

            if self.writer:
                open_pkt = await Mahir_OpeN_RoOm_ChaT(room_id, chat_code, self.key, self.iv)
                if open_pkt:
                    self.writer.write(open_pkt)
                    await self.writer.drain()
                    await asyncio.sleep(0.5)

                welcome_msg = (
                    f"[C][FFD700]❖━━━━━━━━━━━━━━━━━━━━❖\n"
                    f"[C][FFFFFF]Hᴇʟʟᴏ [FF0000]{user_name}\n"
                    f"[C][00FF7F]Wᴇʟᴄᴏᴍᴇ ᴛᴏ Oᴜʀ Rᴏᴏᴍ! ✨\n"
                    f"[C][FFD700]❖━━━━━━━━━━━━━━━━━━━━❖\n"
                    f"[C][B][00FFFF]🔥 MAHIR AUTOMATION BOT 🔥\n"
                    f"[C][FFD700]─────────────────────\n"
                    f"[C][FFFF00] Type [00FF00]/store [FFFF00]to view items\n"
                    f"[C][FFFF00] Type [00FF00]/app [FFFF00]for Android App\n"
                    f"[C][FFD700]─────────────────────\n"
                    f"[C][00BFFF]📢 Telegram : [FFFFFF]@THEMAHIRWORLD\n"
                    f"[C][FF69B4]🎬 TikTok   : [FFFFFF]@MAHIR__222\n"
                    f"[C][00FF00]🛠️ Follow My Craftland Id : \n [FFFF00]1120🙄167🙄200\n"
                    f"[C][FFD700]❖━━━━━━━━━━━━━━━━━━━━❖"
                )
                
                msg_pkt = await Mahir_SEnd_RoOm_MsG(room_id, welcome_msg, self.bot_uid, self.key, self.iv)
                if msg_pkt:
                    self.writer.write(msg_pkt)
                    await self.writer.drain()
                
                await asyncio.sleep(0.5)
                await self.send_store_shortcut(room_id)
                
                log_terminal(f"AUTO WELCOME & STORE BOX SENT TO ROOM: {room_id}", "success")

        except Exception as e:
            log_terminal(f"Auto Welcome Error: {e}", "error")

    async def OnLinE(self, Token, tok, host2, port2, key, iv, bot_uid):
        retry_count = 0
        max_retries = 5

        while retry_count < max_retries:  
            try: 
                if retry_count == 0:
                    log_terminal(f"Connecting to game server...", "info")
                
                self.reader2, self.writer2 = await asyncio.wait_for(
                    asyncio.open_connection(host2, int(port2)),
                    timeout=10
                )
                log_terminal(f"Game connected successfully", "success")

                await asyncio.sleep(0.5)

                self.writer2.write(bytes.fromhex(tok)) 
                await self.writer2.drain()
                await asyncio.sleep(0.3)

                room_packet = Room('[C][B][FF0000]MAHIR', key, iv)
                self.writer2.write(room_packet) 
                await self.writer2.drain()
                log_terminal("ROOM NAME CHANGE => DONE", "success")

                await asyncio.sleep(0.4)   

                while True:  
                    try:  
                        self.DaTa = await asyncio.wait_for(
                            self.reader2.read(9999),
                            timeout=30
                        )
                        if not self.DaTa: 
                            break
                        
                        data_hex = self.DaTa.hex()
                        if data_hex.startswith("0e00"): 
                            decoded_str = DeCode_PackEt(data_hex[10:])
                            if decoded_str:
                                try:
                                    packet_json = json.loads(decoded_str)
                                    f5 = packet_json.get('5', {}).get('data', {})
                                    r_id = f5.get('1', {}).get('data')
                                    c_code = f5.get('36', {}).get('data') or f5.get('10', {}).get('data')
                                    inviter_name = f5.get('9', {}).get('data', {}).get('1', {}).get('data', 'Player')

                                    if r_id and c_code:
                                        asyncio.create_task(self.Auto_Room_Welcome(r_id, c_code, user_name=inviter_name))
                                except Exception:
                                    pass

                    except asyncio.TimeoutError:
                        try:
                            self.writer2.write(b'\x00')
                            await self.writer2.drain()
                        except Exception:
                            break
                    except (ConnectionResetError, ConnectionAbortedError, asyncio.IncompleteReadError, BrokenPipeError, OSError): 
                        break 
                    except Exception:
                        break

            except Exception as e: 
                log_terminal(f"Connection attempt {retry_count+1} failed: {e}", "warning")
                retry_count += 1
                await asyncio.sleep(1)

        log_terminal("Max retries reached for OnLinE, restarting...", "error")
        ResTarTinG()

    async def ChaT(self, Token, tok, host, port, key, iv, bot_uid, R):
        retry_count = 0
        max_retries = 5

        while retry_count < max_retries:  
            try: 
                log_terminal("Connecting to chat server...", "info")
                self.reader, self.writer = await asyncio.wait_for(
                    asyncio.open_connection(host, int(port)),
                    timeout=10
                )

                self.writer.write(bytes.fromhex(tok)) 
                await self.writer.drain()  
                await asyncio.sleep(0.4)     
                R.set() 

                while True:  
                    try:  
                        self.DaTa = await asyncio.wait_for(
                            self.reader.read(9999),
                            timeout=30
                        )
                        if not self.DaTa: break
                        
                        data_hex = self.DaTa.hex()
                        if data_hex.startswith("1200"): 
                            decoded = DeCode_PackEt(data_hex[10:])
                            if decoded:
                                packet_json = json.loads(decoded)
                                try:
                                    f5 = packet_json.get('5', {}).get('data', {})
                                    msg_text = f5.get('4', {}).get('data', "").lower()
                                    chat_id = f5.get('2', {}).get('data') 
                                    sender_uid = f5.get('1', {}).get('data')

                                    if str(sender_uid) == str(self.bot_uid): continue

                                    if "/store" in msg_text or "/stor" in msg_text:
                                        log_terminal(f"Store requested by {sender_uid}", "info")
                                        
                                        info = (
                                            "[C][FFD700]❖━━━━━━━━━━━━━━━━━━━━❖\n"
                                            "[C][B][00FFFF]⚡ MAHIR BOT STORE ⚡\n"
                                            "[C][FFD700]─────────────────────\n"
                                            "[C][00FF00]🤖 TCP BOT Price : [FFFF00]500 BDT\n"
                                            "[C][00FF00]🌐 Website       : [FFFF00]mahir🫡.xo🫡.🫡je\n"
                                            "[C][00FF00]👤 Owner Telegram : [FFFF00]@MAHIR0208\n"
                                            "[C][00FF00]🛠️ Craftland Map  : [FFFF00]1120🙄167🙄200\n"
                                            "[C][FFD700]❖━━━━━━━━━━━━━━━━━━━━❖"
                                        )
                                        txt_pkt = await Mahir_SEnd_RoOm_MsG(chat_id, info, self.bot_uid, self.key, self.iv)
                                        if txt_pkt:
                                            self.writer.write(txt_pkt)
                                            await self.writer.drain()
                                        
                                        await asyncio.sleep(0.5)

                                    elif "/app" in msg_text:
                                        log_terminal(f"App link requested by {sender_uid}", "info")
                                        
                                        app_info = (
                                            "[C][FFD700]❖━━━━━━━━━━━━━━━━━━━━❖\n"
                                            "[C][B][00FFFF]📱 MAHIR TCP OFFICIAL APP 📱\n"
                                            "[C][FFD700]─────────────────────\n"
                                            "[C][FFFFFF]Download Link:\n"
                                            "[C][00FF00]https🙂://www🙂.mediafire🙂.com🙂/file🙂/lvykrek🙂51q17hae🙂/MAHIR_TCP🙂.apk\n"
                                            "[C][FFD700]❖━━━━━━━━━━━━━━━━━━━━❖"
                                        )
                                        txt_pkt = await Mahir_SEnd_RoOm_MsG(chat_id, app_info, self.bot_uid, self.key, self.iv)
                                        if txt_pkt:
                                            self.writer.write(txt_pkt)
                                            await self.writer.drain()

                                except Exception: pass

                    except asyncio.TimeoutError:
                        try:
                            self.writer.write(b'\x00')
                            await self.writer.drain()
                        except Exception: break
                    except Exception: break
            except Exception:
                retry_count += 1
                await asyncio.sleep(2)
        log_terminal("Max retries reached for ChaT", "warning")

    def GeT_Key_Iv(self, serialized_data):
        try:
            my_message = xZRcdx.MyMessage()
            my_message.ParseFromString(serialized_data)
            timestamp, key, iv = my_message.field21, my_message.field22, my_message.field23
            timestamp_obj = Timestamp()
            timestamp_obj.FromNanoseconds(timestamp)
            timestamp_seconds = timestamp_obj.seconds
            timestamp_nanos = timestamp_obj.nanos
            combined_timestamp = timestamp_seconds * 1_000_000_000 + timestamp_nanos
            return combined_timestamp, key, iv
        except Exception as e:
            log_terminal(f"Error extracting key/iv: {e}", "error")
            return None, None, None

    def GeT_LoGin_PorTs(self, JwT_ToKen, PayLoad):
        self.UrL = 'https://clientbp.common.ggbluefox.com/GetLoginData'
        self.HeadErs = {
            'Expect': '100-continue',
            'Authorization': f'Bearer {JwT_ToKen}',
            'X-Unity-Version': '2018.4.11f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': 'OB54',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
            'Host': 'clientbp.common.ggbluefox.com',
            'Connection': 'close',
            'Accept-Encoding': 'gzip, deflate, br',
        }       
        try:
            self.Res = requests.post(self.UrL, headers=self.HeadErs, data=PayLoad, verify=False, timeout=15)
            decoded = DeCode_PackEt(self.Res.content.hex())
            if not decoded:
                log_terminal("Failed to decode response", "error")
                return None, None, None, None

            self.BesTo_data = json.loads(decoded)  

            if '32' not in self.BesTo_data or '14' not in self.BesTo_data:
                log_terminal("Missing port data in response", "warning")
                return None, None, None, None

            address, address2 = self.BesTo_data['32']['data'], self.BesTo_data['14']['data']

            try:
                ip, port = address.rsplit(":", 1)
                ip2, port2 = address2.rsplit(":", 1)

                port = int(port)
                port2 = int(port2)

            except Exception as e:
                log_terminal(f"Port parsing error: {e}", "error")
                return None, None, None, None

            return ip, port, ip2, port2
        except Exception as e:
            log_terminal(f"Error getting ports: {e}", "error")
        return None, None, None, None

    def ToKen_GeneRaTe(self, U, P):
        try:
            if not U or not P:
                log_terminal("Missing UID or Password", "warning")
                return None

            self.A, self.O = G_AccEss(U, P)
            if not self.A or not self.O:
                log_terminal(f"Failed to get access token for UID {U}", "error")
                return None

            major_login = MajoRLoGinrEq_pb2.MajorLogin()
            major_login.event_time = str(datetime.now())[:-7]
            major_login.game_name = "free fire"
            major_login.platform_id = 2
            major_login.platform_sdk_id = 2
            major_login.device_type = "Handheld"
            major_login.system_hardware = "qcom"
            major_login.system_software = "Android OS 13 / API-33 (TP1A.220624.014)"
            
            self.V = '1.129.1'
            major_login.client_version = self.V
            major_login.client_version_code = "2024010012"
            
            major_login.telecom_operator = "Grameenphone"
            major_login.network_operator_a = "46001"
            major_login.network_type = "WIFI"
            major_login.network_type_a = "WIFI"
            major_login.screen_width = 1080
            major_login.screen_height = 2316
            major_login.screen_dpi = "480"
            
            major_login.processor_details = "Qualcomm Technologies, Inc SM8450"
            major_login.memory = 12288
            major_login.gpu_renderer = "Adreno (TM) 730"
            major_login.gpu_version = "OpenGL ES 3.2 V@0548.0"
            major_login.graphics_api = "OpenGLES3"
            
            major_login.unique_device_id = "f" + str(uuid.uuid4())[:15]
            
            major_login.language = "en"
            major_login.open_id = self.O
            major_login.open_id_type = "4"
            major_login.login_open_id_type = 4
            major_login.access_token = self.A
            major_login.login_by = 3
            major_login.origin_platform_type = "4"
            major_login.primary_platform_type = "4"
            
            major_login.memory_available.version = 55
            major_login.memory_available.hidden_value = 81
            major_login.external_storage_total = 256000
            major_login.internal_storage_total = 256000
            major_login.library_path = "/data/app/com.dts.freefireth/base.apk"
            major_login.library_token = "hash|base.apk"
            major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
            
            pb_data = major_login.SerializeToString()
            self.PaYload = bytes.fromhex(EnC_AEs(pb_data.hex()))

            self.ResPonse = MajorLoGin(self.PaYload)
            if not self.ResPonse:
                log_terminal("MajorLogin failed", "error")
                return None

            decoded_res = DeCode_PackEt(self.ResPonse)
            self.BesTo_data = json.loads(decoded_res)
            
            self.bot_uid = self.BesTo_data['1']['data']
            self.JwT_ToKen = self.BesTo_data['8']['data']          
            self.combined_timestamp, self.key, self.iv = self.GeT_Key_Iv(bytes.fromhex(self.ResPonse))

            if not self.key or not self.iv:
                log_terminal("Failed to extract key/iv", "error")
                return None

            ip, port, ip2, port2 = self.GeT_LoGin_PorTs(self.JwT_ToKen, self.PaYload)

            if not ip or not port:
                log_terminal("Failed to get login ports", "error")
                return None

            return self.JwT_ToKen, self.key, self.iv, self.combined_timestamp, ip, port, ip2, port2, self.bot_uid

        except Exception as e:
            log_terminal(f"Error in Token Generate: {e}", "error")
            return None

    def Get_FiNal_ToKen_0115(self, U, P):
        result = self.ToKen_GeneRaTe(U, P)
        if not result:
            log_terminal(f"Token generation failed for {U}", "error")
            update_bot_info(self.U, status="❌ Token Failed")
            return None

        token, key, iv, Timestamp, ip, port, ip2, port2, bot_uid = result
        self.JwT_ToKen = token        

        try:
            self.AfTer_DeC_JwT = jwt.decode(token, options={"verify_signature": False})
            self.AccounT_Uid = self.AfTer_DeC_JwT.get('account_id')
            self.Nm = self.AfTer_DeC_JwT.get('nickname')
            self.H, self.M, self.S = GeT_Time(self.AfTer_DeC_JwT.get('exp'))
            self.Vr = self.AfTer_DeC_JwT.get('release_version')
            self.EncoDed_AccounT = hex(self.AccounT_Uid)[2:]
            self.HeX_VaLue = DecodE_HeX(Timestamp)
            self.TimE_HEx = self.HeX_VaLue
            self.JwT_ToKen_ = token.encode().hex()

            log_terminal(f"Account UID: [bold yellow]{self.AccounT_Uid}[/bold yellow] Loaded Successfully", "bot")
            update_bot_info(self.U, account_uid=str(self.AccounT_Uid))

        except Exception as e:
            log_terminal(f"Error In Token decode: {e}", "error")
            return None

        try:
            self.Header = hex(len(EnC_PacKeT(self.JwT_ToKen_, key, iv)) // 2)[2:]
            length = len(self.EncoDed_AccounT)
            self.__ = '00000000'
            if length == 9: self.__ = '0000000'
            elif length == 8: self.__ = '00000000'
            elif length == 10: self.__ = '000000'
            elif length == 7: self.__ = '000000000'

            self.Header = f'0115{self.__}{self.EncoDed_AccounT}{self.TimE_HEx}00000{self.Header}'
            self.FiNal_ToKen_0115 = self.Header + EnC_PacKeT(self.JwT_ToKen_, key, iv)

        except Exception as e:
            log_terminal(f"Error In Final Token: {e}", "error")            
            return None

        self.AutH_ToKen = self.FiNal_ToKen_0115

        try:
            asyncio.run(self.STarT(self.JwT_ToKen, self.AutH_ToKen, ip, port, ip2, port2, key, iv, bot_uid))
        except Exception as e:
            log_terminal(f"Error starting client: {e}", "error")

        return self.AutH_ToKen, key, iv

def load_accounts(file_path="accs.json"):
    try:
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("{}")
            return {}
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            accounts = {str(k): str(v) for k, v in data.items() if str(k).isdigit()}
            return accounts
    except Exception as e:
        log_terminal(f"Error loading accounts: {e}", "error")
        return {}

# ============ DYNAMIC ACCOUNT LOADER & RUNNER ============
def dynamic_account_loader():
    """স্বয়ংক্রিয়ভাবে accs.json ফাইল স্ক্যান করে নতুন অ্যাকাউন্ট রান করাবে"""
    while True:
        try:
            accounts = load_accounts()
            with running_bots_lock:
                for uid, pwd in accounts.items():
                    if uid not in running_bots:
                        running_bots.add(uid)
                        log_terminal(f"✨ New Account Detected! Launching Guest UID: {uid}", "success")
                        t = threading.Thread(target=FF_CLient, args=(uid, pwd), daemon=True)
                        t.start()
        except Exception as e:
            log_terminal(f"Account Loader Error: {e}", "error")
        time.sleep(3)  # প্রতি ৩ সেকেন্ড পর নতুন অ্যাকাউন্ট স্ক্যান করবে

# ============ HTTP WEB SERVER ============
class BotHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MAHIR · TCP Automation Command Center</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #00f0ff;
            --secondary: #7000ff;
            --accent: #ff0055;
            --bg-dark: #05030a;
            --card-bg: rgba(18, 12, 32, 0.65);
            --border-glow: rgba(112, 0, 255, 0.4);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Rajdhani', sans-serif; }

        body {
            min-height: 100vh;
            background: #030108;
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(112, 0, 255, 0.25), transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(0, 240, 255, 0.15), transparent 40%),
                radial-gradient(circle at 50% 50%, rgba(255, 0, 85, 0.1), transparent 50%);
            background-attachment: fixed;
            color: #fff;
            padding: 25px 15px;
            display: flex;
            justify-content: center;
        }

        .container {
            width: 100%;
            max-width: 1050px;
            background: var(--card-bg);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border-radius: 28px;
            padding: 35px;
            border: 1px solid var(--border-glow);
            box-shadow: 0 0 50px rgba(112, 0, 255, 0.2), inset 0 0 15px rgba(255, 255, 255, 0.05);
            animation: containerGlow 4s infinite alternate;
        }

        @keyframes containerGlow {
            0% { box-shadow: 0 0 40px rgba(112, 0, 255, 0.25); border-color: rgba(112, 0, 255, 0.4); }
            100% { box-shadow: 0 0 60px rgba(0, 240, 255, 0.3); border-color: rgba(0, 240, 255, 0.5); }
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 25px;
            margin-bottom: 30px;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .logo-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, var(--accent), var(--secondary));
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.6rem;
            box-shadow: 0 0 20px rgba(255, 0, 85, 0.6);
            animation: pulseIcon 2s infinite;
        }

        @keyframes pulseIcon {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        .logo h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.2rem;
            font-weight: 900;
            letter-spacing: 3px;
            background: linear-gradient(135deg, #ffffff, var(--primary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
        }

        .logo span {
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.85rem;
            letter-spacing: 2px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .status-badge {
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid #00ff88;
            padding: 10px 22px;
            border-radius: 50px;
            color: #00ff88;
            font-weight: 700;
            font-size: 0.9rem;
            letter-spacing: 1px;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.2);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .pulse-icon {
            width: 9px;
            height: 9px;
            background-color: #00ff88;
            border-radius: 50%;
            box-shadow: 0 0 10px #00ff88;
            animation: pulseDot 1.5s infinite;
        }

        @keyframes pulseDot {
            0% { transform: scale(0.9); opacity: 0.7; }
            50% { transform: scale(1.3); opacity: 1; }
            100% { transform: scale(0.9); opacity: 0.7; }
        }

        .refresh-btn {
            background: linear-gradient(135deg, rgba(0, 240, 255, 0.15), rgba(112, 0, 255, 0.15));
            border: 1px solid var(--primary);
            color: var(--primary);
            padding: 10px 24px;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9rem;
            font-weight: 700;
            letter-spacing: 1px;
        }

        .refresh-btn:hover {
            background: var(--primary);
            color: #000;
            box-shadow: 0 0 25px var(--primary);
            transform: translateY(-2px);
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 18px;
            margin-bottom: 35px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 20px;
            padding: 22px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 3px;
            background: linear-gradient(90deg, transparent, var(--primary), transparent);
            opacity: 0;
            transition: opacity 0.3s;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            border-color: rgba(0, 240, 255, 0.3);
            background: rgba(255, 255, 255, 0.04);
        }

        .stat-card:hover::before { opacity: 1; }

        .stat-card .number {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.4rem;
            font-weight: 900;
            color: #fff;
            margin-bottom: 5px;
        }

        .stat-card .label {
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
        }

        .table-wrap {
            overflow-x: auto;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 35px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
            background: rgba(5, 3, 10, 0.4);
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th {
            background: rgba(112, 0, 255, 0.2);
            color: var(--primary);
            padding: 20px 18px;
            text-align: left;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            font-size: 0.85rem;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            border-bottom: 2px solid rgba(112, 0, 255, 0.3);
        }

        td {
            padding: 18px;
            color: #ddd;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            font-size: 0.95rem;
            vertical-align: middle;
        }

        tr { transition: background 0.2s ease; }
        tr:hover td { background: rgba(0, 240, 255, 0.03); }

        .uid-badge {
            background: linear-gradient(135deg, rgba(0, 240, 255, 0.12), rgba(112, 0, 255, 0.12));
            border: 1px solid rgba(0, 240, 255, 0.4);
            color: var(--primary);
            padding: 8px 16px;
            border-radius: 12px;
            font-family: 'Orbitron', monospace;
            font-weight: 700;
            font-size: 0.95rem;
            letter-spacing: 1px;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.15);
        }

        .room-badge {
            background: linear-gradient(135deg, rgba(255, 0, 85, 0.15), rgba(112, 0, 255, 0.15));
            border: 1px solid rgba(255, 0, 85, 0.5);
            color: #ff3377;
            padding: 8px 16px;
            border-radius: 12px;
            font-family: 'Orbitron', monospace;
            font-weight: 700;
            font-size: 0.95rem;
            letter-spacing: 1.2px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 0 15px rgba(255, 0, 85, 0.2);
            animation: pulseRoom 2s infinite;
        }

        @keyframes pulseRoom {
            0% { box-shadow: 0 0 10px rgba(255, 0, 85, 0.2); }
            50% { box-shadow: 0 0 20px rgba(255, 0, 85, 0.5); }
            100% { box-shadow: 0 0 10px rgba(255, 0, 85, 0.2); }
        }

        .time-badge {
            color: #aaa;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: 50px;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.8px;
            text-transform: uppercase;
        }

        .badge-online { background: rgba(0, 255, 136, 0.12); color: #00ff88; border: 1px solid rgba(0, 255, 136, 0.3); }
        .badge-offline { background: rgba(255, 0, 85, 0.12); color: #ff0055; border: 1px solid rgba(255, 0, 85, 0.3); }
        .badge-connecting { background: rgba(255, 170, 0, 0.12); color: #ffaa00; border: 1px solid rgba(255, 170, 0, 0.3); }

        .admin-panel {
            background: rgba(12, 8, 24, 0.6);
            padding: 30px;
            border-radius: 22px;
            border: 1px dashed var(--border-glow);
            box-shadow: inset 0 0 20px rgba(112, 0, 255, 0.05);
        }

        .dropdown { position: relative; display: inline-block; margin-top: 15px; }

        .dropdown-btn {
            background: linear-gradient(135deg, var(--secondary), var(--accent));
            color: white;
            border: none;
            padding: 12px 26px;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 700;
            font-size: 0.95rem;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 0 5px 20px rgba(112, 0, 255, 0.4);
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }

        .dropdown-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(255, 0, 85, 0.6);
        }

        .dropdown-menu {
            display: none;
            position: absolute;
            top: 110%; left: 0;
            background: #0d0818;
            border: 1px solid var(--border-glow);
            border-radius: 14px;
            min-width: 230px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.9);
            z-index: 100;
            overflow: hidden;
        }

        .dropdown-menu.show { display: block; }

        .dropdown-item {
            padding: 14px 20px;
            color: #ddd;
            display: flex;
            align-items: center;
            gap: 12px;
            cursor: pointer;
            transition: background 0.2s ease;
            font-size: 0.9rem;
            font-weight: 600;
        }

        .dropdown-item:hover { background: rgba(112, 0, 255, 0.3); color: var(--primary); }

        .content-box { display: none; margin-top: 20px; }
        .content-box.active { display: block; }

        textarea {
            width: 100%;
            height: 220px;
            background: #05020a;
            color: #00ff88;
            font-family: 'Consolas', monospace;
            font-size: 0.95rem;
            padding: 18px;
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-top: 12px;
            outline: none;
            resize: vertical;
        }

        .upload-area {
            border: 2px dashed rgba(0, 240, 255, 0.3);
            border-radius: 16px;
            padding: 30px;
            text-align: center;
            background: rgba(0, 0, 0, 0.3);
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .upload-area:hover {
            border-color: var(--primary);
            background: rgba(0, 240, 255, 0.05);
        }

        .action-btn {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 10px;
            cursor: pointer;
            margin-top: 15px;
            font-weight: 700;
            font-size: 0.9rem;
            letter-spacing: 1px;
        }

        .footer {
            margin-top: 35px;
            text-align: center;
            color: rgba(255, 255, 255, 0.4);
            font-size: 0.85rem;
            letter-spacing: 1px;
        }

        .empty-msg { text-align: center; padding: 40px; color: #888; font-size: 1.1rem; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <div class="logo-icon"><i class="fas fa-robot"></i></div>
                <div>
                    <h1>MAHIR ROOM LIST</h1>
                    <span>TCP Automation Dashboard</span>
                </div>
            </div>
            <div class="header-actions">
                <span class="status-badge"><span class="pulse-icon"></span> SYSTEM ONLINE</span>
                <button class="refresh-btn" onclick="location.reload()"><i class="fas fa-sync-alt"></i> REFRESH</button>
            </div>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="number" style="color:#00f0ff;" id="totalJsonAccounts">0</div>
                <div class="label"><i class="fas fa-users-cog" style="color:#00f0ff;"></i> Total Accounts</div>
            </div>
            <div class="stat-card">
                <div class="number" id="totalBots">0</div>
                <div class="label"><i class="fas fa-microchip"></i> Active Running</div>
            </div>
            <div class="stat-card">
                <div class="number" style="color:#00ff88;" id="onlineBots">0</div>
                <div class="label"><i class="fas fa-bolt" style="color:#00ff88;"></i> Online</div>
            </div>
            <div class="stat-card">
                <div class="number" style="color:#ffaa00;" id="connectingBots">0</div>
                <div class="label"><i class="fas fa-spinner fa-spin" style="color:#ffaa00;"></i> Connecting</div>
            </div>
            <div class="stat-card">
                <div class="number" style="color:#ff0055;" id="offlineBots">0</div>
                <div class="label"><i class="fas fa-exclamation-triangle" style="color:#ff0055;"></i> Offline</div>
            </div>
        </div>

        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Account UID</th>
                        <th>Active Room ID</th>
                        <th>Status</th>
                        <th>Last Active</th>
                    </tr>
                </thead>
                <tbody id="botTableBody">
                    <tr><td colspan="5" class="empty-msg"><i class="fas fa-spinner fa-spin"></i> Loading Realtime Data...</td></tr>
                </tbody>
            </table>
        </div>

        <!-- Account JSON Manager -->
        <div class="admin-panel">
            <h3 style="color: var(--primary); font-family: 'Orbitron', sans-serif;"><i class="fas fa-sliders-h"></i> Configuration Control (accs.json)</h3>
            
            <div class="dropdown">
                <button class="dropdown-btn" onclick="toggleDropdown()">
                    <i class="fas fa-tools"></i> Manage Accounts <i class="fas fa-chevron-down" style="font-size: 0.8rem; margin-left: 5px;"></i>
                </button>
                <div class="dropdown-menu" id="dropdownMenu">
                    <div class="dropdown-item" onclick="selectOption('upload')">
                        <i class="fas fa-file-upload" style="color:#00ff88;"></i> Upload accs.json
                    </div>
                    <div class="dropdown-item" onclick="selectOption('edit')">
                        <i class="fas fa-edit" style="color:#ffaa00;"></i> Live JSON Editor
                    </div>
                </div>
            </div>

            <div id="uploadBox" class="content-box">
                <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                    <i class="fas fa-cloud-upload-alt" style="font-size: 2.5rem; color: var(--primary); margin-bottom: 10px;"></i>
                    <p id="fileNameDisplay" style="font-weight: 600; color: #ddd;">Click or Drag & Drop accs.json File Here</p>
                    <input type="file" id="fileInput" accept=".json" style="display: none;" onchange="handleFileSelect(event)">
                </div>
                <button class="action-btn" onclick="uploadJsonFile()"><i class="fas fa-upload"></i> Save & Auto Launch</button>
                <span id="uploadStatus" style="margin-left: 10px; font-weight: 600;"></span>
            </div>

            <div id="editBox" class="content-box">
                <textarea id="jsonEditor" spellcheck="false"></textarea>
                <button class="action-btn" onclick="saveJson()"><i class="fas fa-save"></i> Save Configuration</button>
                <span id="saveStatus" style="margin-left: 10px; font-weight: 600;"></span>
            </div>
        </div>

        <div class="footer">
            MAHIR AUTOMATION SYSTEM &bull; ACTIVE ENGINE V1.129.1
        </div>
    </div>

    <script>
        function fetchBots() {
            fetch('/status')
                .then(res => res.json())
                .then(data => {
                    const tbody = document.getElementById('botTableBody');
                    const total = document.getElementById('totalBots');
                    const online = document.getElementById('onlineBots');
                    const connecting = document.getElementById('connectingBots');
                    const offline = document.getElementById('offlineBots');
                    const totalJsonAccs = document.getElementById('totalJsonAccounts');
                    
                    if (data.total_accs !== undefined) {
                        totalJsonAccs.textContent = data.total_accs;
                    }

                    const botData = data.bots || {};
                    let onlineCount = 0, connectingCount = 0, offlineCount = 0;
                    let html = '';
                    const entries = Object.entries(botData);
                    
                    if (entries.length === 0) {
                        html = `<tr><td colspan="5" class="empty-msg"><i class="fas fa-robot"></i> No active bot processes</td></tr>`;
                    } else {
                        entries.forEach(([uid, info], index) => {
                            let statusText, badgeClass;
                            const statusStr = info.status || "Offline";

                            if (statusStr.includes('✅') || statusStr.includes('Connected') || statusStr.includes('Online')) {
                                statusText = 'Online';
                                badgeClass = 'badge-online';
                                onlineCount++;
                            } else if (statusStr.includes('🔄') || statusStr.includes('Connecting') || statusStr.includes('Initializing')) {
                                statusText = 'Connecting';
                                badgeClass = 'badge-connecting';
                                connectingCount++;
                            } else {
                                statusText = 'Offline';
                                badgeClass = 'badge-offline';
                                offlineCount++;
                            }

                            const accountUid = info.account_uid && info.account_uid !== "Loading..." 
                                ? `<div class="uid-badge"><i class="fas fa-id-card"></i> ${info.account_uid}</div>` 
                                : `<span style="color:#666;">Fetching UID...</span>`;

                            const roomId = info.last_room_id && info.last_room_id !== "None"
                                ? `<div class="room-badge"><i class="fas fa-door-open"></i> ${info.last_room_id}</div>`
                                : `<span style="color:#555;">No Active Room</span>`;

                            const lastActive = info.last_active || "N/A";

                            html += `<tr>
                                <td><b>${index + 1}</b></td>
                                <td>${accountUid}</td>
                                <td>${roomId}</td>
                                <td><span class="badge ${badgeClass}">${statusText}</span></td>
                                <td><span class="time-badge"><i class="far fa-clock"></i> ${lastActive}</span></td>
                            </tr>`;
                        });
                    }
                    tbody.innerHTML = html;
                    total.textContent = entries.length;
                    online.textContent = onlineCount;
                    connecting.textContent = connectingCount;
                    offline.textContent = offlineCount;
                })
                .catch(() => {});
        }

        function toggleDropdown() {
            document.getElementById('dropdownMenu').classList.toggle('show');
        }

        window.onclick = function(event) {
            if (!event.target.matches('.dropdown-btn') && !event.target.matches('.dropdown-btn *')) {
                const dropdowns = document.getElementsByClassName("dropdown-menu");
                for (let i = 0; i < dropdowns.length; i++) {
                    dropdowns[i].classList.remove('show');
                }
            }
        }

        function selectOption(option) {
            document.getElementById('dropdownMenu').classList.remove('show');
            document.getElementById('uploadBox').classList.remove('active');
            document.getElementById('editBox').classList.remove('active');

            if (option === 'upload') {
                document.getElementById('uploadBox').classList.add('active');
            } else if (option === 'edit') {
                document.getElementById('editBox').classList.add('active');
                loadJson();
            }
        }

        let selectedFileContent = null;
        function handleFileSelect(event) {
            const file = event.target.files[0];
            if (file) {
                document.getElementById('fileNameDisplay').textContent = "Selected: " + file.name;
                const reader = new FileReader();
                reader.onload = function(e) { selectedFileContent = e.target.result; };
                reader.readAsText(file);
            }
        }

        function uploadJsonFile() {
            const status = document.getElementById('uploadStatus');
            if (!selectedFileContent) return alert("Select a JSON file!");
            try {
                sendSaveRequest(JSON.parse(selectedFileContent), status);
            } catch (e) { alert("Invalid JSON File!"); }
        }

        function loadJson() {
            fetch('/get_accs').then(res => res.json()).then(data => {
                document.getElementById('jsonEditor').value = JSON.stringify(data, null, 4);
            });
        }

        function saveJson() {
            const editor = document.getElementById('jsonEditor');
            const status = document.getElementById('saveStatus');
            try {
                sendSaveRequest(JSON.parse(editor.value), status);
            } catch (e) { alert("Invalid JSON format!"); }
        }

        function sendSaveRequest(data, statusElement) {
            fetch('/save_accs', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            .then(res => {
                if(res.ok) {
                    statusElement.innerHTML = "✅ Saved & Auto Launching Bots!";
                    statusElement.style.color = "#00ff88";
                    setTimeout(() => fetchBots(), 1000);
                }
            });
        }

        fetchBots();
        setInterval(fetchBots, 2000);
    </script>
</body>
</html>'''
            self.wfile.write(html_content.encode('utf-8'))
        
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with bot_lock:
                status_copy = bot_status.copy()
            
            # Get Total JSON Count dynamically
            accs = load_accounts()
            
            response_payload = {
                "total_accs": len(accs),
                "bots": status_copy
            }
            self.wfile.write(json.dumps(response_payload).encode('utf-8'))

        elif self.path == '/get_accs':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            try:
                with open("accs.json", "r", encoding="utf-8") as f:
                    content = f.read()
                self.wfile.write(content.encode('utf-8'))
            except Exception:
                self.wfile.write(b"{}")

    def do_POST(self):
        if self.path == '/save_accs':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                new_data = json.loads(post_data.decode('utf-8'))
                with open("accs.json", "w", encoding="utf-8") as f:
                    json.dump(new_data, f, indent=4)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
                log_terminal("accs.json updated via Web interface. Triggering auto-loader...", "warning")
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))

    def log_message(self, format, *args):
        pass

def run_web_server():
    server = HTTPServer(('0.0.0.0', 8080), BotHandler)
    log_terminal("MAHIR Web Dashboard running at: http://localhost:8080", "success")
    webbrowser.open('http://localhost:8080')
    server.serve_forever()

def StarT_SerVer():
    console.clear()
    print(render('MAHIR', colors=['white', 'red'], align='center'))
    
    # Clean Rich Table Banner for Terminal
    banner_table = Table(title="🔥 Free Fire Bot Automation Console 🔥", style="bold red", show_header=True, header_style="bold magenta")
    banner_table.add_column("System Status", justify="center")
    banner_table.add_column("Dashboard Link", justify="center")
    banner_table.add_row("[bold green]System Active & Running[/bold green]", "[cyan]http://localhost:8080[/cyan]")
    console.print(banner_table)
    console.print("\n")

    # Start Web Server Thread
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    time.sleep(1)

    # Start Dynamic Account Loader Thread
    loader_thread = threading.Thread(target=dynamic_account_loader, daemon=True)
    loader_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log_terminal("Stopping server process gracefully...", "warning")

if __name__ == "__main__":
    StarT_SerVer()
