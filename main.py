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
import struct
from datetime import datetime
from io import BytesIO
import gzip
import http.client
import uuid
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

import aiohttp
import jwt
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from cfonts import render
from M4H1R import *

from protobuf_decoder.protobuf_decoder import Parser

from Pb2 import MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2

console = Console()

welcome_tracking = {}
running_bots = set()
running_bots_lock = threading.Lock()
bot_status = {}
bot_lock = threading.Lock()

online_count = 0
total_accounts = 0
active_accounts = []
active_lock = threading.Lock()

login_url, ob, version = "https://loginbp.ppmainecoonghj.com/", "OB55", "1.132.1"
TIMEOUT = aiohttp.ClientTimeout(total=30)
WEB_CONFIG_FILE = "web_config.json"

# ================================================================
#   DEFAULT CONFIGURATIONS
# ================================================================
DEFAULT_ROOM_MODES = {
    "Roomlw": {
        1: 2, 2: {1: 11, 2: 43, 3: 1, 4: "{room_name}", 6: 4, 7: 1, 8: 1, 9: 1, 11: 1,
            14: 3030901227, 15: {1: "IDC3", 2: 165, 3: "BD"},
            16: b"\x01\x07\x09\x0a\x0b\x12\x19\x20\x27\x29",
            18: 3030901002000, 27: 1, 34: b"\x00\x01", 40: "en",
            46: 1033, 48: 1, 49: {1: 21},
            50: {1: 35670336, 2: 10757192, 3: 80},
            51: "a_6534489873065906362", 56: 1}
    },
    "Room1v1": {
        1: 2, 2: {1: 1, 2: 15, 3: 0, 4: "{room_name}", 6: 2, 7: 1, 8: 1, 9: 1, 11: 1, 12: 2,
            14: 3030901227, 15: {1: "IDC3", 2: 126, 3: "BD"},
            16: b"\x01\x03\x04\x07\x09\x0a\x0b\x12\x0f\x0e\x16\x19\x1a\x20\x1d",
            18: 3030901002000, 27: 1, 34: b"\x00\x01", 40: "en", 48: 1, 49: {1: 2}}
    },
    "Room2v2": {
        1: 2, 2: {1: 1, 2: 15, 3: 1, 4: "{room_name}", 6: 4, 7: 1, 8: 1, 9: 1, 11: 1, 12: 2,
            14: 3030901227, 15: {1: "IDC3", 2: 126, 3: "BD"},
            16: b"\x01\x03\x04\x07\x09\x0a\x0b\x12\x0f\x0e\x16\x19\x1a\x20\x1d",
            18: 3030901002000, 27: 1, 34: b"\x00\x01", 40: "en", 48: 1, 49: {1: 2}}
    },
    "Room4v4": {
        1: 2, 2: {1: 1, 2: 15, 3: 3, 4: "{room_name}", 6: 8, 7: 1, 8: 1, 9: 1, 11: 1, 12: 2,
            14: 3030901227, 15: {1: "IDC3", 2: 126, 3: "BD"},
            16: b"\x01\x03\x04\x07\x09\x0a\x0b\x12\x0f\x0e\x16\x19\x1a\x20\x1d",
            18: 3030901002000, 27: 1, 34: b"\x00\x01", 40: "en", 48: 1, 49: {1: 2}}
    },
    "nRoom1v1": {
        1: 2, 2: {1: 1, 2: 15, 3: 0, 4: "{room_name}", 6: 2, 7: 1, 8: 1, 9: 1, 11: 1, 12: 2,
            14: 3030901227,
            15: [{1: "IDC1", 2: 3000, 3: "BD"}, {1: "IDC2", 2: 3000, 3: "BD"}]}
    },
    "nRoom2v2": {
        1: 2, 2: {1: 1, 2: 15, 3: 1, 4: "{room_name}", 6: 4, 7: 1, 8: 1, 9: 1, 11: 1, 12: 2,
            14: 3030901227,
            15: [{1: "IDC1", 2: 3000, 3: "BD"}, {1: "IDC2", 2: 3000, 3: "BD"}]}
    },
    "nRoom4v4": {
        1: 2, 2: {1: 1, 2: 15, 3: 3, 4: "{room_name}", 6: 8, 7: 1, 8: 1, 9: 1, 11: 1, 12: 2,
            14: 3030901227,
            15: [{1: "IDC1", 2: 3000, 3: "BD"}, {1: "IDC2", 2: 3000, 3: "BD"}]}
    },
    "nRoom6v6": {
        1: 2, 2: {1: 1, 2: 15, 3: 5, 4: "{room_name}", 6: 12, 7: 1, 8: 1, 9: 1, 11: 1, 12: 2,
            14: 36981056,
            15: [{1: "IDC1", 2: 3000, 3: "BD"}, {1: "IDC2", 2: 3000, 3: "BD"}]}
    },
}

DEFAULT_WELCOME_MSG = (
    "[C][FFD700]❖━━━━━━━━━━━━━━━❖\n"
    "[C][FFFFFF]Hᴇʟʟᴏ [FF0000]{user_name}\n"
    "[C][00FF7F]Wᴇʟᴄᴏᴍᴇ ᴛᴏ Oᴜʀ Rᴏᴏᴍ! ✨\n"
    "[C][FFD700]❖━━━━━━━━━━━━━━━❖\n"
    "[C][B][00FFFF]🔥 MAHIR AUTOMATION BOT 🔥\n"
    "[C][FFD700]────────────────\n"
    "[C][FFFF00] Type [00FF00]/store [FFFF00]to view items\n"
    "[C][FFFF00] Type [00FF00]/app [FFFF00]for Android App\n"
    "[C][FFD700]────────────────\n"
    "[C][00BFFF]📢 Telegram : [FFFFFF]@THEMAHIRWORLD\n"
    "[C][FF69B4]🎬 TikTok   : [FFFFFF]@MAHIR__222\n"
    "[C][00FF00]🛠️ Follow My Craftland Id\n"
    "[C][00FF7F]🛠️ MY UID [FFFF00]1120🙂167🙂200\n"
    "[C][FFD700]❖━━━━━━━━━━━━━━━❖"
)

# Share packets — placeholders: {bot_uid}, {target_id}, {timestamp}, {share_json}
DEFAULT_SHARE_PACKETS = {
    "map": {
        "enabled": True,
        "share_json": '{"WorkshopCode":"#FREEFIREF63E5AB9D1C9BECFEF06BBF1AD75D3E1K200","type":"UGCMapShare"}',
        "fields": {
            1: 1,
            2: {
                1: "{bot_uid}", 2: "{target_id}", 3: 3, 5: "{timestamp}", 7: 1, 8: "{share_json}",
                9: {
                    1: "[B][C][00FFFF]ᎷAH!Ꮢ ᏰOᎿ SYSTEM", 2: 902000016, 4: 330, 5: 801046518,
                    8: "ᎷAH!Ꮢ TEAM", 10: 1,
                    14: {1: 1158053040, 2: 8, 3: b"\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"}
                },
                10: "en", 13: {2: 2, 3: 1}
            }
        }
    },
    "hud": {
        "enabled": False,
        "share_json": '{"WorkshopCode":"#FREEFIREF63E5AB9D1C9BECFEF06BBF1AD75D3E1K200","type":"UGCMapShare"}',
        "fields": {
            1: 1,
            2: {
                1: "{bot_uid}", 2: "{target_id}", 3: 3, 5: "{timestamp}", 7: 1, 8: "{share_json}",
                9: {
                    1: "[B][C][00FFFF]ᎷAH!Ꮢ ᏰOᎿ SYSTEM", 2: 902000016, 4: 330, 5: 801046518,
                    8: "ᎷAH!Ꮢ TEAM", 10: 1,
                    14: {1: 1158053040, 2: 8, 3: b"\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"}
                },
                10: "en", 13: {2: 2, 3: 1}
            }
        }
    }
}

# Commands — {trigger: {...}}
# type: message | start_room | share | welcome
# match: exact | contains | startswith
DEFAULT_COMMANDS = {
    "/store": {
        "enabled": True,
        "match": "contains",
        "type": "message",
        "response": (
            "[C][FFD700]❖━━━━━━━━━━━━━━━❖\n"
            "[C][B][00FFFF]⚡ MAHIR BOT STORE ⚡\n"
            "[C][FFD700]────────────────\n"
            "[C][00FF00]🤖 TCP BOT Price : [FFFF00]500 BDT\n"
            "[C][00FF00]🌐 Website       : [FFFF00]mahir🫡.xo🫡.🫡je\n"
            "[C][00FF00]👤 Owner Telegram : [FFFF00]@MAHIR0208\n"
            "[C][FFD700]❖━━━━━━━━━━━━━━━❖"
        )
    },
    "/app": {
        "enabled": True,
        "match": "contains",
        "type": "message",
        "response": (
            "[C][FFD700]❖━━━━━━━━━━━━━━━❖\n"
            "[C][B][00FFFF]📱 MAHIR TCP OFFICIAL APP 📱\n"
            "[C][FFD700]────────────────\n"
            "[C][FFFFFF]Download Link:\n"
            "[C][00FF00]https🙂://www🙂.mediafire🙂.com🙂/file🙂/lvykrek🙂51q17hae🙂/MAHIR_TCP🙂.apk\n"
            "[C][FFD700]❖━━━━━━━━━━━━━━━❖"
        )
    },
    "st": {
        "enabled": True,
        "match": "exact",
        "type": "start_room"
    }
}

# ================================================================
#   WEB CONFIG
# ================================================================
web_config = {
    "enabled_modes": ["Room1v1", "Room2v2"],
    "room_name_template": "[B]➥{color}ᎷAH!Ꮢ",
    "use_mode": "all",
    "welcome_msg": DEFAULT_WELCOME_MSG,
    "welcome_shares": ["map"],
    "room_modes": {},
    "commands": {},
    "share_packets": {},
}
web_config_lock = threading.Lock()

# ================================================================
#   JSON-SAFE SERIALIZATION
# ================================================================
def to_json_safe(obj):
    if isinstance(obj, dict):
        return {str(k): to_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_json_safe(item) for item in obj]
    elif isinstance(obj, (bytes, bytearray)):
        return {"__hex__": bytes(obj).hex()}
    else:
        return obj

def from_json_safe(obj):
    if isinstance(obj, dict):
        if "__hex__" in obj and len(obj) == 1:
            try: return bytes.fromhex(obj["__hex__"])
            except Exception: return b""
        result = {}
        for k, v in obj.items():
            try: key = int(k)
            except (ValueError, TypeError): key = k
            result[key] = from_json_safe(v)
        return result
    elif isinstance(obj, list):
        return [from_json_safe(item) for item in obj]
    return obj

# ================================================================
#   PLACEHOLDER RESOLVER (preserves types)
# ================================================================
def resolve_placeholders(fields, context):
    if isinstance(fields, dict):
        return {k: resolve_placeholders(v, context) for k, v in fields.items()}
    elif isinstance(fields, list):
        return [resolve_placeholders(item, context) for item in fields]
    elif isinstance(fields, str):
        # Exact placeholder → return typed value
        for key, val in context.items():
            if fields == "{" + key + "}":
                return val
        # Otherwise do string replacement
        result = fields
        for key, val in context.items():
            result = result.replace("{" + key + "}", str(val))
        return result
    return fields

# ================================================================
#   LOAD / SAVE WEB CONFIG
# ================================================================
def _deep_copy_defaults(src):
    return {k: (dict(v) if isinstance(v, dict) else v) for k, v in src.items()}

