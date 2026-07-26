import requests , os , psutil , sys , jwt , pickle , json , binascii , time , urllib3 , xZRcdx , base64 , datetime , re ,socket , threading , http.client , ssl , gzip , asyncio , gc
from io import BytesIO
from protobuf_decoder.protobuf_decoder import Parser
from M4H1R import *
from datetime import datetime , timedelta
from google.protobuf.timestamp_pb2 import Timestamp
from http.server import HTTPServer, BaseHTTPRequestHandler
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from cfonts import render , say
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
import uuid
import webbrowser
import threading # এটি আপনার অলরেডি আছে, তাও নিশ্চিত হোন
import random
# নিশ্চিত করুন Pb2 ফোল্ডারটি আপনার প্রজেক্টে আছে
from Pb2 import MajoRLoGinrEq_pb2

bot_status = {}
bot_lock = threading.Lock()

console = Console()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

async def Mahir_OpeN_RoOm_ChaT(room_id: int, chat_code: str, key: bytes, iv: bytes):
    """Open room chat using chat_code from server response"""
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
        
        # CrEaTe_ProTo একটি সাধারণ ফাংশন, তাই await বাদ দেওয়া হয়েছে
        proto_bytes = CrEaTe_ProTo(fields)
        packet_hex = proto_bytes.hex()
        
        # EnC_PacKeT একটি সাধারণ ফাংশন, তাই await বাদ দেওয়া হয়েছে
        encrypted_packet = EnC_PacKeT(packet_hex, key, iv)
        packet_length = len(encrypted_packet) // 2
        hex_length = f"{packet_length:04x}"
        
        zeros_needed = 6 - len(hex_length)
        packet_prefix = "121500" + ("0" * zeros_needed)
        
        final_packet_hex = packet_prefix + hex_length + encrypted_packet
        final_packet = bytes.fromhex(final_packet_hex)
        
        return final_packet
        
    except Exception as e:
        print(f"❌ Mahir_OpeN_RoOm_ChaT error: {e}")
        return None

# ============ SEND ROOM MESSAGE ============
async def Mahir_SEnd_RoOm_MsG(room_id: int, message: str, bot_uid: int, key: bytes, iv: bytes):
    """Send message in room chat"""
    try:
        timestamp = int(datetime.now().timestamp())
        # xBunnEr একটি সাধারণ ফাংশন, তাই await বাদ দেওয়া হয়েছে
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
        
        # CrEaTe_ProTo এবং EnC_PacKeT থেকে await বাদ দেওয়া হয়েছে
        proto_bytes = CrEaTe_ProTo(fields)
        packet_hex = proto_bytes.hex()
        encrypted_packet = EnC_PacKeT(packet_hex, key, iv)
        packet_length = len(encrypted_packet) // 2
        hex_length = f"{packet_length:04x}"
        zeros_needed = 6 - len(hex_length)
        packet_prefix = "121500" + ("0" * zeros_needed)
        final_packet_hex = packet_prefix + hex_length + encrypted_packet
        return bytes.fromhex(final_packet_hex)
    except Exception as e:
        print(f"❌ room message error: {e}")
        return None

def G_AccEss(U , P):

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
        R = requests.post(UrL , headers = HE , data = dT, timeout=10)
        if R.status_code == 200: 
            json_data = R.json()
            if 'access_token' in json_data and 'open_id' in json_data:
                return json_data['access_token'] , json_data['open_id']
            else:
                print(f" - Missing token in response: {json_data}")
                return None, None
        else: 
            print(f" - Token request failed: {R.status_code} - {R.text}")
            return None, None
    except Exception as e: 
        print(f" - Error in G_AccEss: {e}")
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
                print(f" - Server Busy (503). Retrying in 10s... (Attempt {attempt+1})")
                time.sleep(10)
                continue
                
            raw_data = response.read()
            if response.getheader('Content-Encoding') == 'gzip':
                with gzip.GzipFile(fileobj=BytesIO(raw_data)) as f:
                    raw_data = f.read()                
            
            return raw_data.hex() if response.status in [200, 201] else None
        except Exception as e:
            print(f" - MajorLoGin Error: {e}")
            time.sleep(5)
        finally:
            try: conn.close()
            except: pass
    return None


