#!/usr/bin/env python3

import subprocess
import sys
import importlib
import os
import ssl
import json
import time
import random
import asyncio
import threading
import gc
import re
from datetime import datetime
from io import BytesIO
import gzip
import http.client
import uuid
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

import aiohttp
import jwt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from cfonts import render
from M4H1R import *

from protobuf_decoder.protobuf_decoder import Parser

from Pb2 import MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2

console = Console()

# ========== GLOBAL TRACKING ==========
welcome_tracking = {}
running_bots = set()
running_bots_lock = threading.Lock()
bot_status = {}
bot_lock = threading.Lock()

# ========== CONFIG ==========
login_url, ob, version = "https://loginbp.ggpolarbear.com/", "OB54", "1.126.7"
TIMEOUT = aiohttp.ClientTimeout(total=15)

# ---------- HELPERS ----------
def Uaa():
    versions = ['5.0.1B2','5.1.0P1','5.2.0B1']
    models = ['SM-A125F','Redmi 9A','POCO M3']
    android = random.choice(['11','12','13'])
    return f"GarenaMSDK/{random.choice(versions)}({random.choice(models)};Android {android};en-US;USA;)"

Hr = {
    'User-Agent': Uaa(),
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': ob
}

def get_random_color():
    colors = ["[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]", "[FFC0CB]", "[FFD700]"]
    return random.choice(colors)

def xBunnEr():
    avatar_list = [
        '902000016', '902000031', '902000011', '902000065',
        '902000204', '902000192', '902000191', '902000179',
        '902000133', '902045001', '902038023', '902048004',
        '902039014', '902000063', '902000306', '902047009'
    ]
    return int(random.choice(avatar_list))

def update_bot_info(uid, **kwargs):
    with bot_lock:
        if uid not in bot_status:
            bot_status[uid] = {
                "guest_uid": uid,
                "account_uid": "Loading...",
                "status": "🔄 Initializing...",
                "last_room_id": "None",
                "last_active": "N/A",
                "room_active": False
            }
        bot_status[uid].update(kwargs)

# ---------- PROTO DECODER ----------
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

# ---------- ENCRYPTION / DECRYPTION ----------
async def EnC_Vr(N):
    if N<0: return b''
    H = []
    while True:
        RedZed = N & 0x7F
        N >>= 7
        if N: RedZed |= 0x80
        H.append(RedZed)
        if not N: break
    return bytes(H)

async def CrEaTe_VarianT(fn, val):
    return await EnC_Vr((fn<<3)|0) + await EnC_Vr(val)

async def CrEaTe_LenGTh(fn, val):
    ev = val.encode() if isinstance(val,str) else val
    return await EnC_Vr((fn<<3)|2) + await EnC_Vr(len(ev)) + ev

async def CrEaTe_ProTo(fields):
    packet = bytearray()
    for f,v in fields.items():
        if isinstance(v,list):
            for item in v:
                if isinstance(item, dict):
                    nested = await CrEaTe_ProTo(item)
                    packet.extend(await CrEaTe_LenGTh(f, nested))
        elif isinstance(v,dict):
            nested = await CrEaTe_ProTo(v)
            packet.extend(await CrEaTe_LenGTh(f, nested))
        elif isinstance(v,int):
            packet.extend(await CrEaTe_VarianT(f,v))
        elif isinstance(v,(str,bytes)):
            packet.extend(await CrEaTe_LenGTh(f,v))
    return bytes(packet)

async def DecodE_HeX(H):
    F = str(hex(H))[2:]
    return "0"+F if len(F)==1 else F

async def EnC_PacKeT(HeX, K, V):
    cipher = AES.new(K, AES.MODE_CBC, V)
    return cipher.encrypt(pad(bytes.fromhex(HeX),16)).hex()