def load_web_config():
    try:
        saved = {}
        if os.path.exists(WEB_CONFIG_FILE):
            with open(WEB_CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)

        with web_config_lock:
            em = saved.get("enabled_modes")
            if isinstance(em, list) and em:
                valid = [m for m in em if m in DEFAULT_ROOM_MODES]
                if valid: web_config["enabled_modes"] = valid

            rt = saved.get("room_name_template")
            if isinstance(rt, str) and rt: web_config["room_name_template"] = rt

            um = saved.get("use_mode")
            if um in ("all", "half"): web_config["use_mode"] = um

            wm = saved.get("welcome_msg")
            if isinstance(wm, str) and wm: web_config["welcome_msg"] = wm

            ws = saved.get("welcome_shares")
            if isinstance(ws, list):
                web_config["welcome_shares"] = [s for s in ws if isinstance(s, str)]

            # room_modes
            rmodes = saved.get("room_modes", {})
            modes = {}
            for name, default_fields in DEFAULT_ROOM_MODES.items():
                if name in rmodes:
                    try: modes[name] = from_json_safe(rmodes[name])
                    except Exception: modes[name] = _deep_copy_defaults(default_fields)
                else:
                    modes[name] = _deep_copy_defaults(default_fields)
            web_config["room_modes"] = modes

            # share_packets
            sp = saved.get("share_packets", {})
            shares = {}
            # start from defaults
            for name, default_val in DEFAULT_SHARE_PACKETS.items():
                if name in sp:
                    try:
                        loaded = from_json_safe(sp[name])
                        if isinstance(loaded, dict):
                            shares[name] = loaded
                        else:
                            shares[name] = dict(default_val)
                    except Exception:
                        shares[name] = dict(default_val)
                else:
                    shares[name] = dict(default_val)
            # add custom shares not in default
            for name, val in sp.items():
                if name not in shares:
                    try:
                        loaded = from_json_safe(val)
                        if isinstance(loaded, dict): shares[name] = loaded
                    except Exception:
                        pass
            web_config["share_packets"] = shares

            # commands
            cmds_saved = saved.get("commands", {})
            commands = {}
            for name, default_val in DEFAULT_COMMANDS.items():
                if name in cmds_saved:
                    try:
                        loaded = from_json_safe(cmds_saved[name])
                        if isinstance(loaded, dict): commands[name] = loaded
                        else: commands[name] = dict(default_val)
                    except Exception:
                        commands[name] = dict(default_val)
                else:
                    commands[name] = dict(default_val)
            for name, val in cmds_saved.items():
                if name not in commands:
                    try:
                        loaded = from_json_safe(val)
                        if isinstance(loaded, dict): commands[name] = loaded
                    except Exception:
                        pass
            web_config["commands"] = commands

        console.print(f"[bold green]✅ Web Config Loaded:[/bold green] modes={web_config['enabled_modes']} "
                      f"| shares={list(web_config['share_packets'].keys())} "
                      f"| commands={list(web_config['commands'].keys())}")
    except Exception as e:
        console.print(f"[bold red]Web Config Load Error: {e}[/bold red]")
        with web_config_lock:
            web_config["room_modes"] = {k: _deep_copy_defaults(v) for k, v in DEFAULT_ROOM_MODES.items()}
            web_config["share_packets"] = {k: dict(v) for k, v in DEFAULT_SHARE_PACKETS.items()}
            web_config["commands"] = {k: dict(v) for k, v in DEFAULT_COMMANDS.items()}