Thread(target = AuTo_ResTartinG , daemon = True).start()

class FF_CLient():

    def __init__(self , U , P):  
        self.U = U # UID সেভ করে রাখা
        with bot_lock:
            bot_status[U] = "🔄 Initializing..."
        # বাকি কোড...
        self.empty_count = 0  
        self.reader = None 
        self.writer = None          
        self.U = U
        self.P = P
        try:
            self.Get_FiNal_ToKen_0115(U , P)
        except Exception as e:
            print(f" - Error initializing client for {U}: {e}")

    async def STarT(self , JwT_ToKen , AutH_ToKen , ip , port, ip2 , port2 , key, iv , bot_uid):
        with bot_lock:
            bot_status[self.U] = "✅ Connected & Online"
        R = asyncio.Event()
        task1 = asyncio.create_task(self.ChaT(self.JwT_ToKen , self.AutH_ToKen , ip , port , key , iv , bot_uid, R))  
        await R.wait()
        await asyncio.sleep(0.5)
        task2 = asyncio.create_task(self.OnLinE(self.JwT_ToKen , self.AutH_ToKen , ip2 , port2 , key , iv , bot_uid))
        await asyncio.gather(task1)

    async def sF(self):
        if self.writer:
            try: 
                self.writer.close() 
                await asyncio.sleep(0.1) 
                await self.writer.wait_closed()
            except Exception as e: 
                print(f' - Error CLose WriTer => {e}')
        self.reader = None 
        self.writer = None
        gc.collect()

    def dec_to_hex(self, n):
        h = hex(n)[2:]
        return h if len(h) % 2 == 0 else '0' + h

    async def send_store_shortcut(self, target_id):
        """স্টোর এবং ক্রাফটল্যান্ড ম্যাপ শর্টকাট একসাথে পাঠানোর ফাংশন"""
        try:
            # দুটি আলাদা শর্টকাট ডাটা
            map1_json = '{"WorkshopCode":"#FREEFIREEFEA38678BAE600F301D25D0D39DD6E64471","type":"UGCMapShare"}'
            map_json = '{"WorkshopCode":"#FREEFIREF63E5AB9D1C9BECFEF06BBF1AD75D3E1K200","type":"UGCMapShare"}'

            # লুপ চালিয়ে দুটি প্যাকেটই পাঠানো হবে
            for raw_json in [map1_json, map_json]:
                fields = {
                    1: 1, 
                    2: {
                        1: int(self.bot_uid),
                        2: int(target_id),
                        3: 3, # 3 = Room Chat
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

                # প্যাকেট জেনারেট এবং এনক্রিপশন
                proto_hex = CrEaTe_ProTo(fields).hex()
                encrypted = EnC_PacKeT(proto_hex, self.key, self.iv)
                length = len(encrypted) // 2
                len_hex = self.dec_to_hex(length)

                if len(len_hex) == 2: header = "1215000000"
                elif len(len_hex) == 3: header = "121500000"
                elif len(len_hex) == 4: header = "12150000"
                else: header = "1215000"

                packet = bytes.fromhex(header + len_hex + encrypted)

                if self.writer:
                    self.writer.write(packet)
                    await self.writer.drain()
                    # একটি প্যাকেট পাঠানোর পর ০.৫ সেকেন্ড অপেক্ষা (সার্ভার সেফটির জন্য)
                    await asyncio.sleep(0.5) 
            
            print(f" ✅ STORE & MAP SHORTCUTS SENT TO: {target_id}")
            return True

        except Exception as e:
            print(f" - Shortcut Error: {e}")
            return False

    async def Auto_Room_Welcome(self, room_id, chat_code):
        """রুম চ্যাট অথেন্টিকেশন, ওয়েলকাম মেসেজ এবং শর্টকাট পাঠানো"""
        try:
            if self.writer:
                # ১. রুম চ্যাট ওপেন করা
                open_pkt = await Mahir_OpeN_RoOm_ChaT(room_id, chat_code, self.key, self.iv)
                if open_pkt:
                    self.writer.write(open_pkt)
                    await self.writer.drain()
                    await asyncio.sleep(0.5)

                # ২. টেক্সট ওয়েলকাম মেসেজ পাঠানো
                welcome_msg = (
                    "[C][B][00FF00]ᎷAH!Ꮢ ᏰOᎿ [FF0000]IS HERE! ❤\n"
                    "[00FFFF] Website: [FFFF00]mahir🗿.🗿xo🗿.🗿je\n"
                    "[00FFFF]💰TCP BOT Price: [FFFF00]500 BDT\n"
                    "[00FF00]👑 Owner   : [FFFF00]@MAHIR0208\n"
                    "[00FF00] Follow My Craftland Id   : [FFFF00]1120🙄167🙄200"
                )
                msg_pkt = await Mahir_SEnd_RoOm_MsG(room_id, welcome_msg, self.bot_uid, self.key, self.iv)
                if msg_pkt:
                    self.writer.write(msg_pkt)
                    await self.writer.drain()
                
                # ৩. স্পেশাল শর্টকাট বক্স পাঠানো (আপনার রিকুয়েস্ট অনুযায়ী)
                await asyncio.sleep(0.5)
                await self.send_store_shortcut(room_id)
                
                print(f" ✅ AUTO WELCOME & STORE BOX SENT TO ROOM: {room_id}")

        except Exception as e:
            print(f" - Auto Welcome Error: {e}")

    async def OnLinE(self , Token , tok , host2 , port2 , key , iv , bot_uid):
        global writer , writer2 , TarGeT , sQ , Nm
        retry_count = 0
        max_retries = 5

        while retry_count < max_retries:  
            try: 
                if retry_count == 0:
                    print(f" - Connecting to game {host2}:{port2}...")
                
                self.reader2, self.writer2 = await asyncio.wait_for(
                    asyncio.open_connection(host2, int(port2)),
                    timeout=10
                )
                print(f" ✅ Game connected: {host2}:{port2}")

                await asyncio.sleep(0.5)

                # Send auth token
                self.writer2.write(bytes.fromhex(tok)) 
                await self.writer2.drain()
                await asyncio.sleep(0.3)

                # Send room name change/create
                room_packet = Room('[C][B][FF0000]MAHIR', key, iv)
                self.writer2.write(room_packet) 
                await self.writer2.drain()
                print('✅ ROOM NAME CHANGE => DONE')

                await asyncio.sleep(0.4)   

                # Keep connection alive and listen for room packets
                while True:  
                    try:  
                        self.DaTa = await asyncio.wait_for(
                            self.reader2.read(9999),
                            timeout=30
                        )
                        if not self.DaTa: 
                            break
                        
                        # --- অটো মেসেজ ডিটেকশন লজিক ---
                        data_hex = self.DaTa.hex()
                        if data_hex.startswith("0e00"): 
                            # রুম ডাটা প্যাকেট ডিকোড করা
                            decoded_str = DeCode_PackEt(data_hex[10:])
                            if decoded_str:
                                try:
                                    packet_json = json.loads(decoded_str)
                                    f5 = packet_json.get('5', {}).get('data', {})
                                    r_id = f5.get('1', {}).get('data')
                                    # চ্যাট কোড ফিল্ড ১০ বা ৩৬ এ থাকে
                                    c_code = f5.get('36', {}).get('data') or f5.get('10', {}).get('data')

                                    if r_id and c_code:
                                        # ব্যাকগ্রাউন্ড টাস্ক হিসেবে মেসেজ পাঠানো
                                        asyncio.create_task(self.Auto_Room_Welcome(r_id, c_code))
                                except:
                                    pass
                        # ----------------------------

                    except asyncio.TimeoutError:
                        try:
                            self.writer2.write(b'\x00')
                            await self.writer2.drain()
                        except:
                            break
                    except (ConnectionResetError , ConnectionAbortedError , asyncio.IncompleteReadError , BrokenPipeError , OSError): 
                        break 
                    except Exception:
                        break

            except Exception as e: 
                print(f" - Connection attempt {retry_count+1} failed: {e}")
                retry_count += 1
                await asyncio.sleep(1)

        print(f" - Max retries reached for OnLinE, restarting...")
        ResTarTinG()

    async def ChaT(self , Token , tok , host , port , key , iv ,bot_uid, R):
        global writer , writer2 , TarGeT , sQ , Nm
        retry_count = 0
        max_retries = 5

        while retry_count < max_retries:  
            try: 
                print(f" - Connecting to chat {host}:{port}...")
                self.reader, self.writer = await asyncio.wait_for(
                    asyncio.open_connection(host , int(port)),
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
                        
                        # --- কমান্ড ডিটেকশন লজিক ---
                        data_hex = self.DaTa.hex()
                        if data_hex.startswith("1200"): # চ্যাট মেসেজ প্যাকেট
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
                                        print(f" 🛒 Store requested by {sender_uid}")
                                        
                                        # ১. টেক্সট মেসেজ
                                        info = (
                                            "[B][C][00FFFF]ᎷAH!Ꮢ ᏰOᎿ SᎿOᏒᎬ\n"
                                            "[FFFFFF]────────────────\n"
                                            "[00FF00]🤖 TCP BOT Price : [FFFF00]500 BDT\n"
                                            "[00FF00]🌐 Website       : [FFFF00]mahir🗿.🗿xo🗿.🗿je\n"
                                            "[00FF00] Owner         : [FFFF00]@MAHIR0208\n"
                                            "[00FF00] Follow My Craftland Id   : [FFFF00]1120🙄167🙄200" # এখানে শেষে " কোটেশন মার্ক যোগ করা হয়েছে
                                        )
                                        txt_pkt = await Mahir_SEnd_RoOm_MsG(chat_id, info, self.bot_uid, self.key, self.iv)
                                        if txt_pkt:
                                            self.writer.write(txt_pkt)
                                            await self.writer.drain()
                                        
                                        # ২. শর্টকাট বক্স
                                        await asyncio.sleep(0.5)
                                        await self.send_store_shortcut(chat_id)

                                except: pass
                        # -------------------------

                    except asyncio.TimeoutError:
                        try:
                            self.writer.write(b'\x00')
                            await self.writer.drain()
                        except: break
                    except Exception: break
            except Exception:
                retry_count += 1
                await asyncio.sleep(2)
        print(f" - Max retries reached for ChaT")

    def GeT_Key_Iv(self , serialized_data):

        try:
            my_message = xZRcdx.MyMessage()
            my_message.ParseFromString(serialized_data)
            timestamp , key , iv = my_message.field21 , my_message.field22 , my_message.field23
            timestamp_obj = Timestamp()
            timestamp_obj.FromNanoseconds(timestamp)
            timestamp_seconds = timestamp_obj.seconds
            timestamp_nanos = timestamp_obj.nanos
            combined_timestamp = timestamp_seconds * 1_000_000_000 + timestamp_nanos
            return combined_timestamp , key , iv
        except Exception as e:
            print(f" - Error extracting key/iv: {e}")
            return None, None, None

    def GeT_LoGin_PorTs(self , JwT_ToKen , PayLoad):
        """Get login ports - FIXED with better error handling"""
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
            self.Res = requests.post(self.UrL , headers=self.HeadErs , data=PayLoad , verify=False, timeout=15)
            decoded = DeCode_PackEt(self.Res.content.hex())
            if not decoded:
                print(" - Failed to decode response")
                return None, None, None, None

            self.BesTo_data = json.loads(decoded)  

            if '32' not in self.BesTo_data or '14' not in self.BesTo_data:
                print(f" - Missing port data in response: {self.BesTo_data.keys()}")
                return None, None, None, None

            address , address2 = self.BesTo_data['32']['data'] , self.BesTo_data['14']['data']

            try:
                ip , port = address.rsplit(":", 1)
                ip2 , port2 = address2.rsplit(":", 1)

                port = int(port)
                port2 = int(port2)

            except Exception as e:
                print(f" - Port parsing error: {e}")
                return None, None, None, None

            print(f" - Got ports: Chat={ip}:{port}, Game={ip2}:{port2}")
            return ip , port , ip2 , port2
        except requests.RequestException as e:
            print(f" - Bad Requests: {e}")
        except Exception as e:
            print(f" - Error getting ports: {e}")
        print(" - Failed To Get Ports!")
        return None, None, None, None

    def ToKen_GeneRaTe(self, U, P):
        try:
            if not U or not P:
                print(" - Missing UID or Password")
                return None

            # ১. গ্যারিনা এক্সেস টোকেন নেওয়া
            self.A, self.O = G_AccEss(U, P)
            if not self.A or not self.O:
                print(" - Failed to get access token")
                return None

            # ২. MajoRLoGinrEq Protobuf অবজেক্ট তৈরি (mahir.py এর লজিক অনুযায়ী)
            major_login = MajoRLoGinrEq_pb2.MajorLogin()
            major_login.event_time = str(datetime.now())[:-7]
            major_login.game_name = "free fire"
            
            # ডিভাইস এবং প্ল্যাটফর্ম ইনফো (Strict Live Data Style)
            major_login.platform_id = 2
            major_login.platform_sdk_id = 2
            major_login.device_type = "Handheld"
            major_login.system_hardware = "qcom"
            major_login.system_software = "Android OS 13 / API-33 (TP1A.220624.014)"
            
            # ভার্সন কন্ট্রোল
            self.V = '1.129.1' # mahir.py এর ডাইনামিক ভার্সন অনুযায়ী পরিবর্তন করতে পারেন
            major_login.client_version = self.V
            major_login.client_version_code = "2024010012"
            
            # নেটওয়ার্ক এবং ডিসপ্লে
            major_login.telecom_operator = "Grameenphone"
            major_login.network_operator_a = "46001"
            major_login.network_type = "WIFI"
            major_login.network_type_a = "WIFI"
            major_login.screen_width = 1080
            major_login.screen_height = 2316
            major_login.screen_dpi = "480"
            
            # হার্ডওয়্যার (S22 Ultra Style)
            major_login.processor_details = "Qualcomm Technologies, Inc SM8450"
            major_login.memory = 12288
            major_login.gpu_renderer = "Adreno (TM) 730"
            major_login.gpu_version = "OpenGL ES 3.2 V@0548.0"
            major_login.graphics_api = "OpenGLES3"
            
            # ইউনিক ডিভাইস আইডি (ব্যান এড়ানোর জন্য)
            major_login.unique_device_id = "f" + str(uuid.uuid4())[:15]
            
            major_login.language = "en"
            major_login.open_id = self.O
            major_login.open_id_type = "4"
            major_login.login_open_id_type = 4
            major_login.access_token = self.A
            major_login.login_by = 3
            major_login.origin_platform_type = "4"
            major_login.primary_platform_type = "4"
            
            # মেমোরি এবং স্টোরেজ
            major_login.memory_available.version = 55
            major_login.memory_available.hidden_value = 81
            major_login.external_storage_total = 256000
            major_login.internal_storage_total = 256000
            major_login.library_path = "/data/app/com.dts.freefireth/base.apk"
            major_login.library_token = "hash|base.apk"
            major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
            
            # ৩. প্রোটোবাফ সিরিয়ালাইজ এবং এনক্রিপশন
            pb_data = major_login.SerializeToString()
            
            # mahir.py এর এনক্রিপশন মেথড (EnC_AEs যদি mahir.py এর মত হয়)
            # এখানে main.py এর EnC_AEs ফাংশনটি ব্যবহার করা হয়েছে
            self.PaYload = bytes.fromhex(EnC_AEs(pb_data.hex()))

            # ৪. মেজর লগইন রিকোয়েস্ট
            self.ResPonse = MajorLoGin(self.PaYload)
            if not self.ResPonse:
                print(" - MajorLogin failed")
                return None

            # ৫. রেসপন্স ডিকোড করা
            decoded_res = DeCode_PackEt(self.ResPonse)
            self.BesTo_data = json.loads(decoded_res)
            
            self.bot_uid = self.BesTo_data['1']['data']
            self.JwT_ToKen = self.BesTo_data['8']['data']          
            self.combined_timestamp, self.key, self.iv = self.GeT_Key_Iv(bytes.fromhex(self.ResPonse))

            if not self.key or not self.iv:
                print(" - Failed to extract key/iv")
                return None

            # ৬. পোর্ট ডাটা সংগ্রহ
            ip, port, ip2, port2 = self.GeT_LoGin_PorTs(self.JwT_ToKen, self.PaYload)

            if not ip or not port:
                print(" - Failed to get login ports")
                return None

            return self.JwT_ToKen, self.key, self.iv, self.combined_timestamp, ip, port, ip2, port2, self.bot_uid

        except Exception as e:
            print(f' - Error in new Token Generate: {e}')
            return None

    def Get_FiNal_ToKen_0115(self , U , P):
        result = self.ToKen_GeneRaTe(U , P)
        if not result:
            print(f" - Token generation failed for {U}")
            return None

        token , key , iv , Timestamp , ip , port , ip2 , port2 , bot_uid = result
        self.JwT_ToKen = token        

        try:
            self.AfTer_DeC_JwT = jwt.decode(token, options={"verify_signature": False})
            self.AccounT_Uid = self.AfTer_DeC_JwT.get('account_id')
            self.Nm = self.AfTer_DeC_JwT.get('nickname')
            self.H , self.M , self.S = GeT_Time(self.AfTer_DeC_JwT.get('exp'))
            self.Vr = self.AfTer_DeC_JwT.get('release_version')
            self.EncoDed_AccounT = hex(self.AccounT_Uid)[2:]
            self.HeX_VaLue = DecodE_HeX(Timestamp)
            self.TimE_HEx = self.HeX_VaLue
            self.JwT_ToKen_ = token.encode().hex()

            print(f" - Account: {self.Nm} (UID: {self.AccounT_Uid})")

        except Exception as e:
            print(f" - Error In ToKen decode: {e}")
            return None

        try:
            self.Header = hex(len(EnC_PacKeT(self.JwT_ToKen_, key, iv)) // 2)[2:]
            length = len(self.EncoDed_AccounT)
            self.__ = '00000000'
            if length == 9: self.__ = '0000000'
            elif length == 8: self.__ = '00000000'
            elif length == 10: self.__ = '000000'
            elif length == 7: self.__ = '000000000'
            else:
                print(f' - Unexpected length: {length}')                

            self.Header = f'0115{self.__}{self.EncoDed_AccounT}{self.TimE_HEx}00000{self.Header}'
            self.FiNal_ToKen_0115 = self.Header + EnC_PacKeT(self.JwT_ToKen_, key, iv)

        except Exception as e:
            print(f" - Error In Final Token: {e}")            
            return None

        self.AutH_ToKen = self.FiNal_ToKen_0115

        try:
            asyncio.run(self.STarT(self.JwT_ToKen , self.AutH_ToKen , ip, port , ip2 , port2 , key,  iv, bot_uid))
        except Exception as e:
            print(f" - Error starting client: {e}")

        return self.AutH_ToKen , key , iv

def load_accounts(file_path="accs.json"):

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Filter out non-UID keys like "UID"
            accounts = {k: v for k, v in data.items() if k.isdigit()}
            return accounts
    except Exception as e:
        print(f" - Error loading accounts: {e}")
        return {}

# ============ HTTP WEB SERVER ============
class BotHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html_content = '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>FF Bot Controller · MAHIR</title>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                <style>
                    * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
                    body {
                        min-height: 100vh;
                        background: radial-gradient(circle at 20% 30%, #1a0a0a, #0a0505);
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        padding: 20px;
                    }
                    .container {
                        width: 100%;
                        max-width: 1100px;
                        background: rgba(20, 10, 15, 0.85);
                        backdrop-filter: blur(15px);
                        border-radius: 30px;
                        padding: 30px;
                        border: 1px solid rgba(255, 50, 50, 0.25);
                        box-shadow: 0 20px 60px rgba(0,0,0,0.9);
                    }
                    .header {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        flex-wrap: wrap;
                        border-bottom: 2px solid rgba(255, 50, 50, 0.2);
                        padding-bottom: 20px;
                        margin-bottom: 30px;
                    }
                    .logo h1 {
                        font-size: 2.5rem;
                        font-weight: 900;
                        background: linear-gradient(135deg, #ff3333, #ff6666);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        text-shadow: 0 0 40px rgba(255,0,0,0.3);
                    }
                    .logo span { color: #ff4444; font-size: 1rem; -webkit-text-fill-color: #ff6666; }
                    .status-badge {
                        background: rgba(0,255,100,0.15);
                        border: 1px solid #00ff64;
                        padding: 8px 20px;
                        border-radius: 50px;
                        color: #00ff64;
                        font-weight: 600;
                        font-size: 0.9rem;
                    }
                    .stats {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                        gap: 15px;
                        margin-bottom: 30px;
                    }
                    .stat-card {
                        background: rgba(255,255,255,0.04);
                        border-radius: 16px;
                        padding: 18px 20px;
                        text-align: center;
                        border: 1px solid rgba(255,255,255,0.06);
                    }
                    .stat-card .number {
                        font-size: 2rem;
                        font-weight: 700;
                        color: #ff4444;
                    }
                    .stat-card .label {
                        color: #aaa;
                        font-size: 0.85rem;
                        margin-top: 5px;
                    }
                    .table-wrap {
                        overflow-x: auto;
                        border-radius: 16px;
                        border: 1px solid rgba(255,255,255,0.06);
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        background: rgba(0,0,0,0.2);
                    }
                    th {
                        background: rgba(255,50,50,0.15);
                        color: #ff6666;
                        padding: 15px 12px;
                        text-align: left;
                        font-weight: 600;
                        font-size: 0.85rem;
                        text-transform: uppercase;
                        letter-spacing: 1px;
                    }
                    td {
                        padding: 14px 12px;
                        color: #ddd;
                        border-bottom: 1px solid rgba(255,255,255,0.04);
                        font-size: 0.95rem;
                    }
                    tr:hover td { background: rgba(255,50,50,0.05); }
                    .status-online { color: #00ff88; }
                    .status-offline { color: #ff4444; }
                    .status-connecting { color: #ffaa00; }
                    .badge {
                        display: inline-block;
                        padding: 4px 14px;
                        border-radius: 50px;
                        font-size: 0.75rem;
                        font-weight: 600;
                    }
                    .badge-online { background: rgba(0,255,136,0.15); color: #00ff88; }
                    .badge-offline { background: rgba(255,68,68,0.15); color: #ff4444; }
                    .badge-connecting { background: rgba(255,170,0,0.15); color: #ffaa00; }
                    .footer {
                        margin-top: 25px;
                        text-align: center;
                        color: #666;
                        font-size: 0.8rem;
                    }
                    .refresh-btn {
                        background: rgba(255,50,50,0.15);
                        border: 1px solid rgba(255,50,50,0.3);
                        color: #ff6666;
                        padding: 8px 18px;
                        border-radius: 50px;
                        cursor: pointer;
                        transition: 0.3s;
                        font-size: 0.85rem;
                    }
                    .refresh-btn:hover {
                        background: rgba(255,50,50,0.25);
                    }
                    .empty-msg {
                        text-align: center;
                        padding: 40px;
                        color: #888;
                        font-size: 1.1rem;
                    }
                    @media (max-width: 600px) {
                        .logo h1 { font-size: 1.8rem; }
                        .stats { grid-template-columns: 1fr 1fr; }
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <div class="logo">
                            <h1>🔥 MAHIR</h1>
                            <span>FF Room Controller</span>
                        </div>
                        <div>
                            <span class="status-badge"><i class="fas fa-circle" style="color:#00ff64;font-size:10px;"></i> LIVE</span>
                            <button class="refresh-btn" onclick="location.reload()"><i class="fas fa-sync-alt"></i> Refresh</button>
                        </div>
                    </div>

                    <div class="stats">
                        <div class="stat-card">
                            <div class="number" id="totalBots">0</div>
                            <div class="label"><i class="fas fa-robot"></i> Total Bots</div>
                        </div>
                        <div class="stat-card">
                            <div class="number" style="color:#00ff88;" id="onlineBots">0</div>
                            <div class="label"><i class="fas fa-check-circle" style="color:#00ff88;"></i> Online</div>
                        </div>
                        <div class="stat-card">
                            <div class="number" style="color:#ffaa00;" id="connectingBots">0</div>
                            <div class="label"><i class="fas fa-spinner fa-spin" style="color:#ffaa00;"></i> Connecting</div>
                        </div>
                        <div class="stat-card">
                            <div class="number" style="color:#ff4444;" id="offlineBots">0</div>
                            <div class="label"><i class="fas fa-times-circle" style="color:#ff4444;"></i> Offline</div>
                        </div>
                    </div>

                    <div class="table-wrap">
                        <table>
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>UID</th>
                                    <th>Status</th>
                                    <th>Nickname</th>
                                    <th>Bot UID</th>
                                </tr>
                            </thead>
                            <tbody id="botTableBody">
                                <tr><td colspan="5" class="empty-msg"><i class="fas fa-spinner fa-spin"></i> Loading bots...</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="footer">
                        <i class="fas fa-shield-alt"></i> MAHIR Bot System &bull; Port 8080
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
                                
                                let onlineCount = 0, connectingCount = 0, offlineCount = 0;
                                let html = '';
                                const entries = Object.entries(data);
                                
                                if (entries.length === 0) {
                                    html = `<tr><td colspan="5" class="empty-msg"><i class="fas fa-robot"></i> No bots loaded</td></tr>`;
                                } else {
                                    entries.forEach(([uid, status], index) => {
                                        let statusText, statusClass, badgeClass;
                                        if (status.includes('✅') || status.includes('Connected')) {
                                            statusText = 'Online';
                                            statusClass = 'status-online';
                                            badgeClass = 'badge-online';
                                            onlineCount++;
                                        } else if (status.includes('🔄') || status.includes('Connecting')) {
                                            statusText = 'Connecting';
                                            statusClass = 'status-connecting';
                                            badgeClass = 'badge-connecting';
                                            connectingCount++;
                                        } else {
                                            statusText = 'Offline';
                                            statusClass = 'status-offline';
                                            badgeClass = 'badge-offline';
                                            offlineCount++;
                                        }
                                        html += `<tr>
                                            <td>${index + 1}</td>
                                            <td><code style="color:#ff8888;">${uid}</code></td>
                                            <td><span class="badge ${badgeClass}"><i class="fas fa-circle" style="font-size:8px;"></i> ${statusText}</span></td>
                                            <td>${status}</td>
                                            <td style="color:#888;">—</td>
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
                    fetchBots();
                    setInterval(fetchBots, 3000);
                </script>
            </body>
            </html>
            '''
            self.wfile.write(html_content.encode('utf-8'))
        
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with bot_lock:
                # এখানে U ভেরিয়েবল ব্যবহার করা যাবে না। 
                # আমরা শুধু বর্তমান ডিকশনারি কপি করে পাঠাবো।
                status_copy = bot_status.copy()
            self.wfile.write(json.dumps(status_copy).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

def run_web_server():
    server = HTTPServer(('0.0.0.0', 8080), BotHandler)
    print("\n" + "="*50)
    print("🔥 MAHIR Web Dashboard running at: http://localhost:8080")
    print("="*50 + "\n")
    webbrowser.open('http://localhost:8080')
    server.serve_forever()

def StarT_SerVer():
    print(render('MAHIR', colors=['white', 'red'], align='center'))
    TexT = f'[TarGeT InFo] > BoTs arE OnLine\n[BoT sTaTus] > [bold green]ConEcTed SuccEssFuLy[/bold green]'
    panel = Panel(Align.center(TexT) , title="[bold red]FF - RooM[/bold red]", border_style="bright_red" , padding=(1, 2) , expand=False)
    console.print(panel)

    accounts = load_accounts()
    if not accounts:
        print(" - No valid accounts found!")
        return

    print(f" - Loaded {len(accounts)} account(s)")

    # Start web server in background
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    time.sleep(2)

    threads = []
    for uid, pwd in accounts.items():
        print(f" - Starting bot for UID: {uid}")
        t = threading.Thread(target=FF_CLient, args=(uid, pwd))
        t.daemon = True
        t.start()
        threads.append(t)
        time.sleep(1)  

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n - Stopping server...")

if __name__ == "__main__":
    StarT_SerVer()