async def GeneRaTePk(Pk, N, K, V):
    PkEnc = await EnC_PacKeT(Pk, K, V)
    _ = await DecodE_HeX(len(PkEnc)//2)
    HeadEr = N+"000000" if len(_)==2 else N+"00000" if len(_)==3 else N+"0000" if len(_)==4 else N+"000"
    return bytes.fromhex(HeadEr+_+PkEnc)

# ---------- MESSAGE PACKETS ----------
async def MAHIR_OpeN_RoOm_ChaT(room_id: int, chat_code: str, key: bytes, iv: bytes):
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
        proto_bytes = await CrEaTe_ProTo(fields)
        return await GeneRaTePk(proto_bytes.hex(), '1215', key, iv)
    except Exception:
        return None

async def MAHIR_SEnd_RoOm_MsG(room_id: int, message: str, bot_uid: int, key: bytes, iv: bytes):
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
        proto_bytes = await CrEaTe_ProTo(fields)
        return await GeneRaTePk(proto_bytes.hex(), '1215', key, iv)
    except Exception:
        return None

async def Mahir_Room_Site_Change(room_id, bot_id, side, slot, key, iv):
    try:
        fields = {
            1: 20,
            2: {
                1: int(room_id),
                2: int(bot_id),
                3: int(side), 
                4: int(slot), 
                6: 1
            }
        }
        # CrEaTe_ProTo async তাই এখানে await দিতে হবে
        proto_bytes = await CrEaTe_ProTo(fields)
        packet_hex = proto_bytes.hex()
        final_packet = await GeneRaTePk(packet_hex, '0e15', key, iv)
        return final_packet
    except Exception:
        return None

async def Mahir_Room_START(room_id, key, iv):
    try:
        fields = {
            1: 11,
            2: {
                1: int(room_id),
                2: 1
            }
        }
        proto_bytes = await CrEaTe_ProTo(fields)
        packet_hex = proto_bytes.hex()
        final_packet = await GeneRaTePk(packet_hex, '0e15', key, iv)
        return final_packet
    except Exception:
        return None

async def Mahir_Room_ExiT(bot_uid, key, iv):
    try:
        fields = {
            1: 6, 
            2: {
                1: int(bot_uid)
            }
        }
        proto_bytes = await CrEaTe_ProTo(fields)
        packet_hex = proto_bytes.hex()
        return await GeneRaTePk(packet_hex, '0e15', key, iv)
    except Exception:
        return None

# ---------- LOGIN & AUTH ----------
async def GeNeRaTeAccAccess(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {"Host":"100067.connect.garena.com","User-Agent":Uaa(),"Content-Type":"application/x-www-form-urlencoded","Connection":"close"}
    data = {"uid":uid,"password":password,"response_type":"token","client_type":"2","client_secret":"2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3","client_id":"100067"}
    try:
        async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
            async with session.post(url, headers=headers, data=data) as resp:
                if resp.status != 200: return None, None
                data = await resp.json()
                return data.get("open_id"), data.get("access_token")
    except Exception:
        return None, None

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 2
    major_login.client_version = "1.126.7"
    major_login.client_version_code = "2024010012"
    major_login.system_software = "Android OS 11 / API-30 (RQ3A.210805.001)"
    major_login.system_hardware = "Handheld"    
    major_login.device_type = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1080
    major_login.screen_height = 2400
    major_login.screen_dpi = "440"
    major_login.processor_details = "ARMv8"
    major_login.memory = 6144
    major_login.gpu_renderer = "Adreno (TM) 650"
    major_login.gpu_version = "OpenGL ES 3.2 V@1.50"
    major_login.graphics_api = "OpenGLES3"
    major_login.supported_astc_bitset = 16383
    major_login.unique_device_id = f"Google|{random.randint(10000000,99999999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(100000000000,999999999999)}"
    major_login.client_ip = ""
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.memory_available.version = 55
    major_login.memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 2
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = random.randint(120000, 130000)
    major_login.external_storage_available = random.randint(38000, 52000)
    major_login.internal_storage_total = random.randint(100000, 120000)
    major_login.internal_storage_available = random.randint(18000, 32000)
    major_login.game_disk_storage_available = random.randint(18000, 28080)
    major_login.external_sdcard_avail_storage = random.randint(28080, 60000)
    major_login.external_sdcard_total_storage = random.randint(110000, 130000)
    major_login.login_by = 3
    major_login.library_path = "/data/app/~~random/base.apk"
    major_login.reg_avatar = 1
    major_login.library_token = "hash|base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.login_open_id_type = 4
    major_login.loading_time = random.randint(9000, 18000)
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTy3KUhvha/qugOBot9Bf7gcwqrf2btWC5rnrKZxrHIxEFfgxmPVkTxN+2dHiSprlxvm2Kl6o8EEgBJy7FzLLpbARlcqc2f/GQz+6UsLSMGXd"
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 0
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    
    string = major_login.SerializeToString()
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(string, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

async def MajorLogin(payload):
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    try:
        async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
            async with session.post(login_url+"MajorLogin", data=payload, headers=Hr, ssl=ssl_ctx) as resp:
                return await resp.read() if resp.status==200 else None
    except Exception:
        return None

async def GetLoginData(base_url, payload, token):
    headers = Hr.copy()
    headers['Authorization'] = f"Bearer {token}"
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    try:
        async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
            async with session.post(f"{base_url}/GetLoginData", data=payload, headers=headers, ssl=ssl_ctx) as resp:
                return await resp.read() if resp.status==200 else None
    except Exception:
        return None

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_packet = await EnC_PacKeT(token.encode().hex(), key, iv)
    encrypted_packet_length = hex(len(encrypted_packet)//2)[2:]
    headers = '0000000'
    if uid_length==8: headers = '00000000'
    elif uid_length==10: headers = '000000'
    elif uid_length==7: headers = '000000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"


# ========== ACCOUNT LOADER (JSON) ==========
def load_accounts(file_path="accs.json"):
    try:
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("{}")
            return {}
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                accounts = {str(k): str(v) for k, v in data.items() if str(k).isdigit()}
                return accounts
            else:
                console.print("[bold red]⚠️ accs.json is not a dictionary! Recreating with empty object.[/bold red]")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump({}, f, indent=4)
                return {}
    except Exception as e:
        console.print(f"[bold red]Error loading accounts: {e}[/bold red]")
        return {}

# ========== DYNAMIC ACCOUNT LOADER (THREAD BASED) ==========
def dynamic_account_loader():
    """Automatically scan accs.json and launch new accounts (thread based)"""
    while True:
        try:
            accounts = load_accounts()
            with running_bots_lock:
                for uid, pwd in accounts.items():
                    if uid not in running_bots:
                        running_bots.add(uid)
                        console.print(f"[bold green]✨ New Account Detected! Launching UID: {uid}[/bold green]")
                        threading.Thread(
                            target=lambda u=uid, p=pwd: asyncio.run(run_bot(u, p)),
                            daemon=True
                        ).start()
        except Exception as e:
            console.print(f"[bold red]Account Loader Error: {e}[/bold red]")
        time.sleep(3)

async def run_bot(uid, pwd):
    bot = FreeFireBot(uid=uid, password=pwd, server='bd', index=len(running_bots))
    await bot.keep_online_forever()


# ========== BOT CLIENT ==========
class FreeFireBot:
    def __init__(self, uid, password, server='bd', index=0):
        self.uid = uid
        self.password = password
        self.server = server
        self.index = index
        self.is_running = True
        self.online_writer = None
        self.chat_writer = None
        self.reader = None
        self.key = None
        self.iv = None
        self.region = None
        self.tasks = []
        self.is_online = False
        self.Nm = "Unknown"
        self.bot_uid = None
        self.chat_reader = None
        self.room_created = False
        self.room_members = set()
        self.room_members_names = {}
        
        update_bot_info(self.uid, status="🔄 Initializing...", room_active=False)

    # ---------- SHARE METHODS ----------
    async def send_share(self, target_id, share_type="map"):
        try:
            if share_type == "map":
                share_json = '{"WorkshopCode":"#FREEFIREF63E5AB9D1C9BECFEF06BBF1AD75D3E1K200","type":"UGCMapShare"}'
            
            fields = {
                1: 1, 
                2: {
                    1: int(self.bot_uid),
                    2: int(target_id),
                    3: 3, 
                    5: int(time.time()),
                    7: 1,
                    8: share_json, 
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
            packet = await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '1215', self.key, self.iv)
            if self.chat_writer:
                self.chat_writer.write(packet)
                await self.chat_writer.drain()
                await asyncio.sleep(0.1)
            return True
        except Exception:
            return False

    async def Auto_Room_Welcome(self, room_id, chat_code, user_uid, user_name="Player"):
        try:
            tracking_key = f"{self.bot_uid}_{room_id}_{user_uid}"
            current_time = time.time()
            if tracking_key in welcome_tracking:
                if current_time - welcome_tracking[tracking_key] < 0:
                    return
            welcome_tracking[tracking_key] = current_time

            if not self.chat_writer:
                return

            open_pkt = await MAHIR_OpeN_RoOm_ChaT(room_id, chat_code, self.key, self.iv)
            if open_pkt:
                self.chat_writer.write(open_pkt)
                await self.chat_writer.drain()
                await asyncio.sleep(0.4)

            welcome_msg = (
                f"[C][FFD700]❖━━━━━━━━━━━━━━━❖\n"
                f"[C][FFFFFF]Hᴇʟʟᴏ [FF0000]{user_name}\n"
                f"[C][00FF7F]Wᴇʟᴄᴏᴍᴇ ᴛᴏ Oᴜʀ Rᴏᴏᴍ! ✨\n"
                f"[C][FFD700]❖━━━━━━━━━━━━━━━❖\n"
                f"[C][B][00FFFF]🔥 MAHIR AUTOMATION BOT 🔥\n"
                f"[C][FFD700]────────────────\n"
                f"[C][FFFF00] Type [00FF00]/store [FFFF00]to view items\n"
                f"[C][FFFF00] Type [00FF00]/app [FFFF00]for Android App\n"
                f"[C][FFD700]────────────────\n"
                f"[C][00BFFF]📢 Telegram : [FFFFFF]@THEMAHIRWORLD\n"
                f"[C][FF69B4]🎬 TikTok   : [FFFFFF]@MAHIR__222\n"
                f"[C][00FF00]🛠️ Follow My Craftland Id\n"
                f"[C][00FF7F]🛠️ MY UID [FFFF00]1120🙂167🙂200\n"
                f"[C][FFD700]❖━━━━━━━━━━━━━━━❖"
            )
            msg_pkt = await MAHIR_SEnd_RoOm_MsG(room_id, welcome_msg, self.bot_uid, self.key, self.iv)
            if msg_pkt:
                self.chat_writer.write(msg_pkt)
                await self.chat_writer.drain()
            
            await asyncio.sleep(0.3)
            await self.send_share(room_id, "map")
            await asyncio.sleep(0.2)
            await self.send_share(room_id, "hud")
            
            curr_time_str = datetime.now().strftime("%I:%M:%S %p")
            update_bot_info(self.uid, last_room_id=str(room_id), last_active=curr_time_str)
            
        except Exception:
            pass

    # ---------- ROOM MEMBER EXTRACTION ----------
    def extract_room_members(self, packet_json):
        members = []
        try:
            f5 = packet_json.get('5', {}).get('data', {})
            field2 = f5.get('2', {}).get('data', {})
            if isinstance(field2, dict):
                for key, value in field2.items():
                    if isinstance(value, dict):
                        data = value.get('data', {})
                        if isinstance(data, dict):
                            uid = data.get('1', {}).get('data')
                            name = data.get('2', {}).get('data', 'Player')
                            if uid:
                                members.append((str(uid), str(name)))
            if not members:
                user_data = f5.get('1', {}).get('data', {})
                if isinstance(user_data, dict):
                    uid = user_data.get('2', {}).get('data')
                    name = user_data.get('3', {}).get('data', 'Player')
                    if uid:
                        members.append((str(uid), str(name)))
        except Exception:
            pass
        return members

    def get_room_mode(self):
        # জোড় সংখ্যক ইন্ডেক্সের বটগুলো 1v1 এবং বিজোড়গুলো 2v2 খুলবে
        if self.index % 2 == 0:
            return Room1v1, "1v1"
        else:
            return Room2v2, "2v2"

    # ---------- TCP ONLINE (ROOM UPDATE - MMM STYLE) ----------
    async def tcp_online(self, ip, port, auth_token):
        self.current_room_id = None 
        self.is_in_side2 = False 
        self.room_members = set() # মেম্বার ট্র্যাকিং
        
        while self.is_running:
            try:
                reader, writer = await asyncio.open_connection(ip, int(port))
                writer.write(bytes.fromhex(auth_token))
                await writer.drain()
                self.reader = reader
                self.online_writer = writer
                self.is_online = True
                update_bot_info(self.uid, status="✅ Online", room_active=True)
                
                selected_color = get_random_color()
                room_name = f"[B]➥{selected_color}ᎷAH!Ꮢ"
                room_func, mode_name = self.get_room_mode()
                room_pkt = room_func(room_name, self.key, self.iv)
                writer.write(room_pkt)
                await writer.drain()
                
                self.room_created = True
                self.is_in_side2 = False 
                console.print(f"[bold cyan][{self.uid}][/bold cyan] [green]Room Created: {room_name}[/green]")
                
                while self.is_running and self.is_online:
                    try:
                        data = await asyncio.wait_for(self.reader.read(65536), timeout=5.0)
                        if not data: break
                        data_hex = data.hex()
                        
                        if data_hex.startswith("0e00"):
                            decoded = DeCode_PackEt(data_hex[10:])
                            if decoded:
                                try:
                                    packet_json = json.loads(decoded)
                                    cmd_type = packet_json.get('4', {}).get('data')
                                    f5 = packet_json.get('5', {}).get('data', {})
                                    
                                    # --- ১. রুম আইডি ডিটেকশন (Field 5.2.1) ---
                                    room_data = f5.get('2', {}).get('data', {})
                                    p_rid = room_data.get('1', {}).get('data')
                                    
                                    if p_rid and 10000000 < int(p_rid) < 999999999:
                                        if self.current_room_id != p_rid:
                                            self.current_room_id = p_rid
                                            console.print(f"[bold cyan][{self.uid}][/bold cyan] [bold white]Active Room ID:[/bold white] [bold yellow]{p_rid}[/bold yellow]")
                                            update_bot_info(self.uid, last_room_id=str(p_rid), room_active=True)

                                    # --- ২. প্লেয়ার এবং নাম ডিটেকশন (Field 5.1.2 ও 5.1.3) ---
                                    user_data_container = f5.get('1', {}).get('data', {})
                                    u_uid = user_data_container.get('2', {}).get('data') # Player UID
                                    u_name = user_data_container.get('3', {}).get('data') # Player Nickname
                                    
                                    # চ্যাট কোড ফিল্ড
                                    c_code = room_data.get('36', {}).get('data') or room_data.get('40', {}).get('data')

                                    # জয়েন লজিক: যদি এটি আসল প্লেয়ার হয় এবং বট নিজে না হয়
                                    if u_uid and str(u_uid) != str(self.bot_uid) and len(str(u_uid)) > 8:
                                        uid_str = str(u_uid)
                                        
                                        if uid_str not in self.room_members:
                                            # নাম ঠিক করা (যদি নাম না থাকে তবে "Player" বলবে)
                                            display_name = str(u_name) if u_name and not str(u_name).isdigit() else "Player"
                                            
                                            console.print(f"[bold cyan][{self.uid}][/bold cyan] [bold green]➜ Player Joined:[/bold green] {display_name} ({uid_str})")
                                            
                                            # প্রথমে সাইড চেঞ্জ (Side 2)
                                            if not self.is_in_side2 and self.current_room_id:
                                                move_pkt = await Mahir_Room_Site_Change(self.current_room_id, self.bot_uid, 2, 1, self.key, self.iv)
                                                if move_pkt:
                                                    self.online_writer.write(move_pkt)
                                                    await self.online_writer.drain()
                                                    self.is_in_side2 = True
                                                    await asyncio.sleep(0.1)

                                            # তারপর নামসহ ওয়েলকাম মেসেজ
                                            if self.current_room_id and c_code:
                                                asyncio.create_task(self.Auto_Room_Welcome(self.current_room_id, c_code, uid_str, user_name=display_name))
                                            
                                            self.room_members.add(uid_str)

                                    # --- ৩. কেউ বেরিয়ে গেলে (cmd_type 7) ---
                                    if cmd_type == 7:
                                        self.room_members.clear() 
                                        if self.is_in_side2 and self.current_room_id:
                                            await asyncio.sleep(0.3)
                                            back_pkt = await Mahir_Room_Site_Change(self.current_room_id, self.bot_uid, 1, 1, self.key, self.iv)
                                            if back_pkt:
                                                self.online_writer.write(back_pkt)
                                                await self.online_writer.drain()
                                                self.is_in_side2 = False
                                                console.print(f"[bold cyan][{self.uid}][/bold cyan] [blue]Room empty. Bot back to Side 1.[/blue]")

                                    # --- ৪. রুম ফুল ও স্টার্ট লজিক ---
                                    if cmd_type == 65:
                                        is_full = f5.get('1', {}).get('data')
                                        if is_full == 1 and self.current_room_id:
                                            console.print(f"[bold cyan][{self.uid}][/bold cyan] [bold red]Room Full! Starting Match...[/bold red]")
                                            start_pkt = await Mahir_Room_START(self.current_room_id, self.key, self.iv)
                                            if start_pkt:
                                                self.online_writer.write(start_pkt)
                                                await self.online_writer.drain()
                                                await asyncio.sleep(1.0)
                                                exit_pkt = await Mahir_Room_ExiT(self.bot_uid, self.key, self.iv)
                                                if exit_pkt:
                                                    self.online_writer.write(exit_pkt)
                                                    await self.online_writer.drain()
                                                    await asyncio.sleep(1.0)
                                                    self.online_writer.write(room_pkt)
                                                    await self.online_writer.drain()
                                                    self.is_in_side2 = False 
                                    
                                except Exception: pass
                        
                    except asyncio.TimeoutError: continue
                    except Exception: break
                        
            except Exception: self.is_online = False
            await asyncio.sleep(10)

    # ---------- TCP CHAT (COMMAND HANDLING) ----------
    async def tcp_chat(self, ip, port, auth_token, key, iv, ready_event):
        while self.is_running:
            try:
                reader, writer = await asyncio.open_connection(ip, int(port))
                writer.write(bytes.fromhex(auth_token))
                await writer.drain()
                self.chat_reader = reader
                self.chat_writer = writer
                ready_event.set()
                
                while self.is_running:
                    try:
                        data = await asyncio.wait_for(self.chat_reader.read(4096), timeout=5.0)
                        if not data:
                            break
                        data_hex = data.hex()
                        if data_hex.startswith("1200"):
                            decoded = DeCode_PackEt(data_hex[10:])
                            if decoded:
                                try:
                                    packet_json = json.loads(decoded)
                                    f5 = packet_json.get('5', {}).get('data', {})
                                    msg_text = f5.get('4', {}).get('data', "").lower()
                                    chat_id = f5.get('2', {}).get('data')
                                    sender_uid = f5.get('1', {}).get('data')
                                    if str(sender_uid) == str(self.bot_uid):
                                        continue
                                    
                                    if "/store" in msg_text or "/stor" in msg_text:
                                        store_msg = (
                                            "[C][FFD700]❖━━━━━━━━━━━━━━━❖\n"
                                            "[C][B][00FFFF]⚡ MAHIR BOT STORE ⚡\n"
                                            "[C][FFD700]────────────────\n"
                                            "[C][00FF00]🤖 TCP BOT Price : [FFFF00]500 BDT\n"
                                            "[C][00FF00]🌐 Website       : [FFFF00]mahir🫡.xo🫡.🫡je\n"
                                            "[C][00FF00]👤 Owner Telegram : [FFFF00]@MAHIR0208\n"
                                            "[C][00FF00]🛠️ FOLLOW MY Craftland ID \n"
                                            "[C][FFD700]❖━━━━━━━━━━━━━━━❖"
                                        )
                                        pkt = await MAHIR_SEnd_RoOm_MsG(chat_id, store_msg, self.bot_uid, self.key, self.iv)
                                        if pkt:
                                            self.chat_writer.write(pkt)
                                            await self.chat_writer.drain()
                                    
                                    elif "/app" in msg_text:
                                        app_msg = (
                                            "[C][FFD700]❖━━━━━━━━━━━━━━━❖\n"
                                            "[C][B][00FFFF]📱 MAHIR TCP OFFICIAL APP 📱\n"
                                            "[C][FFD700]────────────────\n"
                                            "[C][FFFFFF]Download Link:\n"
                                            "[C][00FF00]https🙂://www🙂.mediafire🙂.com🙂/file🙂/lvykrek🙂51q17hae🙂/MAHIR_TCP🙂.apk\n"
                                            "[C][FFD700]❖━━━━━━━━━━━━━━━❖"
                                        )
                                        pkt = await MAHIR_SEnd_RoOm_MsG(chat_id, app_msg, self.bot_uid, self.key, self.iv)
                                        if pkt:
                                            self.chat_writer.write(pkt)
                                            await self.chat_writer.drain()
                                            
                                except Exception:
                                    pass
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        break
                        
            except Exception:
                pass
            await asyncio.sleep(10)

    # ---------- MAIN BOT LOOP ----------
    async def keep_online_forever(self):
        while self.is_running:
            try:
                open_id, access_token = await GeNeRaTeAccAccess(self.uid, self.password)
                if not open_id:
                    console.print(Panel(
                        f"[bold red]UID :[/bold red] {self.uid}\n[bold red]Error:[/bold red] Failed to generate guest token!",
                        title=f"[bold red]❌ AUTHENTICATION FAILED ({self.server.upper()})[/bold red]",
                        border_style="red",
                        expand=False
                    ))
                    update_bot_info(self.uid, status="❌ Auth Failed", room_active=False)
                    await asyncio.sleep(10)
                    continue
                    
                payload = await EncRypTMajoRLoGin(open_id, access_token)
                response = await MajorLogin(payload)
                if not response:
                    console.print(Panel(
                        f"[bold red]UID :[/bold red] {self.uid}\n[bold red]Error:[/bold red] Major login response missing!",
                        title=f"[bold red]❌ MAJOR LOGIN FAILED ({self.server.upper()})[/bold red]",
                        border_style="red",
                        expand=False
                    ))
                    update_bot_info(self.uid, status="❌ Login Failed", room_active=False)
                    await asyncio.sleep(10)
                    continue
                    
                auth_data = MajoRLoGinrEs_pb2.MajorLoginRes()
                auth_data.ParseFromString(response)
                
                login_data = await GetLoginData(auth_data.url, payload, auth_data.token)
                if not login_data:
                    console.print(Panel(
                        f"[bold red]UID :[/bold red] {self.uid}\n[bold red]Error:[/bold red] Login data not received!",
                        title=f"[bold red]❌ GET LOGIN DATA FAILED ({self.server.upper()})[/bold red]",
                        border_style="red",
                        expand=False
                    ))
                    update_bot_info(self.uid, status="❌ Data Failed", room_active=False)
                    await asyncio.sleep(10)
                    continue
                    
                port_data = PorTs_pb2.GetLoginData()
                port_data.ParseFromString(login_data)
                
                self.key = auth_data.key
                self.iv = auth_data.iv
                self.region = auth_data.region
                self.bot_uid = auth_data.account_uid
                
                try:
                    dec_jwt = jwt.decode(auth_data.token, options={"verify_signature": False})
                    self.Nm = dec_jwt.get('nickname') or "Unknown"
                    update_bot_info(self.uid, account_uid=str(auth_data.account_uid))
                except Exception:
                    self.Nm = "Unknown"
                
                online_ip, online_port = port_data.Online_IP_Port.split(":")
                chat_ip, chat_port = port_data.AccountIP_Port.split(":")
                
                auth_token = await xAuThSTarTuP(
                    auth_data.account_uid, 
                    auth_data.token, 
                    auth_data.timestamp, 
                    auth_data.key, 
                    auth_data.iv
                )
                
                ready = asyncio.Event()
                t1 = asyncio.create_task(
                    self.tcp_chat(chat_ip, chat_port, auth_token, auth_data.key, auth_data.iv, ready)
                )
                self.tasks.append(t1)
                await ready.wait()
                
                t2 = asyncio.create_task(
                    self.tcp_online(online_ip, online_port, auth_token)
                )
                self.tasks.append(t2)
                
                await asyncio.gather(t1, t2, return_exceptions=True)
                
            except Exception as e:
                console.print(Panel(
                    f"[bold red]UID :[/bold red] {self.uid}\n[bold red]Error:[/bold red] {e}",
                    title=f"[bold red]❌ UNEXPECTED BOT ERROR ({self.server.upper()})[/bold red]",
                    border_style="red",
                    expand=False
                ))
                update_bot_info(self.uid, status="❌ Error", room_active=False)
            await asyncio.sleep(10)


# ========== WEB SERVER ==========
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
            max-width: 1100px;
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
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 18px;
            margin-bottom: 35px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 20px;
            padding: 20px 15px;
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
            font-size: 0.8rem;
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
            <div class="stat-card">
                <div class="number" style="color:#ff8c00;" id="activeRooms">0</div>
                <div class="label"><i class="fas fa-door-open" style="color:#ff8c00;"></i> Active Rooms</div>
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
                    const activeRooms = document.getElementById('activeRooms');
                    
                    if (data.total_accs !== undefined) {
                        totalJsonAccs.textContent = data.total_accs;
                    }

                    const botData = data.bots || {};
                    let onlineCount = 0, connectingCount = 0, offlineCount = 0;
                    let roomActiveCount = 0;
                    let html = '';
                    const entries = Object.entries(botData);
                    
                    if (entries.length === 0) {
                        html = `<tr><td colspan="5" class="empty-msg"><i class="fas fa-robot"></i> No active bot processes</td></tr>`;
                    } else {
                        entries.forEach(([uid, info], index) => {
                            let statusText, badgeClass;
                            const statusStr = info.status || "Offline";
                            const roomActive = info.room_active === true;
                            const isOnline = statusStr.includes('✅') || statusStr.includes('Online') || statusStr.includes('Connected');

                            // Status classification
                            if (isOnline) {
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

                            // Active Rooms count: only if Online AND room_active True AND last_room_id not "None"
                            if (isOnline && roomActive && info.last_room_id && info.last_room_id !== "None") {
                                roomActiveCount++;
                            }

                            // Account UID: actual account_uid
                            const accountUid = (info.account_uid && info.account_uid !== "Loading...") 
                                ? `<div class="uid-badge"><i class="fas fa-id-card"></i> ${info.account_uid}</div>` 
                                : `<span style="color:#666;">Fetching UID...</span>`;

                            // Room ID: show only if Online, roomActive True, and last_room_id not "None"
                            const roomId = (isOnline && roomActive && info.last_room_id && info.last_room_id !== "None")
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
                    activeRooms.textContent = roomActiveCount;
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
                console.print("[bold yellow]accs.json updated via Web interface. Triggering auto-loader...[/bold yellow]")
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))

    def log_message(self, format, *args):
        pass

def start_web_server():
    port = 8080
    try:
        server = HTTPServer(('0.0.0.0', port), BotHandler)
        console.print(f"[bold green]🌐 Web Dashboard running at: http://localhost:{port}[/bold green]")
        # অটোমেটিক ব্রাউজার ওপেন হবে
        webbrowser.open(f'http://localhost:{port}')
        server.serve_forever()
    except OSError:
        console.print(f"[bold red]❌ Error: Port {port} is already in use. Please kill the previous process or free the port.[/bold red]")

# ========== MAIN FUNCTION ==========
async def main_async():
    print(render('MAHIR', colors=['white', 'red'], align='center'))
    
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()
    await asyncio.sleep(1)

    loader_thread = threading.Thread(target=dynamic_account_loader, daemon=True)
    loader_thread.start()
    
    console.print(Panel(
        "[bold green]✅ System Active & Running[/bold green]\n"
        "[cyan]🌐 Dashboard: http://localhost:8080 (or next available)[/cyan]\n"
        "[yellow]📁 Upload accs.json from Web UI to start bots[/yellow]",
        title="[bold red]🔥 MAHIR BOT SYSTEM 🔥[/bold red]",
        border_style="bright_red",
        expand=False
    ))

    while True:
        await asyncio.sleep(3600)

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main_async())
    except KeyboardInterrupt:
        console.print("\n[bold red] - Server shutting down...[/bold red]")

if __name__ == "__main__":
    main()