def save_web_config():
    try:
        with web_config_lock:
            data = {
                "enabled_modes": list(web_config["enabled_modes"]),
                "room_name_template": web_config["room_name_template"],
                "use_mode": web_config["use_mode"],
                "welcome_msg": web_config["welcome_msg"],
                "welcome_shares": list(web_config["welcome_shares"]),
                "room_modes": to_json_safe(web_config["room_modes"]),
                "commands": to_json_safe(web_config["commands"]),
                "share_packets": to_json_safe(web_config["share_packets"]),
            }
        with open(WEB_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        console.print(f"[bold red]Web Config Save Error: {e}[/bold red]")
        return False

# ================================================================
#   PROTOBUF PARSER
# ================================================================
def read_varint(data, pos):
    result = 0; shift = 0
    while pos < len(data):
        b = data[pos]; pos += 1
        result |= (b & 0x7F) << shift
        if not (b & 0x80): break
        shift += 7
    return result, pos

def parse_pb(data):
    fields = {}; pos = 0; n = len(data)
    while pos < n:
        try: key, pos = read_varint(data, pos)
        except: break
        fn = key >> 3; wt = key & 0x07
        try:
            if wt == 0: val, pos = read_varint(data, pos)
            elif wt == 2:
                ln, pos = read_varint(data, pos); val = data[pos:pos + ln]; pos += ln
            elif wt == 5: val = data[pos:pos + 4]; pos += 4
            elif wt == 1: val = data[pos:pos + 8]; pos += 8
            else: break
        except: break
        fields.setdefault(fn, []).append(val)
    return fields

def extract_player_name(login_data_bytes):
    try:
        fields = parse_pb(login_data_bytes)
        for field_num in [4, 3, 5, 6]:
            if field_num in fields:
                name_val = fields[field_num][0]
                if isinstance(name_val, (bytes, bytearray)):
                    decoded = name_val.decode('utf-8', errors='ignore')
                    if (decoded and len(decoded) < 60 and
                        not decoded.startswith("0OuCe") and
                        not decoded.startswith("eyJ") and
                        all(c.isprintable() or c in '\u200b\u200c\u200d' for c in decoded)):
                        return decoded
    except Exception:
        pass
    return None

def Uaa():
    versions = ['5.0.1B2','5.1.0P1','5.2.0B1']
    models = ['SM-A125F','Redmi 9A','POCO M3']
    android = random.choice(['11','12','13'])
    return f"GarenaMSDK/{random.choice(versions)}({random.choice(models)};Android {android};en-US;USA;)"

Hr = {
    'User-Agent': Uaa(), 'Connection': "Keep-Alive", 'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'X-Unity-Version': "2018.4.11f1", 'X-GA': "v1 1", 'ReleaseVersion': ob
}

def get_random_color():
    colors = ["[FF0000]","[00FF00]","[0000FF]","[FFFF00]","[FF00FF]","[00FFFF]","[FFFFFF]","[FFA500]","[FFC0CB]","[FFD700]"]
    return random.choice(colors)

def xBunnEr():
    return int(random.choice(['902000016','902000031','902000011','902000065','902000204','902000192','902000191','902000179','902000133','902045001','902038023','902048004','902039014','902000063','902000306','902047009']))

def update_bot_info(uid, **kwargs):
    with bot_lock:
        if uid not in bot_status:
            bot_status[uid] = {"guest_uid": uid, "account_uid": "Loading...", "status": "🔄 Initializing...",
                "last_room_id": "None", "last_active": "N/A", "room_active": False}
        bot_status[uid].update(kwargs)

def update_active_account(uid, **kwargs):
    with active_lock:
        global online_count
        for acc in active_accounts:
            if acc['uid'] == uid:
                acc.update(kwargs); return
        active_accounts.append({
            'uid': uid, 'bot_uid': kwargs.get('bot_uid', uid),
            'name': kwargs.get('name', 'Unknown'), 'region': kwargs.get('region', 'BD'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'room_id': kwargs.get('room_id', 'Pending...'),
            'room_name': kwargs.get('room_name', 'Pending...')
        })

def remove_active_account(uid):
    global online_count
    with active_lock:
        active_accounts[:] = [a for a in active_accounts if a['uid'] != uid]
        if online_count > 0: online_count -= 1

def Fix_PackEt(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {'wire_type': result.wire_type}
        if result.wire_type in ["varint", "string", "bytes"]: field_data['data'] = result.data
        elif result.wire_type == 'length_delimited': field_data["data"] = Fix_PackEt(result.data.results)
        result_dict[result.field] = field_data
    return result_dict

def DeCode_PackEt(input_text):
    try:
        return json.dumps(Fix_PackEt(Parser().parse(input_text)))
    except Exception:
        return None

async def EnC_Vr(N):
    if N<0: return b''
    H = []
    while True:
        RedZed = N & 0x7F; N >>= 7
        if N: RedZed |= 0x80
        H.append(RedZed)
        if not N: break
    return bytes(H)

async def CrEaTe_VarianT(fn, val): return await EnC_Vr((fn<<3)|0) + await EnC_Vr(val)

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
        elif isinstance(v,int): packet.extend(await CrEaTe_VarianT(f,v))
        elif isinstance(v,(str,bytes)): packet.extend(await CrEaTe_LenGTh(f,v))
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

async def MAHIR_OpeN_RoOm_ChaT(room_id: int, chat_code: str, key: bytes, iv: bytes):
    try:
        fields = {1: 3, 2: {1: int(room_id), 2: 3, 3: "en", 4: str(chat_code)}}
        proto_bytes = await CrEaTe_ProTo(fields)
        return await GeneRaTePk(proto_bytes.hex(), '1215', key, iv)
    except Exception:
        return None

async def MAHIR_SEnd_RoOm_MsG(room_id: int, message: str, bot_uid: int, key: bytes, iv: bytes):
    try:
        timestamp = int(datetime.now().timestamp())
        avatar = xBunnEr()
        fields = {
            1: 1, 2: {1: int(bot_uid), 2: int(room_id), 3: 3, 4: message, 5: timestamp, 7: 6,
                9: {1: f"[C][FF0000]{message[:15]}", 2: avatar, 3: 2, 4: 330, 5: 800000304,
                    6: 66, 7: 66, 8: "MAHIR", 9: 66, 10: 1, 11: 1, 13: {1: 68, 2: 67},
                    14: {1: 1158053040, 2: 8, 3: b"\x10\x15\x08\x0A\x0B\x15\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"}},
                10: "en", 13: {3: 1}, 14: {}
            }
        }
        proto_bytes = await CrEaTe_ProTo(fields)
        return await GeneRaTePk(proto_bytes.hex(), '1215', key, iv)
    except Exception:
        return None

async def Mahir_Room_Site_Change(room_id, bot_id, side, slot, key, iv):
    try:
        fields = {1: 20, 2: {1: int(room_id), 2: int(bot_id), 3: int(side), 4: int(slot), 6: 1}}
        return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0e15', key, iv)
    except Exception:
        return None

async def Mahir_Room_START(room_id, key, iv):
    try:
        fields = {1: 11, 2: {1: int(room_id), 2: 1}}
        return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0e15', key, iv)
    except Exception:
        return None

async def Mahir_Room_ExiT(bot_uid, key, iv):
    try:
        fields = {1: 6, 2: {1: int(bot_uid)}}
        return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0e15', key, iv)
    except Exception:
        return None

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

def encode_varint(value):
    result = []
    if value < 0: value &= (1 << 64) - 1
    while True:
        byte = value & 0x7F; value >>= 7
        if value: byte |= 0x80
        result.append(byte)
        if not value: break
    return bytes(result)

def create_proto(fields):
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(value, dict):
            nested = create_proto(value)
            packet.extend(encode_varint((field << 3) | 2))
            packet.extend(encode_varint(len(nested))); packet.extend(nested)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    nested = create_proto(item)
                    packet.extend(encode_varint((field << 3) | 2))
                    packet.extend(encode_varint(len(nested))); packet.extend(nested)
        elif isinstance(value, int):
            packet.extend(encode_varint((field << 3) | 0)); packet.extend(encode_varint(value))
        elif isinstance(value, str):
            encoded = value.encode('utf-8')
            packet.extend(encode_varint((field << 3) | 2))
            packet.extend(encode_varint(len(encoded))); packet.extend(encoded)
        elif isinstance(value, bytes):
            packet.extend(encode_varint((field << 3) | 2))
            packet.extend(encode_varint(len(value))); packet.extend(value)
    return bytes(packet)

def encrypt_aes(hex_data: str) -> str:
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv  = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pad(bytes.fromhex(hex_data), AES.block_size)).hex()

async def EncRypTMajoRLoGin(open_id: str, access_token: str, version: str) -> bytes:
    fields = {
        3: str(datetime.now())[:-7], 4: "free fire", 5: 1, 7: str(version),
        8: "Android OS 11 / API-30 (RP1A.200720.011/230921V810)", 9: "Handheld",
        10: "Grameenphone", 11: "WIFI", 12: 1708, 13: 750, 14: "480",
        15: "ARM64 FP ASIMD AES | 2000 | 8", 16: 5767, 17: "Mali-G52 MC2",
        18: "OpenGL ES 3.2 v1.r26p0-01eac0.f143e3f9482527bbad36b3ec27f93e59",
        19: "Google|3f10d414-be33-4ac3-b9fc-fcbf47c183b5", 20: "103.200.36.134",
        21: "en", 22: str(open_id), 23: "4", 24: "Handheld",
        25: "INFINIX MOBILITY LIMITED Infinix X6812", 26: "BD", 29: str(access_token), 30: 1,
        41: "Grameenphone", 42: "WIFI", 57: "7428b253defc164018c604a1ebbfebdf",
        60: 110962, 61: 80611, 62: 1051, 64: 80829, 65: 110962, 66: 80829, 67: 110962, 73: 2,
        74: "/data/app/~~MxBbX9YA6AkFscre_RExgw==/com.dts.freefireth-hLOkTeh1Q46L_oLV4UXQTg==/lib/arm64", 76: 1,
        77: "b8e0cd5e295eee42f5860d3c86e483dd|/data/app/~~MxBbX9YA6AkFscre_RExgw==/com.dts.freefireth-hLOkTeh1Q46L_oLV4UXQTg==/base.apk",
        78: 3, 79: 2, 81: "64", 83: "2019121229", 85: 3, 86: "OpenGLES2", 87: 4095, 88: 4,
        91: {9: 65}, 92: 10508, 93: "android",
        94: "KqsHT76RdsVKvnpkirzc2FQs3eu0OZChfZxMTZn+Rjv06Ri2qeOQkyPcdk5JceWKmXhOFFUPuNy9S8esTr37yCT5piY32iUcehVw0bL4F4lzAmyD",
        95: 111207, 96: '{"cur_rate":[60,90],"support_etc2":false}', 97: 1, 98: 1, 99: "4", 100: "4",
        102: "B\\FFP[[\tf", 103: 1, 104: 28754, 105: 1,
        106: "https://dl.ak.freefiremobile.com/live/ABHotUpdates/|https://core-ak.freefiremobile.com/live/ABHotUpdates/|a4332cb1c1a84e51dd77441e4856ed5a",
        107: "1.477aa00e98bf924c"
    }
    return bytes.fromhex(encrypt_aes(create_proto(fields).hex()))

async def MajorLogin(payload):
    global login_url
    base = login_url.rstrip("/")
    if not base.startswith(("http://", "https://")): base = "https://" + base
    url = f"{base}/MajorLogin"
    Hr["X-GA-SV"] = str(int(time.time()))
    Hr["ReleaseVersion"] = ob
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status != 200: return None
            raw = await response.read()
            return raw[64:] if len(raw) > 64 else raw

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization'] = f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    class ParsedMajorLogin:
        def __init__(self, fields):
            self.account_uid = int(fields.get(1, 0))
            self.region = str(fields.get(2, ""))
            self.token = str(fields.get(8, ""))
            self.url = str(fields.get(10, ""))
            self.timestamp = int(fields.get(21, 0))
            raw_key = fields.get(22, b"")
            if isinstance(raw_key, str):
                try: self.key = bytes.fromhex(raw_key.replace(" ", ""))
                except: self.key = raw_key.encode()
            else: self.key = bytes(raw_key)
            raw_iv = fields.get(23, b"")
            if isinstance(raw_iv, str):
                try: self.iv = bytes.fromhex(raw_iv.replace(" ", ""))
                except: self.iv = raw_iv.encode()
            else: self.iv = bytes(raw_iv)

    def _dec_vr(buf, off):
        res, sh, st = 0, 0, off
        while True:
            if off >= len(buf): raise IndexError("Out")
            b = buf[off]; off += 1
            res += (b & 0x7F) << sh; sh += 7
            if b < 0x80: break
        return res, off - st

    def _dec_proto(buf):
        off, parts, blen = 0, [], len(buf)
        try:
            while off < blen:
                it, vl = _dec_vr(buf, off); off += vl
                wt, fn = it & 7, it >> 3
                if wt == 0: val, vl = _dec_vr(buf, off); off += vl
                elif wt == 2:
                    length, vl = _dec_vr(buf, off); off += vl
                    if off + length > blen: return None
                    val = buf[off:off + length]; off += length
                elif wt == 5:
                    if off + 4 > blen: return None
                    val = struct.unpack_from("<I", buf, off)[0]; off += 4
                elif wt == 1:
                    if off + 8 > blen: return None
                    val = struct.unpack_from("<Q", buf, off)[0]; off += 8
                else: return None
                parts.append((fn, wt, val))
            return parts
        except: return None

    def _to_dict(parts):
        res = {}
        for fn, wt, v in parts:
            if wt == 2:
                try: val = v.decode("utf-8")
                except: val = v
            else: val = v
            res[fn] = val
        return res

    buf = MajoRLoGinResPonsE
    try:
        c = AES.new(b'Yg&tc%DEuh6%Zc^8', AES.MODE_CBC, b'6oyZDr22E3ychjM%')
        buf = unpad(c.decrypt(buf), AES.block_size)
    except: buf = MajoRLoGinResPonsE

    parsed = _dec_proto(buf)
    if parsed:
        d = _to_dict(parsed)
        if 1 in d or 8 in d or 10 in d: return ParsedMajorLogin(d)

    for o in range(len(buf)):
        parsed = _dec_proto(buf[o:])
        if parsed:
            d = _to_dict(parsed)
            if 1 in d or 8 in d or 10 in d: return ParsedMajorLogin(d)

    try:
        proto = MajoRLoGinrEs_pb2.MajorLoginRes()
        proto.ParseFromString(MajoRLoGinResPonsE)
        return proto
    except: pass

    return ParsedMajorLogin({})

def create_auth_token_chat(account_id, jwt_token, timestamp, key, iv):
    try:
        K = bytes.fromhex(key) if isinstance(key, str) else key
        V = bytes.fromhex(iv)  if isinstance(iv,  str) else iv
        ct = AES.new(K, AES.MODE_CBC, V).encrypt(pad(jwt_token.encode('utf-8'), AES.block_size))
        header = bytes.fromhex('6d19') + int(account_id).to_bytes(8, 'big') + int(timestamp).to_bytes(4, 'big') + len(ct).to_bytes(4, 'big')
        return (header + ct).hex()
    except Exception as e:
        print(f"❌ CHAT AUTH: {e}"); return None

def create_auth_token_online(account_uid, token, kts, key, iv):
    try:
        K = bytes.fromhex(key) if isinstance(key, str) else key
        V = bytes.fromhex(iv)  if isinstance(iv,  str) else iv
        enc_token = AES.new(K, AES.MODE_CBC, V).encrypt(pad(token.encode("utf-8"), 16))
        opcode = bytes.fromhex("830c")
        return (opcode + int(account_uid).to_bytes(8, byteorder="big") + int(kts).to_bytes(4, byteorder="big") + len(enc_token).to_bytes(8, byteorder="big") + enc_token).hex()
    except Exception as e:
        print(f"❌ ONLINE AUTH: {e}"); return None

def load_accounts(file_path="accs.json"):
    try:
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f: f.write("{}")
            return {}
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return {str(k): str(v) for k, v in data.items() if str(k).isdigit()}
            return {}
    except Exception as e:
        console.print(f"[bold red]Acc Load Error: {e}[/bold red]")
        return {}

async def process_single_bot(uid, pwd, index):
    for attempt in range(1, 3):
        bot = FreeFireBot(uid=uid, password=pwd, server='bd', index=index)
        bot_task = asyncio.create_task(bot.keep_online_forever())
        wait_time = 0
        while wait_time < 20:
            await asyncio.sleep(0.5); wait_time += 0.5
            if bot.is_online: return True
        bot.is_running = False; bot_task.cancel()
        await asyncio.sleep(0.2)
    console.print(f"[bold red]🚫 Skipping UID {uid}.[/bold red]")
    return False

async def batch_account_loader():
    global total_accounts
    launched_accounts = set()
    active_tasks = {}
    while True:
        try:
            accounts = load_accounts()
            total_accounts = len(accounts)
            new_accounts = [(uid, pwd) for uid, pwd in accounts.items() if uid not in launched_accounts]
            for uid, pwd in new_accounts:
                if uid in launched_accounts: continue
                launched_accounts.add(uid)
                with running_bots_lock: running_bots.add(uid)
                console.print(f"[bold green]✨ New Account → UID {uid} → Launching...[/bold green]")
                task = asyncio.create_task(process_single_bot(uid, pwd, len(launched_accounts)))
                active_tasks[uid] = task
                await asyncio.sleep(0.15)
            for uid in list(active_tasks.keys()):
                if active_tasks[uid].done(): del active_tasks[uid]
        except Exception as e:
            console.print(f"[bold red]Loader Err: {e}[/bold red]")
        await asyncio.sleep(1)

def ResTarTinG():
    console.print("[bold yellow]♻️ Restarting...[/bold yellow]")
    time.sleep(0.5)
    os.execl(sys.executable, sys.executable, *sys.argv)

def AuTo_ResTartinG():
    while True:
        time.sleep(3600)
        console.print("[bold red]⚠️ Auto restart...[/bold red]")
        ResTarTinG()

# ================================================================
#   BOT CLIENT
# ================================================================
class FreeFireBot:
    def __init__(self, uid, password, server='bd', index=0):
        self.uid = uid; self.password = password; self.server = server; self.index = index
        self.is_running = True
        self.online_writer = None; self.chat_writer = None; self.reader = None
        self.key = None; self.iv = None; self.region = None; self.tasks = []
        self.is_online = False; self.Nm = "Unknown"; self.bot_uid = None
        self.chat_reader = None; self.room_created = False; self.room_members = set()
        self.current_room_id = None; self.current_room_name = None; self.is_in_side2 = False
        update_bot_info(self.uid, status="🔄 Initializing...", room_active=False)

    # ---------- SEND SHARE (from config) ----------
    async def send_share(self, target_id, share_name):
        try:
            with web_config_lock:
                share_cfg = dict(web_config.get("share_packets", {}).get(share_name, {}))
            if not share_cfg or not share_cfg.get("enabled", True):
                return False
            fields_template = share_cfg.get("fields", {})
            share_json = share_cfg.get("share_json", "")
            context = {
                "bot_uid": int(self.bot_uid),
                "target_id": int(target_id),
                "timestamp": int(time.time()),
                "share_json": share_json,
            }
            fields = resolve_placeholders(fields_template, context)
            packet = await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '1215', self.key, self.iv)
            if self.chat_writer:
                self.chat_writer.write(packet)
                await self.chat_writer.drain()
                await asyncio.sleep(0.1)
            return True
        except Exception as e:
            console.print(f"[bold red]send_share[{share_name}] err: {e}[/bold red]")
            return False

    # ---------- WELCOME ----------
    async def Auto_Room_Welcome(self, room_id, chat_code, user_uid, user_name="Player"):
        try:
            tracking_key = f"{self.bot_uid}_{room_id}_{user_uid}"
            current_time = time.time()
            if tracking_key in welcome_tracking:
                if current_time - welcome_tracking[tracking_key] < 0: return
            welcome_tracking[tracking_key] = current_time
            if not self.chat_writer: return
            open_pkt = await MAHIR_OpeN_RoOm_ChaT(room_id, chat_code, self.key, self.iv)
            if open_pkt:
                self.chat_writer.write(open_pkt); await self.chat_writer.drain()
                await asyncio.sleep(0.4)

            with web_config_lock:
                welcome_template = web_config.get("welcome_msg", DEFAULT_WELCOME_MSG)
                welcome_shares = list(web_config.get("welcome_shares", ["map"]))
            welcome_msg = welcome_template.replace("{user_name}", str(user_name))

            msg_pkt = await MAHIR_SEnd_RoOm_MsG(room_id, welcome_msg, self.bot_uid, self.key, self.iv)
            if msg_pkt:
                self.chat_writer.write(msg_pkt); await self.chat_writer.drain()
            await asyncio.sleep(0.3)
            for sh in welcome_shares:
                await self.send_share(room_id, sh)
                await asyncio.sleep(0.2)
            curr_time_str = datetime.now().strftime("%I:%M:%S %p")
            update_bot_info(self.uid, last_room_id=str(room_id), last_active=curr_time_str)
        except Exception:
            pass

    def get_room_mode(self):
        with web_config_lock:
            enabled = list(web_config.get("enabled_modes", ["Room1v1", "Room2v2"]))
            use_mode = web_config.get("use_mode", "all")
            all_modes = web_config.get("room_modes", {})
        enabled = [m for m in enabled if m in all_modes]
        if not enabled: enabled = ["Room1v1", "Room2v2"]
        if use_mode == "half" and len(enabled) > 1:
            half_count = max(1, len(enabled) // 2)
            pool = random.sample(enabled, half_count)
        else: pool = enabled
        chosen_name = random.choice(pool)
        fields_template = all_modes.get(chosen_name) or DEFAULT_ROOM_MODES.get(chosen_name, {})
        return chosen_name, fields_template

    def build_room_name(self):
        with web_config_lock:
            template = web_config.get("room_name_template", "[B]➥{color}ᎷAH!Ꮢ")
        try: return template.replace("{color}", get_random_color())
        except Exception: return f"[B]➥{get_random_color()}ᎷAH!Ꮢ"

    # ---------- TCP ONLINE ----------
    async def tcp_online(self, ip, port, auth_token):
        self.current_room_id = None; self.current_room_name = None
        self.is_in_side2 = False; self.room_members = set()
        while self.is_running:
            try:
                reader, writer = await asyncio.open_connection(ip, int(port))
                writer.write(bytes.fromhex(auth_token)); await writer.drain()
                self.reader, self.online_writer = reader, writer
                self.is_online = True
                update_bot_info(self.uid, status="✅ Online", room_active=True)
                console.print(f"[bold cyan]ℹ [{self.uid}] ONLINE Connected ✅[/bold cyan]")

                room_name = self.build_room_name()
                mode_name, fields_template = self.get_room_mode()
                try:
                    fields = resolve_placeholders(fields_template, {"room_name": room_name})
                    proto = await CrEaTe_ProTo(fields)
                    self.room_pkt = await GeneRaTePk(proto.hex(), '0e0b', self.key, self.iv)
                    if not self.room_pkt:
                        self.is_online = False; await asyncio.sleep(5); continue
                except Exception as e:
                    console.print(f"[bold red]❌ [{self.uid}] ROOM FAIL: {e}[/bold red]")
                    self.is_online = False; await asyncio.sleep(5); continue

                self.online_writer.write(self.room_pkt); await self.online_writer.drain()
                self.room_created = True
                console.print(f"[bold cyan]ℹ [{self.uid}] Room Created ({mode_name}) ✅[/bold cyan]")

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

                                    if cmd_type in [5, 25, 1]:
                                        room_info = f5.get('2', {}).get('data', {})
                                        r_id = room_info.get('1', {}).get('data')
                                        r_name = room_info.get('2', {}).get('data')
                                        if isinstance(r_name, (bytes, bytearray)):
                                            try: r_name = r_name.decode('utf-8', errors='ignore')
                                            except: r_name = str(r_name)
                                        if isinstance(r_name, dict): r_name = r_name.get('data', 'Unknown')
                                        if r_id and str(r_id) != str(self.current_room_id):
                                            if 10000000 < int(r_id) < 999999999:
                                                self.current_room_id = str(r_id)
                                                self.current_room_name = str(r_name) if r_name else "Unknown"
                                                console.print(Panel(
                                                    f"[bold green]🏠 Room Name :[/bold green] [white]{self.current_room_name}[/white]\n"
                                                    f"[bold green]🆔 Room ID   :[/bold green] [bold yellow]{self.current_room_id}[/bold yellow]\n"
                                                    f"[bold cyan]👤 Bot Name  :[/bold cyan] [white]{self.Nm}[/white]\n"
                                                    f"[bold cyan]🆔 Bot UID   :[/bold cyan] [white]{self.bot_uid}[/white]",
                                                    title=f"[bold magenta]✨ ROOM ESTABLISHED ({self.uid})[/bold magenta]",
                                                    border_style="cyan"))
                                                console.print(f"[bold yellow]{self.bot_uid}৷ {self.Nm}[/bold yellow]")
                                                update_bot_info(self.uid, last_room_id=str(r_id), room_active=True)
                                                update_active_account(self.uid, **{
                                                    'bot_uid': str(self.bot_uid), 'name': self.Nm,
                                                    'region': self.region or 'BD',
                                                    'room_id': self.current_room_id,
                                                    'room_name': self.current_room_name})

                                    user_info = f5.get('1', {}).get('data', {})
                                    if isinstance(user_info, dict):
                                        u_uid = user_info.get('2', {}).get('data')
                                        u_name = user_info.get('3', {}).get('data')
                                        if u_uid and str(u_uid) != str(self.bot_uid) and len(str(u_uid)) > 8:
                                            uid_str = str(u_uid)
                                            if uid_str not in self.room_members:
                                                p_name = str(u_name) if u_name and not str(u_name).isdigit() else "Player"
                                                if not self.is_in_side2 and self.current_room_id:
                                                    move_pkt = await Mahir_Room_Site_Change(self.current_room_id, self.bot_uid, 2, 1, self.key, self.iv)
                                                    if move_pkt:
                                                        self.online_writer.write(move_pkt); await self.online_writer.drain()
                                                        self.is_in_side2 = True; await asyncio.sleep(0.2)
                                                c_code = room_info.get('36', {}).get('data') or room_info.get('40', {}).get('data')
                                                if self.current_room_id and c_code:
                                                    asyncio.create_task(self.Auto_Room_Welcome(self.current_room_id, c_code, uid_str, user_name=p_name))
                                                self.room_members.add(uid_str)
                                                console.print(f"[bold cyan][{self.uid}][/bold cyan] [bold green]➜ Joined:[/bold green] {p_name} ({uid_str})")

                                    if cmd_type == 65:
                                        is_full = f5.get('1', {}).get('data')
                                        if is_full == 1 and self.current_room_id:
                                            console.print(f"[bold red]!!! ROOM FULL ({self.current_room_id}) !!![/bold red]")
                                            start_pkt = await Mahir_Room_START(self.current_room_id, self.key, self.iv)
                                            if start_pkt:
                                                self.online_writer.write(start_pkt); await self.online_writer.drain()
                                                await asyncio.sleep(1.5)
                                                exit_pkt = await Mahir_Room_ExiT(self.bot_uid, self.key, self.iv)
                                                if exit_pkt:
                                                    self.online_writer.write(exit_pkt); await self.online_writer.drain()
                                                    self.room_members.clear(); self.is_in_side2 = False
                                                    await asyncio.sleep(0.5)
                                                    self.online_writer.write(self.room_pkt); await self.online_writer.drain()
                                                    console.print(f"[bold cyan][{self.uid}][/bold cyan] [bold green]New Room.[/bold green]")
                                    if cmd_type == 7:
                                        self.room_members.clear()
                                        if self.is_in_side2 and self.current_room_id:
                                            await asyncio.sleep(0.3)
                                            back_pkt = await Mahir_Room_Site_Change(self.current_room_id, self.bot_uid, 1, 0, self.key, self.iv)
                                            if back_pkt:
                                                self.online_writer.write(back_pkt); await self.online_writer.drain()
                                                self.is_in_side2 = False
                                except Exception: pass
                    except asyncio.TimeoutError: continue
                    except Exception: break
            except Exception:
                self.is_online = False
                update_active_account(self.uid, room_id='Pending...', room_name='Pending...')
            await asyncio.sleep(10)

    # ---------- COMMAND HANDLER ----------
    async def _execute_command(self, cmd, cmd_name, chat_id, sender_uid):
        ctype = cmd.get("type", "message")
        try:
            if ctype == "message":
                resp = cmd.get("response", "")
                # Optional placeholder replace
                resp = resp.replace("{user_name}", str(sender_uid))
                pkt = await MAHIR_SEnd_RoOm_MsG(chat_id, resp, self.bot_uid, self.key, self.iv)
                if pkt:
                    self.chat_writer.write(pkt); await self.chat_writer.drain()

            elif ctype == "start_room":
                if self.current_room_id and self.online_writer:
                    st_pkt = await Mahir_Room_START(self.current_room_id, self.key, self.iv)
                    if st_pkt:
                        self.online_writer.write(st_pkt); await self.online_writer.drain()
                        await asyncio.sleep(1.0)
                        ex_pkt = await Mahir_Room_ExiT(self.bot_uid, self.key, self.iv)
                        if ex_pkt:
                            self.online_writer.write(ex_pkt); await self.online_writer.drain()
                            self.room_members.clear(); self.is_in_side2 = False
                            await asyncio.sleep(0.5)
                            if hasattr(self, 'room_pkt') and self.room_pkt:
                                self.online_writer.write(self.room_pkt); await self.online_writer.drain()

            elif ctype == "share":
                share_name = cmd.get("share_name", "map")
                # Optionally send a message first
                resp = cmd.get("response", "")
                if resp:
                    pkt = await MAHIR_SEnd_RoOm_MsG(chat_id, resp, self.bot_uid, self.key, self.iv)
                    if pkt:
                        self.chat_writer.write(pkt); await self.chat_writer.drain()
                        await asyncio.sleep(0.2)
                await self.send_share(chat_id, share_name)

            elif ctype == "welcome":
                # Resend welcome message in this room
                if self.current_room_id:
                    with web_config_lock:
                        welcome_template = web_config.get("welcome_msg", DEFAULT_WELCOME_MSG)
                    msg = welcome_template.replace("{user_name}", str(sender_uid))
                    pkt = await MAHIR_SEnd_RoOm_MsG(self.current_room_id, msg, self.bot_uid, self.key, self.iv)
                    if pkt:
                        self.chat_writer.write(pkt); await self.chat_writer.drain()
        except Exception as e:
            console.print(f"[bold red]Cmd '{cmd_name}' err: {e}[/bold red]")

    def _match_command(self, trigger, match_mode, msg_text):
        t = trigger.lower()
        m = msg_text.lower()
        if match_mode == "exact": return m == t
        if match_mode == "startswith": return m.startswith(t)
        return t in m

    # ---------- TCP CHAT ----------
    async def tcp_chat(self, ip, port, auth_token, key, iv, ready_event):
        while self.is_running:
            try:
                reader, writer = await asyncio.open_connection(ip, int(port))
                writer.write(bytes.fromhex(auth_token)); await writer.drain()
                self.chat_reader = reader; self.chat_writer = writer
                ready_event.set()
                console.print(f"[bold cyan]ℹ [{self.uid}] CHAT Connected ✅[/bold cyan]")

                while self.is_running:
                    try:
                        data = await asyncio.wait_for(self.chat_reader.read(4096), timeout=5.0)
                        if not data: break
                        data_hex = data.hex()
                        if data_hex.startswith("1200"):
                            decoded = DeCode_PackEt(data_hex[10:])
                            if decoded:
                                try:
                                    packet_json = json.loads(decoded)
                                    f5 = packet_json.get('5', {}).get('data', {})
                                    msg_text = str(f5.get('4', {}).get('data', "")).strip()
                                    chat_id = f5.get('2', {}).get('data')
                                    sender_uid = f5.get('1', {}).get('data')
                                    if str(sender_uid) == str(self.bot_uid): continue

                                    with web_config_lock:
                                        cmds = dict(web_config.get("commands", {}))

                                    for trigger, cmd in cmds.items():
                                        if not cmd.get("enabled", True): continue
                                        match_mode = cmd.get("match", "contains")
                                        if self._match_command(trigger, match_mode, msg_text):
                                            asyncio.create_task(self._execute_command(cmd, trigger, chat_id, sender_uid))
                                            break
                                except Exception: pass
                    except asyncio.TimeoutError: continue
                    except Exception: break
            except Exception: pass
            await asyncio.sleep(10)

    # ---------- MAIN ----------
    async def keep_online_forever(self):
        global online_count
        while self.is_running:
            try:
                open_id, access_token = await GeNeRaTeAccAccess(self.uid, self.password)
                if not open_id:
                    update_bot_info(self.uid, status="❌ Auth Failed", room_active=False)
                    await asyncio.sleep(10); continue

                payload = await EncRypTMajoRLoGin(open_id, access_token, version)
                response = await MajorLogin(payload)
                if not response:
                    update_bot_info(self.uid, status="❌ Login Failed", room_active=False)
                    await asyncio.sleep(10); continue

                try: auth_data = await DecRypTMajoRLoGin(response)
                except: 
                    update_bot_info(self.uid, status="❌ Decrypt Failed", room_active=False)
                    await asyncio.sleep(10); continue

                if not getattr(auth_data, 'token', None) or not getattr(auth_data, 'url', None):
                    update_bot_info(self.uid, status="❌ Empty Auth", room_active=False)
                    await asyncio.sleep(10); continue

                login_data = await GetLoginData(auth_data.url, payload, auth_data.token)
                if not login_data:
                    update_bot_info(self.uid, status="❌ Data Failed", room_active=False)
                    await asyncio.sleep(10); continue

                port_data = PorTs_pb2.GetLoginData()
                port_data.ParseFromString(login_data)
                self.key = auth_data.key; self.iv = auth_data.iv
                self.region = auth_data.region; self.bot_uid = auth_data.account_uid

                extracted_name = extract_player_name(login_data)
                if extracted_name and len(extracted_name) < 60:
                    self.Nm = extracted_name
                else:
                    try:
                        dec_jwt = jwt.decode(auth_data.token, options={"verify_signature": False})
                        fallback = dec_jwt.get('nickname')
                        if fallback and len(str(fallback)) < 30 and not str(fallback).startswith("0OuCe") and not str(fallback).startswith("eyJ"):
                            self.Nm = str(fallback)
                        else:
                            self.Nm = f"Player_{str(auth_data.account_uid)[-4:]}"
                    except: self.Nm = f"Player_{str(auth_data.account_uid)[-4:]}"

                update_bot_info(self.uid, account_uid=str(auth_data.account_uid))

                online_ip, online_port = port_data.Online_IP_Port.split(":")
                chat_ip, chat_port = port_data.AccountIP_Port.split(":")

                online_auth_token = create_auth_token_online(auth_data.account_uid, auth_data.token, auth_data.timestamp, auth_data.key, auth_data.iv)
                chat_auth_token = create_auth_token_chat(auth_data.account_uid, auth_data.token, auth_data.timestamp, auth_data.key, auth_data.iv)

                if not online_auth_token or not chat_auth_token:
                    update_bot_info(self.uid, status="❌ Token Failed", room_active=False)
                    await asyncio.sleep(10); continue

                console.print(f"[bold green]✔ BoT OnLiNe: {self.Nm} | ChaT: {chat_ip}:{chat_port} | OnLiNe: {online_ip}:{online_port}[/bold green]")

                with active_lock:
                    if not any(a['uid'] == self.uid for a in active_accounts):
                        online_count += 1
                        active_accounts.append({
                            'uid': self.uid, 'bot_uid': str(auth_data.account_uid), 'name': self.Nm,
                            'region': self.region or 'BD', 'time': datetime.now().strftime('%H:%M:%S'),
                            'room_id': 'Pending...', 'room_name': 'Pending...'})

                update_bot_info(self.uid, status="✅ Online", account_uid=str(auth_data.account_uid), room_active=True)

                ready = asyncio.Event()
                t1 = asyncio.create_task(self.tcp_chat(chat_ip, chat_port, chat_auth_token, auth_data.key, auth_data.iv, ready))
                self.tasks.append(t1)
                await ready.wait()
                t2 = asyncio.create_task(self.tcp_online(online_ip, online_port, online_auth_token))
                self.tasks.append(t2)
                await asyncio.gather(t1, t2, return_exceptions=True)
            except Exception as e:
                console.print(f"[bold red]❌ UID {self.uid} Err: {e}[/bold red]")
                update_bot_info(self.uid, status="❌ Error", room_active=False)
            remove_active_account(self.uid)
            await asyncio.sleep(10)

# ================================================================
#   WEB SERVER
# ================================================================
class BotHandler(BaseHTTPRequestHandler):
    def _json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def _text_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(data if isinstance(data, bytes) else data.encode('utf-8'))

    def _read_body(self):
        try:
            cl = int(self.headers.get('Content-Length', 0))
            return self.rfile.read(cl).decode('utf-8')
        except Exception:
            return ""

    def _html_escape(self, s):
        return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            try:
                with open('accs.json', 'r', encoding='utf-8') as f: accs_content = f.read()
            except: accs_content = "{}"
            cur_ver = version or "loading..."
            cur_rel = ob or "loading..."
            with active_lock:
                cur_online = online_count; cur_total = total_accounts; cur_threads = len(active_accounts)
            with web_config_lock:
                rc_enabled = list(web_config.get("enabled_modes", []))
                rc_template = web_config.get("room_name_template", "")
                rc_use = web_config.get("use_mode", "all")
                rc_welcome = web_config.get("welcome_msg", DEFAULT_WELCOME_MSG)
                rc_welcome_shares = list(web_config.get("welcome_shares", ["map"]))
                all_share_names = list(web_config.get("share_packets", {}).keys())
                all_command_triggers = list(web_config.get("commands", {}).keys())
                all_room_modes = list(web_config.get("room_modes", {}).keys())

            mode_checkboxes = ""
            for mode_name in DEFAULT_ROOM_MODES.keys():
                checked = "checked" if mode_name in rc_enabled else ""
                mode_checkboxes += f'<label class="mode-chip"><input type="checkbox" name="enabled_modes" value="{mode_name}" {checked}><span>{mode_name}</span></label>'

            share_checkboxes = ""
            for sh in all_share_names:
                checked = "checked" if sh in rc_welcome_shares else ""
                share_checkboxes += f'<label class="mode-chip"><input type="checkbox" name="welcome_shares" value="{sh}" {checked}><span>{sh}</span></label>'

            mode_options = "".join(f'<option value="{m}">{m}</option>' for m in all_room_modes)
            share_options = "".join(f'<option value="{s}">{s}</option>' for s in all_share_names)
            command_options = "".join(f'<option value="{self._html_escape(c)}">{self._html_escape(c)}</option>' for c in all_command_triggers)

            accs_esc = self._html_escape(accs_content)
            welcome_esc = self._html_escape(rc_welcome)
            template_esc = self._html_escape(rc_template)

            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MAHIR ROOM BOT</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; font-family:'Rajdhani',sans-serif; }}
body {{ background:#030712; color:#f3f4f6; min-height:100vh; padding:20px; background-image: radial-gradient(at 0% 0%, rgba(239,68,68,0.15) 0px, transparent 50%), radial-gradient(at 100% 100%, rgba(59,130,246,0.15) 0px, transparent 50%); background-attachment:fixed; }}
.container {{ max-width:1500px; margin:0 auto; }}
.header {{ text-align:center; padding:30px; background:rgba(17,24,39,0.7); backdrop-filter:blur(16px); border:1px solid rgba(255,255,255,0.1); border-radius:20px; margin-bottom:25px; position:relative; overflow:hidden; }}
.header::before {{ content:''; position:absolute; top:0; left:-100%; width:100%; height:2px; background:linear-gradient(90deg,transparent,#ef4444,#3b82f6,transparent); animation:bar 3s linear infinite; }}
@keyframes bar {{ 0%{{left:-100%}} 100%{{left:100%}} }}
.header h1 {{ font-family:'Orbitron',sans-serif; font-size:2.8em; font-weight:900; letter-spacing:4px; background:linear-gradient(135deg,#fff,#ff4b4b 50%,#ff8533); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
.header p {{ margin-top:8px; font-size:1.1em; color:#9ca3af; letter-spacing:2px; font-weight:600; }}
.stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:20px; margin-bottom:25px; }}
.stat-card {{ background:rgba(17,24,39,0.6); border:1px solid rgba(255,255,255,0.08); border-radius:18px; padding:20px; text-align:center; }}
.stat-card h2 {{ font-family:'Orbitron',sans-serif; font-size:2.5em; color:#10b981; }}
.stat-card p {{ margin-top:5px; font-size:1em; color:#9ca3af; font-weight:700; letter-spacing:1px; }}
.section {{ background:rgba(17,24,39,0.6); border:1px solid rgba(255,255,255,0.08); border-radius:18px; padding:25px; margin-bottom:25px; }}
.section-header {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:18px; flex-wrap:wrap; gap:10px; }}
.section h2 {{ font-family:'Orbitron',sans-serif; color:#38bdf8; font-size:1.3em; letter-spacing:1.5px; }}
.section h3 {{ font-family:'Orbitron',sans-serif; color:#a855f7; font-size:1.05em; margin-bottom:12px; }}
.live-indicator {{ display:inline-flex; align-items:center; gap:6px; background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); padding:4px 12px; border-radius:20px; font-size:0.85em; color:#10b981; font-weight:700; }}
.pulse-dot {{ width:8px; height:8px; background:#10b981; border-radius:50%; box-shadow:0 0 8px #10b981; animation:pulse 1.5s infinite; }}
@keyframes pulse {{ 0%{{transform:scale(0.95)}} 70%{{transform:scale(1)}} 100%{{transform:scale(0.95)}} }}
.table-wrapper {{ overflow-x:auto; max-height:500px; overflow-y:auto; border-radius:10px; border:1px solid rgba(255,255,255,0.05); }}
table {{ width:100%; border-collapse:collapse; text-align:left; }}
th,td {{ padding:14px 16px; border-bottom:1px solid rgba(255,255,255,0.05); font-size:1.05em; white-space:nowrap; }}
th {{ background:rgba(31,41,55,0.9); color:#f3f4f6; position:sticky; top:0; }}
.badge-online {{ background:rgba(16,185,129,0.15); color:#10b981; padding:4px 10px; border-radius:6px; font-weight:700; border:1px solid rgba(16,185,129,0.3); }}
.copy-btn {{ background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.4); padding:5px 12px; border-radius:8px; font-weight:700; cursor:pointer; margin-left:8px; }}
.copy-btn.copied {{ background:rgba(16,185,129,0.3); color:#10b981; }}
.copy-all-btn {{ background:linear-gradient(135deg,#3b82f6,#1d4ed8); color:#fff; border:none; padding:10px 20px; border-radius:10px; font-weight:700; cursor:pointer; letter-spacing:1px; }}
textarea {{ width:100%; background:rgba(15,23,42,0.8); color:#38bdf8; border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:15px; font-family:'Courier New',monospace; font-size:14px; resize:vertical; outline:none; }}
textarea:focus {{ border-color:#38bdf8; box-shadow:0 0 15px rgba(56,189,248,0.3); }}
.btn {{ padding:14px 32px; background:linear-gradient(135deg,#ef4444,#dc2626); color:#fff; border:none; border-radius:10px; font-size:1.05em; font-weight:700; cursor:pointer; margin-top:15px; letter-spacing:1px; }}
.btn:disabled {{ opacity:0.6; cursor:not-allowed; }}
.btn-green {{ background:linear-gradient(135deg,#10b981,#059669); }}
.btn-purple {{ background:linear-gradient(135deg,#a855f7,#7c3aed); }}
.btn-cyan {{ background:linear-gradient(135deg,#06b6d4,#0891b2); }}
.btn-red {{ background:linear-gradient(135deg,#ef4444,#dc2626); }}
.btn-gray {{ background:linear-gradient(135deg,#6b7280,#4b5563); padding:8px 16px; font-size:0.9em; margin:0; }}
.footer {{ text-align:center; padding:20px; color:#6b7280; font-weight:600; }}
#toast {{ visibility:hidden; min-width:250px; background:#10b981; color:#fff; text-align:center; border-radius:8px; padding:14px; position:fixed; z-index:99; right:30px; bottom:30px; font-weight:bold; opacity:0; transition:opacity 0.3s,bottom 0.3s; }}
#toast.show {{ visibility:visible; opacity:1; bottom:40px; }}
.config-grid {{ display:grid; gap:20px; }}
.config-label {{ color:#9ca3af; font-weight:700; letter-spacing:1px; margin-bottom:8px; }}
.mode-chips {{ display:flex; flex-wrap:wrap; gap:10px; }}
.mode-chip {{ display:inline-flex; align-items:center; gap:8px; background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.3); padding:8px 16px; border-radius:10px; cursor:pointer; }}
.mode-chip input {{ width:16px; height:16px; accent-color:#38bdf8; }}
.mode-chip span {{ font-weight:700; color:#cbd5e1; }}
.mode-chip input:checked ~ span {{ color:#38bdf8; }}
.input-text {{ width:100%; padding:12px 16px; background:rgba(15,23,42,0.8); color:#38bdf8; border:1px solid rgba(255,255,255,0.1); border-radius:10px; font-family:'Courier New',monospace; font-size:15px; outline:none; }}
.input-text:focus {{ border-color:#38bdf8; }}
.radio-row {{ display:flex; gap:20px; flex-wrap:wrap; }}
.radio-chip {{ display:inline-flex; align-items:center; gap:8px; background:rgba(168,85,247,0.08); border:1px solid rgba(168,85,247,0.3); padding:10px 20px; border-radius:10px; cursor:pointer; }}
.radio-chip input {{ width:16px; height:16px; accent-color:#a855f7; }}
.radio-chip span {{ font-weight:700; color:#cbd5e1; }}
.radio-chip input:checked ~ span {{ color:#a855f7; }}
.help-text {{ color:#6b7280; font-size:0.85em; margin-top:6px; }}
.tab-btns {{ display:flex; gap:10px; margin-bottom:20px; flex-wrap:wrap; }}
.tab-btn {{ padding:10px 20px; background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.3); border-radius:10px; color:#cbd5e1; font-weight:700; cursor:pointer; }}
.tab-btn.active {{ background:linear-gradient(135deg,#3b82f6,#1d4ed8); color:#fff; border-color:#3b82f6; }}
.tab-content {{ display:none; }} .tab-content.active {{ display:block; }}
.list-row {{ display:flex; gap:10px; align-items:center; margin-bottom:10px; padding:12px; background:rgba(15,23,42,0.6); border:1px solid rgba(255,255,255,0.08); border-radius:10px; }}
.list-row span.name {{ flex:1; font-weight:700; color:#a78bfa; font-family:'Courier New',monospace; }}
.list-row button {{ padding:6px 12px; border:none; border-radius:6px; font-weight:700; cursor:pointer; font-size:0.85em; }}
.add-row {{ display:flex; gap:10px; margin-top:10px; }}
.add-row input {{ flex:1; padding:10px 14px; background:rgba(15,23,42,0.8); color:#a78bfa; border:1px solid rgba(168,85,247,0.3); border-radius:8px; font-family:'Courier New',monospace; outline:none; }}
.mode-select {{ padding:10px 16px; background:rgba(15,23,42,0.9); color:#a78bfa; border:1px solid rgba(168,85,247,0.4); border-radius:10px; font-weight:700; cursor:pointer; }}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>🔥 MAHIR ROOM BOT 🔥</h1><p>⚡ FULLY WEB-CONFIGURABLE SYSTEM ⚡</p></div>

<div class="stats">
<div class="stat-card"><h2 id="stat-online">{cur_online}</h2><p>🟢 ONLINE</p></div>
<div class="stat-card"><h2 id="stat-total">{cur_total}</h2><p>📊 TOTAL</p></div>
<div class="stat-card"><h2 id="stat-threads">{cur_threads}</h2><p>⚙️ THREADS</p></div>
<div class="stat-card"><h2 id="stat-version" style="font-size:1.8em;color:#38bdf8;">{cur_ver}</h2><p>📦 VERSION ({cur_rel})</p></div>
</div>

<!-- CONFIG TABS -->
<div class="section">
<div class="section-header"><h2>⚙️ Bot Configuration</h2><div class="live-indicator"><div class="pulse-dot"></div> LIVE</div></div>
<div class="tab-btns">
<button class="tab-btn active" onclick="switchTab(event,'tab-room')">🎮 Room Config</button>
<button class="tab-btn" onclick="switchTab(event,'tab-welcome')">💬 Welcome</button>
<button class="tab-btn" onclick="switchTab(event,'tab-shares')">📤 Shares</button>
<button class="tab-btn" onclick="switchTab(event,'tab-packets')">📦 Room Packets</button>
<button class="tab-btn" onclick="switchTab(event,'tab-commands')">⚡ Commands</button>
<button class="tab-btn" onclick="switchTab(event,'tab-accounts')">👥 Accounts</button>
</div>

<!-- TAB 1: Room Config -->
<div id="tab-room" class="tab-content active">
<form id="room-form" onsubmit="saveRoomConfig(event)">
<div class="config-grid">
<div>
<div class="config-label">🎮 Enabled Room Modes</div>
<div class="mode-chips">{mode_checkboxes}</div>
</div>
<div>
<div class="config-label">📝 Room Name Template</div>
<input type="text" class="input-text" id="room_name_template" value="{template_esc}" placeholder="[B]➥{{color}}ᎷAH!Ꮢ">
<div class="help-text">💡 Use <b>{{color}}</b> for random color.</div>
</div>
<div>
<div class="config-label">🎯 Selection Mode</div>
<div class="radio-row">
<label class="radio-chip"><input type="radio" name="use_mode" value="all" {"checked" if rc_use=="all" else ""}><span>🔵 ALL</span></label>
<label class="radio-chip"><input type="radio" name="use_mode" value="half" {"checked" if rc_use=="half" else ""}><span>🟣 HALF (random subset)</span></label>
</div>
</div>
<div>
<div class="config-label">📤 Auto-send Shares after Welcome</div>
<div class="mode-chips">{share_checkboxes}</div>
<div class="help-text">✅ Shares to auto-send when a player joins.</div>
</div>
<button type="submit" class="btn btn-green" id="room-save-btn">💾 SAVE ROOM CONFIG</button>
</div>
</form>
</div>

<!-- TAB 2: Welcome Message -->
<div id="tab-welcome" class="tab-content">
<h3>💬 Welcome Message</h3>
<textarea id="welcome_msg_ta" style="height:280px; color:#facc15;" spellcheck="false">{welcome_esc}</textarea>
<div class="help-text">
💡 Placeholder: <b>{{user_name}}</b> → player name.<br>
📝 Use real newlines. Color codes: <b>[C][FF0000]</b> etc.
</div>
<button class="btn btn-cyan" id="welcome-save-btn" onclick="saveWelcomeMsg()">💾 SAVE WELCOME</button>
</div>

<!-- TAB 3: Share Packets -->
<div id="tab-shares" class="tab-content">
<h3>📤 Share Packet Manager</h3>
<div class="config-label">Existing Shares:</div>
<div id="shares-list"></div>
<div class="add-row">
<input type="text" id="new_share_name" placeholder="new share name (e.g. custom1)">
<button class="btn btn-purple" style="margin-top:0;" onclick="addNewShare()">➕ ADD NEW SHARE</button>
</div>
<hr style="margin:20px 0; border-color:rgba(255,255,255,0.1);">
<div class="config-label">Edit Share:</div>
<select id="share_selector" class="mode-select" onchange="loadSelectedShare()"></select>
<div style="margin-top:15px;">
<label class="config-label">Enabled: <input type="checkbox" id="share_enabled" style="width:auto; accent-color:#38bdf8;"></label>
</div>
<div class="config-label" style="margin-top:10px;">share_json (raw JSON string):</div>
<textarea id="share_json_ta" style="height:80px;" spellcheck="false"></textarea>
<div class="config-label" style="margin-top:10px;">Fields (JSON, bytes as {{"__hex__":"..."}}):</div>
<textarea id="share_fields_ta" style="height:300px; color:#a78bfa;" spellcheck="false"></textarea>
<div class="help-text">Placeholders: <b>{{bot_uid}}</b>, <b>{{target_id}}</b>, <b>{{timestamp}}</b>, <b>{{share_json}}</b></div>
<button class="btn btn-purple" id="share-save-btn" onclick="saveShare()">💾 SAVE SHARE</button>
<button class="btn btn-red" style="margin-left:10px;" onclick="deleteShare()">🗑️ DELETE SHARE</button>
</div>

<!-- TAB 4: Room Packets -->
<div id="tab-packets" class="tab-content">
<h3>📦 Room Packet Manager</h3>
<div class="config-label">Existing Room Modes:</div>
<div id="modes-list"></div>
<div class="add-row">
<input type="text" id="new_mode_name" placeholder="new mode name (e.g. MyRoom1v1)">
<button class="btn btn-purple" style="margin-top:0;" onclick="addNewMode()">➕ ADD NEW MODE</button>
</div>
<hr style="margin:20px 0; border-color:rgba(255,255,255,0.1);">
<div class="config-label">Edit Mode:</div>
<select id="mode_selector" class="mode-select" onchange="loadSelectedMode()"></select>
<div class="config-label" style="margin-top:15px;">JSON Fields (bytes as {{"__hex__":"..."}}):</div>
<textarea id="packet_ta" style="height:400px; color:#a78bfa;" spellcheck="false"></textarea>
<div class="help-text">Placeholder: <b>{{room_name}}</b> for room name. Bytes → {{"__hex__":"0107..."}}.</div>
<button class="btn btn-purple" id="packet-save-btn" onclick="saveMode()">💾 SAVE MODE</button>
<button class="btn btn-red" style="margin-left:10px;" onclick="deleteMode()">🗑️ DELETE MODE</button>
</div>

<!-- TAB 5: Commands -->
<div id="tab-commands" class="tab-content">
<h3>⚡ Chat Command Manager</h3>
<div class="config-label">Existing Commands:</div>
<div id="commands-list"></div>
<div class="add-row">
<input type="text" id="new_command_name" placeholder="new trigger (e.g. /help)">
<button class="btn btn-purple" style="margin-top:0;" onclick="addNewCommand()">➕ ADD NEW COMMAND</button>
</div>
<hr style="margin:20px 0; border-color:rgba(255,255,255,0.1);">
<div class="config-label">Edit Command:</div>
<select id="command_selector" class="mode-select" onchange="loadSelectedCommand()"></select>
<div style="margin-top:15px;">
<label class="config-label"><input type="checkbox" id="cmd_enabled" style="width:auto; accent-color:#38bdf8;"> Enabled</label>
</div>
<div class="config-label" style="margin-top:10px;">Match Mode:</div>
<select id="cmd_match" class="mode-select">
<option value="exact">exact (must match whole message)</option>
<option value="contains">contains (anywhere in message)</option>
<option value="startswith">startswith (message starts with trigger)</option>
</select>
<div class="config-label" style="margin-top:10px;">Type:</div>
<select id="cmd_type" class="mode-select" onchange="updateCommandFields()">
<option value="message">💬 message (send chat response)</option>
<option value="start_room">🚀 start_room (reset & new room)</option>
<option value="share">📤 share (send share packet)</option>
<option value="welcome">🎉 welcome (resend welcome msg)</option>
</select>
<div id="cmd_share_row" style="display:none; margin-top:10px;">
<div class="config-label">Share Name:</div>
<select id="cmd_share_name" class="mode-select">{share_options}</select>
</div>
<div id="cmd_response_row" style="margin-top:10px;">
<div class="config-label">Response Message:</div>
<textarea id="cmd_response_ta" style="height:200px; color:#facc15;" spellcheck="false"></textarea>
<div class="help-text">Placeholder: <b>{{user_name}}</b> = sender's UID (or name if available)</div>
</div>
<button class="btn btn-purple" id="cmd-save-btn" onclick="saveCommand()">💾 SAVE COMMAND</button>
<button class="btn btn-red" style="margin-left:10px;" onclick="deleteCommand()">🗑️ DELETE COMMAND</button>
</div>

<!-- TAB 6: Accounts (accs.json) -->
<div id="tab-accounts" class="tab-content">
<h3>👥 Account Manager (accs.json)</h3>
<div class="help-text" style="margin-bottom:12px;">
💡 Format: <b>{{"UID": "PASSWORD"}}</b> — JSON format maintain করুন।<br>
⚠️ Save করলে নতুন account auto-launch হবে।
</div>
<form id="update-form" onsubmit="submitForm(event)">
<textarea id="bd_content" style="height:400px; color:#38bdf8;" placeholder='{{"12345678": "password"}}' spellcheck="false">{accs_esc}</textarea>
<br>
<button type="submit" class="btn" id="save-btn">💾 SAVE & START ACCOUNTS</button>
</form>
</div>

</div>

<!-- ACTIVE ACCOUNTS -->
<div class="section">
<div class="section-header">
<h2>📋 Active Accounts</h2>
<button class="copy-all-btn" onclick="copyAllRoomIds()">📋 Copy All Room IDs</button>
<div class="live-indicator"><div class="pulse-dot"></div> LIVE</div>
</div>
<div class="table-wrapper">
<table>
<thead><tr>
<th>BOT UID</th><th>UID</th><th>NAME</th><th>REGION</th>
<th>ROOM ID</th><th>ROOM NAME</th><th>TIME</th><th>STATUS</th>
</tr></thead>
<tbody id="accounts-tbody"><tr><td colspan="8">🔄 Loading...</td></tr></tbody>
</table>
</div>
</div>

<div class="footer"><p>© 2026 MAHIR BOT | Web-Configurable System</p></div>
</div>
<div id="toast"></div>

<script>
let allShares = {{}};
let allCommands = {{}};
let allModes = {{}};

/* ===== Tabs ===== */
function switchTab(e, tabId) {{
document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
document.getElementById(tabId).classList.add('active');
e.currentTarget.classList.add('active');
}}

/* ===== Toast ===== */
function showToast(msg, color) {{
const t = document.getElementById('toast');
t.innerText = msg;
t.style.background = color || '#10b981';
t.className = 'show';
setTimeout(() => {{ t.className = t.className.replace('show', ''); }}, 3000);
}}

/* ===== Stats ===== */
async function fetchStats() {{
try {{
const res = await fetch('/api/stats');
if (!res.ok) return;
const data = await res.json();
document.getElementById('stat-online').innerText = data.online;
document.getElementById('stat-total').innerText = data.total;
document.getElementById('stat-threads').innerText = data.threads;
document.getElementById('stat-version').innerText = data.version;
const tbody = document.getElementById('accounts-tbody');
if (data.accounts && data.accounts.length > 0) {{
let html = '';
data.accounts.forEach(acc => {{
const rid = acc.room_id || 'Pending...';
const rname = acc.room_name || 'Pending...';
const ridStyle = (rid !== 'Pending...') ? 'color:#facc15;font-weight:bold;' : 'color:#6b7280;';
const rnameStyle = (rname !== 'Pending...') ? 'color:#a78bfa;font-weight:bold;' : 'color:#6b7280;';
const isReady = (rid !== 'Pending...') && (rid !== 'None') && (rid !== 'N/A');
const cb = isReady ? `<button class="copy-btn" onclick="copyRoomId('${{rid}}',this)">📋</button>` : '';
html += `<tr><td>${{acc.bot_uid}}</td><td>${{acc.uid}}</td>
<td style="color:#38bdf8;font-weight:bold;">${{acc.name}}</td>
<td style="color:#f59e0b;font-weight:bold;">${{acc.region}}</td>
<td style="${{ridStyle}}">${{rid}}${{cb}}</td>
<td style="${{rnameStyle}}">${{rname}}</td>
<td>${{acc.time}}</td>
<td><span class="badge-online">● ONLINE</span></td></tr>`;
}});
tbody.innerHTML = html;
}} else {{
tbody.innerHTML = '<tr><td colspan="8">⚠️ No active accounts.</td></tr>';
}}
}} catch (e) {{ console.error(e); }}
}}

function copyRoomId(rid, el) {{
navigator.clipboard.writeText(rid).then(() => {{
el.innerText = '✅'; el.classList.add('copied');
showToast('📋 Copied: ' + rid);
setTimeout(() => {{ el.innerText = '📋'; el.classList.remove('copied'); }}, 1500);
}});
}}

async function copyAllRoomIds() {{
const res = await fetch('/api/stats'); const d = await res.json();
const ids = (d.accounts||[]).map(a => a.room_id).filter(id => id && id !== 'Pending...' && id !== 'None' && id !== 'N/A');
if (!ids.length) return showToast('⚠️ No Room IDs', '#ef4444');
navigator.clipboard.writeText(ids.join('\\n'));
showToast('📋 Copied ' + ids.length + ' IDs');
}}

/* ===== Room Config ===== */
async function saveRoomConfig(e) {{
e.preventDefault();
const btn = document.getElementById('room-save-btn');
btn.innerText = '⏳...'; btn.disabled = true;
const form = document.getElementById('room-form');
const modes = Array.from(form.querySelectorAll('input[name="enabled_modes"]:checked')).map(c => c.value);
const shares = Array.from(form.querySelectorAll('input[name="welcome_shares"]:checked')).map(c => c.value);
if (!modes.length) {{ showToast('⚠️ Select a mode!', '#ef4444'); btn.disabled = false; btn.innerText = '💾 SAVE ROOM CONFIG'; return; }}
const template = document.getElementById('room_name_template').value || '[B]➥{{color}}ᎷAH!Ꮢ';
const useMode = form.querySelector('input[name="use_mode"]:checked').value;
const body = new URLSearchParams();
body.append('enabled_modes', modes.join(','));
body.append('room_name_template', template);
body.append('use_mode', useMode);
body.append('welcome_shares', shares.join(','));
const res = await fetch('/save_room_config', {{method:'POST', headers:{{'Content-Type':'application/x-www-form-urlencoded'}}, body: body.toString()}});
if (res.ok) showToast('⚙️ Saved!'); else showToast('❌ Failed', '#ef4444');
btn.innerText = '💾 SAVE ROOM CONFIG'; btn.disabled = false;
}}

/* ===== Welcome ===== */
async function saveWelcomeMsg() {{
const btn = document.getElementById('welcome-save-btn');
btn.innerText = '⏳...'; btn.disabled = true;
const msg = document.getElementById('welcome_msg_ta').value;
const body = new URLSearchParams();
body.append('welcome_msg', msg);
const res = await fetch('/save_welcome_msg', {{method:'POST', headers:{{'Content-Type':'application/x-www-form-urlencoded'}}, body: body.toString()}});
if (res.ok) showToast('💬 Saved!'); else showToast('❌ Failed', '#ef4444');
btn.innerText = '💾 SAVE WELCOME'; btn.disabled = false;
}}

/* ===== SHARES ===== */
async function loadShares() {{
const res = await fetch('/api/share_packets');
allShares = await res.json();
const list = document.getElementById('shares-list');
list.innerHTML = '';
Object.entries(allShares).forEach(([name, cfg]) => {{
const row = document.createElement('div');
row.className = 'list-row';
const enabled = cfg.enabled !== false;
row.innerHTML = `<span class="name">${{enabled ? '✅' : '❌'}} ${{name}}</span>`;
list.appendChild(row);
}});
const sel = document.getElementById('share_selector');
sel.innerHTML = '';
Object.keys(allShares).forEach(n => {{
const opt = document.createElement('option'); opt.value = n; opt.text = n; sel.appendChild(opt);
}});
if (Object.keys(allShares).length) {{
sel.value = Object.keys(allShares)[0];
loadSelectedShare();
}}
}}

function loadSelectedShare() {{
const n = document.getElementById('share_selector').value;
const cfg = allShares[n] || {{}};
document.getElementById('share_enabled').checked = cfg.enabled !== false;
document.getElementById('share_json_ta').value = cfg.share_json || '';
document.getElementById('share_fields_ta').value = JSON.stringify(cfg.fields || {{}}, null, 4);
}}

async function saveShare() {{
const btn = document.getElementById('share-save-btn');
btn.innerText = '⏳...'; btn.disabled = true;
try {{
const n = document.getElementById('share_selector').value;
if (!n) throw new Error('No share selected');
const fields = JSON.parse(document.getElementById('share_fields_ta').value);
const share_json = document.getElementById('share_json_ta').value;
const enabled = document.getElementById('share_enabled').checked;
allShares[n] = {{enabled: enabled, share_json: share_json, fields: fields}};
const res = await fetch('/save_share_packets', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify(allShares)}});
if (res.ok) {{ showToast('📤 Saved: ' + n); await loadShares(); }}
else showToast('❌ Failed', '#ef4444');
}} catch (e) {{ showToast('❌ ' + e.message, '#ef4444'); }}
btn.innerText = '💾 SAVE SHARE'; btn.disabled = false;
}}

async function addNewShare() {{
const name = document.getElementById('new_share_name').value.trim();
if (!name) return showToast('⚠️ Enter name', '#ef4444');
if (allShares[name]) return showToast('⚠️ Already exists', '#ef4444');
allShares[name] = {{enabled: true, share_json: '{{}}', fields: {{}}}};
const res = await fetch('/save_share_packets', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify(allShares)}});
if (res.ok) {{
showToast('➕ Added: ' + name);
document.getElementById('new_share_name').value = '';
await loadShares();
document.getElementById('share_selector').value = name;
loadSelectedShare();
}}
}}

async function deleteShare() {{
const n = document.getElementById('share_selector').value;
if (!n) return;
if (!confirm('Delete share "' + n + '"?')) return;
delete allShares[n];
const res = await fetch('/save_share_packets', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify(allShares)}});
if (res.ok) {{ showToast('🗑️ Deleted'); await loadShares(); }}
}}

/* ===== ROOM MODES ===== */
async function loadModes() {{
const res = await fetch('/api/room_modes');
allModes = await res.json();
const list = document.getElementById('modes-list');
list.innerHTML = '';
Object.keys(allModes).forEach(n => {{
const row = document.createElement('div');
row.className = 'list-row';
row.innerHTML = `<span class="name">${{n}}</span>`;
list.appendChild(row);
}});
const sel = document.getElementById('mode_selector');
sel.innerHTML = '';
Object.keys(allModes).forEach(n => {{
const opt = document.createElement('option'); opt.value = n; opt.text = n; sel.appendChild(opt);
}});
if (Object.keys(allModes).length) {{
sel.value = Object.keys(allModes)[0];
loadSelectedMode();
}}
}}

function loadSelectedMode() {{
const n = document.getElementById('mode_selector').value;
document.getElementById('packet_ta').value = JSON.stringify(allModes[n] || {{}}, null, 4);
}}

async function saveMode() {{
const btn = document.getElementById('packet-save-btn');
btn.innerText = '⏳...'; btn.disabled = true;
try {{
const n = document.getElementById('mode_selector').value;
if (!n) throw new Error('No mode selected');
const fields = JSON.parse(document.getElementById('packet_ta').value);
allModes[n] = fields;
const res = await fetch('/save_room_modes', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify(allModes)}});
if (res.ok) {{ showToast('📦 Saved: ' + n); await loadModes(); }}
else showToast('❌ Failed', '#ef4444');
}} catch (e) {{ showToast('❌ ' + e.message, '#ef4444'); }}
btn.innerText = '💾 SAVE MODE'; btn.disabled = false;
}}

async function addNewMode() {{
const name = document.getElementById('new_mode_name').value.trim();
if (!name) return showToast('⚠️ Enter name', '#ef4444');
if (allModes[name]) return showToast('⚠️ Already exists', '#ef4444');
allModes[name] = {{1: 2, 2: {{1: 1, 2: 15, 3: 0, 4: "{{room_name}}"}}}};
const res = await fetch('/save_room_modes', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify(allModes)}});
if (res.ok) {{
showToast('➕ Added: ' + name);
document.getElementById('new_mode_name').value = '';
await loadModes();
document.getElementById('mode_selector').value = name;
loadSelectedMode();
}}
}}

async function deleteMode() {{
const n = document.getElementById('mode_selector').value;
if (!n) return;
if (!confirm('Delete mode "' + n + '"?')) return;
delete allModes[n];
const res = await fetch('/save_room_modes', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify(allModes)}});
if (res.ok) {{ showToast('🗑️ Deleted'); await loadModes(); }}
}}

/* ===== COMMANDS ===== */
async function loadCommands() {{
const res = await fetch('/api/commands');
allCommands = await res.json();
const list = document.getElementById('commands-list');
list.innerHTML = '';
Object.entries(allCommands).forEach(([name, cfg]) => {{
const row = document.createElement('div');
row.className = 'list-row';
const enabled = cfg.enabled !== false;
const type = cfg.type || 'message';
row.innerHTML = `<span class="name">${{enabled ? '✅' : '❌'}} ${{name}} [${{type}}]</span>`;
list.appendChild(row);
}});
const sel = document.getElementById('command_selector');
sel.innerHTML = '';
Object.keys(allCommands).forEach(n => {{
const opt = document.createElement('option'); opt.value = n; opt.text = n; sel.appendChild(opt);
}});
if (Object.keys(allCommands).length) {{
sel.value = Object.keys(allCommands)[0];
loadSelectedCommand();
}}
}}

function updateCommandFields() {{
const t = document.getElementById('cmd_type').value;
document.getElementById('cmd_response_row').style.display = (t === 'message' || t === 'share' || t === 'welcome') ? 'block' : 'none';
document.getElementById('cmd_share_row').style.display = (t === 'share') ? 'block' : 'none';
}}

function loadSelectedCommand() {{
const n = document.getElementById('command_selector').value;
const cfg = allCommands[n] || {{}};
document.getElementById('cmd_enabled').checked = cfg.enabled !== false;
document.getElementById('cmd_match').value = cfg.match || 'contains';
document.getElementById('cmd_type').value = cfg.type || 'message';
document.getElementById('cmd_response_ta').value = cfg.response || '';
document.getElementById('cmd_share_name').value = cfg.share_name || 'map';
updateCommandFields();
}}

async function saveCommand() {{
const btn = document.getElementById('cmd-save-btn');
btn.innerText = '⏳...'; btn.disabled = true;
try {{
const n = document.getElementById('command_selector').value;
if (!n) throw new Error('No command selected');
const newCfg = {{
enabled: document.getElementById('cmd_enabled').checked,
match: document.getElementById('cmd_match').value,
type: document.getElementById('cmd_type').value,
}};
if (newCfg.type === 'message' || newCfg.type === 'share' || newCfg.type === 'welcome') {{
newCfg.response = document.getElementById('cmd_response_ta').value;
}}
if (newCfg.type === 'share') {{
newCfg.share_name = document.getElementById('cmd_share_name').value;
}}
allCommands[n] = newCfg;
const res = await fetch('/save_commands', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify(allCommands)}});
if (res.ok) {{ showToast('⚡ Saved: ' + n); await loadCommands(); }}
else showToast('❌ Failed', '#ef4444');
}} catch (e) {{ showToast('❌ ' + e.message, '#ef4444'); }}
btn.innerText = '💾 SAVE COMMAND'; btn.disabled = false;
}}

async function addNewCommand() {{
const name = document.getElementById('new_command_name').value.trim();
if (!name) return showToast('⚠️ Enter trigger', '#ef4444');
if (allCommands[name]) return showToast('⚠️ Exists', '#ef4444');
allCommands[name] = {{enabled: true, match: 'contains', type: 'message', response: 'Hello!'}};
const res = await fetch('/save_commands', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify(allCommands)}});
if (res.ok) {{
showToast('➕ Added: ' + name);
document.getElementById('new_command_name').value = '';
await loadCommands();
document.getElementById('command_selector').value = name;
loadSelectedCommand();
}}
}}

async function deleteCommand() {{
const n = document.getElementById('command_selector').value;
if (!n) return;
if (!confirm('Delete "' + n + '"?')) return;
delete allCommands[n];
const res = await fetch('/save_commands', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify(allCommands)}});
if (res.ok) {{ showToast('🗑️ Deleted'); await loadCommands(); }}
}}

/* ===== Accounts JSON ===== */
async function submitForm(e) {{
e.preventDefault();
const btn = document.getElementById('save-btn');
btn.innerText = '⏳...'; btn.disabled = true;
const content = document.getElementById('bd_content').value;
const res = await fetch('/update', {{method:'POST', headers:{{'Content-Type':'application/x-www-form-urlencoded'}}, body: 'bd_content=' + encodeURIComponent(content)}});
if (res.ok) {{ showToast('💾 Saved!'); fetchStats(); }} else showToast('❌ Failed', '#ef4444');
btn.innerText = '💾 SAVE & START ACCOUNTS'; btn.disabled = false;
}}

/* ===== INIT ===== */
fetchStats();
setInterval(fetchStats, 2000);
loadShares();
loadModes();
loadCommands();
</script>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))
            return

        # ===== GET APIs =====
        if self.path == '/api/stats':
            with active_lock:
                accs = list(active_accounts); oc = online_count
            try: total = len(load_accounts())
            except: total = 0
            self._json_response({'online': oc, 'total': total, 'threads': len(accs),
                'version': version or "loading...", 'release': ob or "loading...", 'accounts': accs})
            return

        if self.path == '/api/room_modes':
            with web_config_lock: modes = to_json_safe(web_config.get("room_modes", {}))
            self._json_response(modes); return

        if self.path == '/api/share_packets':
            with web_config_lock: shares = to_json_safe(web_config.get("share_packets", {}))
            self._json_response(shares); return

        if self.path == '/api/commands':
            with web_config_lock: cmds = to_json_safe(web_config.get("commands", {}))
            self._json_response(cmds); return

        if self.path == '/api/room_config':
            with web_config_lock:
                data = {
                    'enabled_modes': list(web_config.get('enabled_modes', [])),
                    'room_name_template': web_config.get('room_name_template', ''),
                    'use_mode': web_config.get('use_mode', 'all'),
                    'welcome_msg': web_config.get('welcome_msg', ''),
                    'welcome_shares': list(web_config.get('welcome_shares', [])),
                }
            self._json_response(data); return

        if self.path == '/status':
            with bot_lock: sc = bot_status.copy()
            accs = load_accounts()
            self._json_response({"total_accs": len(accs), "bots": sc}); return

        if self.path == '/get_accs':
            try:
                with open("accs.json", "r", encoding="utf-8") as f: c = f.read()
            except: c = "{}"
            self._text_response(c); return

        self.send_response(404); self.end_headers()

    def do_POST(self):
        raw = self._read_body()

        if self.path in ('/update', '/save_accs'):
            if self.path == '/update':
                params = parse_qs(raw)
                if 'bd_content' not in params:
                    return self._text_response('No content', 400)
                new_content = params['bd_content'][0]
            else:
                new_content = raw
            try:
                parsed = json.loads(new_content)
                with open("accs.json", "w", encoding="utf-8") as f:
                    json.dump(parsed, f, indent=4)
                console.print("[bold yellow]accs.json updated.[/bold yellow]")
                self._text_response('OK')
            except Exception as e:
                self._text_response(f"Invalid JSON: {e}", 400)
            return

        if self.path == '/save_room_config':
            params = parse_qs(raw)
            modes_raw = params.get('enabled_modes', [''])[0]
            modes = [m.strip() for m in modes_raw.split(',') if m.strip()]
            template = params.get('room_name_template', [''])[0] or "[B]➥{color}ᎷAH!Ꮢ"
            use_mode = params.get('use_mode', ['all'])[0]
            if use_mode not in ('all', 'half'): use_mode = 'all'
            shares_raw = params.get('welcome_shares', [''])[0]
            shares = [s.strip() for s in shares_raw.split(',') if s.strip()]

            with web_config_lock:
                web_config['enabled_modes'] = modes if modes else ["Room1v1", "Room2v2"]
                web_config['room_name_template'] = template
                web_config['use_mode'] = use_mode
                web_config['welcome_shares'] = shares
            save_web_config()
            console.print(f"[bold green]⚙️ Room Config:[/bold green] modes={modes} use={use_mode}")
            self._text_response('OK'); return

        if self.path == '/save_welcome_msg':
            params = parse_qs(raw)
            msg = params.get('welcome_msg', [''])[0] or DEFAULT_WELCOME_MSG
            with web_config_lock: web_config['welcome_msg'] = msg
            save_web_config()
            console.print(f"[bold green]💬 Welcome Msg Updated[/bold green]")
            self._text_response('OK'); return

        if self.path == '/save_room_modes':
            try:
                data = json.loads(raw)
                if not isinstance(data, dict): raise ValueError("Expected dict")
                parsed_modes = {}
                for name, fields in data.items():
                    parsed_modes[name] = from_json_safe(fields)
                if not parsed_modes: raise ValueError("Empty")
                with web_config_lock: web_config['room_modes'] = parsed_modes
                save_web_config()
                console.print(f"[bold green]📦 Room Modes:[/bold green] {list(parsed_modes.keys())}")
                self._text_response('OK')
            except Exception as e:
                self._text_response(f"Invalid: {e}", 400)
            return

        if self.path == '/save_share_packets':
            try:
                data = json.loads(raw)
                if not isinstance(data, dict): raise ValueError("Expected dict")
                parsed = {}
                for name, cfg in data.items():
                    if isinstance(cfg, dict):
                        parsed[name] = from_json_safe(cfg)
                with web_config_lock: web_config['share_packets'] = parsed
                save_web_config()
                console.print(f"[bold green]📤 Share Packets:[/bold green] {list(parsed.keys())}")
                self._text_response('OK')
            except Exception as e:
                self._text_response(f"Invalid: {e}", 400)
            return

        if self.path == '/save_commands':
            try:
                data = json.loads(raw)
                if not isinstance(data, dict): raise ValueError("Expected dict")
                parsed = {}
                for name, cfg in data.items():
                    if isinstance(cfg, dict):
                        parsed[name] = from_json_safe(cfg)
                with web_config_lock: web_config['commands'] = parsed
                save_web_config()
                console.print(f"[bold green]⚡ Commands:[/bold green] {list(parsed.keys())}")
                self._text_response('OK')
            except Exception as e:
                self._text_response(f"Invalid: {e}", 400)
            return

        if self.path == '/reset_room_modes':
            with web_config_lock:
                web_config['room_modes'] = {k: _deep_copy_defaults(v) for k, v in DEFAULT_ROOM_MODES.items()}
            save_web_config()
            self._text_response('OK'); return

        self.send_response(404); self.end_headers()

    def log_message(self, format, *args): pass

def start_web_server():
    port = 8080
    try:
        server = HTTPServer(('0.0.0.0', port), BotHandler)
        console.print(f"[bold green]🌐 Dashboard: http://localhost:{port}[/bold green]")
        webbrowser.open(f'http://localhost:{port}')
        server.serve_forever()
    except OSError:
        console.print(f"[bold red]❌ Port {port} in use.[/bold red]")

async def main_async():
    print(render('MAHIR', colors=['white', 'red'], align='center'))
    load_web_config()
    threading.Thread(target=AuTo_ResTartinG, daemon=True).start()
    threading.Thread(target=start_web_server, daemon=True).start()
    await asyncio.sleep(1)
    asyncio.create_task(batch_account_loader())
    console.print(Panel(
        "[bold green]✅ System Active[/bold green]\n"
        "[cyan]🌐 http://localhost:8080[/cyan]\n"
        "[magenta]⚙️ Room Packets: Web editable[/magenta]\n"
        "[yellow]💬 Welcome: Web editable[/yellow]\n"
        "[blue]📤 Shares: Web editable[/blue]\n"
        "[red]⚡ Commands: Web editable[/red]",
        title="[bold red]🔥 MAHIR SYSTEM 🔥[/bold red]",
        border_style="bright_red", expand=False))
    while True: await asyncio.sleep(3600)

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try: loop.run_until_complete(main_async())
    except KeyboardInterrupt: console.print("\n[bold red]Shutdown.[/bold red]")

if __name__ == "__main__":
    main()