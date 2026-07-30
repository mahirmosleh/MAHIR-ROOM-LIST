# By mr3skr | 4real ofc - FIXED VERSION

import requests , json , binascii , time , urllib3 , base64 , datetime , re ,socket , threading , random , os , sys , psutil
from protobuf_decoder.protobuf_decoder import Parser
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad , unpad
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from random import choice

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Key , Iv = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56]) , bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

def Ua():
    versions = [
        '4.0.18P6', '4.0.19P7', '4.0.20P1', '4.1.0P3', '4.1.5P2', '4.2.1P8',
        '4.2.3P1', '5.0.1B2', '5.0.2P4', '5.1.0P1', '5.2.0B1', '5.2.5P3',
        '5.3.0B1', '5.3.2P2', '5.4.0P1', '5.4.3B2', '5.5.0P1', '5.5.2P3'
    ]
    models = [
        'SM-A125F', 'SM-A225F', 'SM-A325M', 'SM-A515F', 'SM-A725F', 'SM-M215F', 'SM-M325FV',
        'Redmi 9A', 'Redmi 9C', 'POCO M3', 'POCO M4 Pro', 'RMX2185', 'RMX3085',
        'moto g(9) play', 'CPH2239', 'V2027', 'OnePlus Nord', 'ASUS_Z01QD',
    ]
    android_versions = ['9', '10', '11', '12', '13', '14']
    languages = ['en-US', 'es-MX', 'pt-BR', 'id-ID', 'ru-RU', 'hi-IN']
    countries = ['USA', 'MEX', 'BRA', 'IDN', 'RUS', 'IND']
    version = random.choice(versions)
    model = random.choice(models)
    android = random.choice(android_versions)
    lang = random.choice(languages)
    country = random.choice(countries)
    return f"GarenaMSDK/{version}({model};Android {android};{lang};{country};)"

def EnC_AEs(HeX):
    cipher = AES.new(Key , AES.MODE_CBC , Iv)
    return cipher.encrypt(pad(bytes.fromhex(HeX), AES.block_size)).hex()

def ArA_CoLor():
    return "FF0000"

def DEc_AEs(HeX):
    cipher = AES.new(Key , AES.MODE_CBC , Iv)
    return unpad(cipher.decrypt(bytes.fromhex(HeX)), AES.block_size).hex()

def EnC_PacKeT(HeX , K , V): 
    return AES.new(K , AES.MODE_CBC , V).encrypt(pad(bytes.fromhex(HeX) ,16)).hex()

def DEc_PacKeT(HeX , K , V):
    return unpad(AES.new(K , AES.MODE_CBC , V).decrypt(bytes.fromhex(HeX)) , 16).hex()  

def EnC_Uid(H , Tp):
    e , H = [] , int(H)
    while H:
        e.append((H & 0x7F) | (0x80 if H > 0x7F else 0)) ; H >>= 7
    return bytes(e).hex() if Tp == 'Uid' else None

def EnC_Vr(N):
    if N < 0: ''
    H = []
    while True:
        BesTo = N & 0x7F ; N >>= 7
        if N: BesTo |= 0x80
        H.append(BesTo)
        if not N: break
    return bytes(H)

def DEc_Uid(H):
    n = s = 0
    for b in bytes.fromhex(H):
        n |= (b & 0x7F) << s
        if not b & 0x80: break
        s += 7
    return n

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
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(CrEaTe_LenGTh(field, value))           
    return packet    

def DecodE_HeX(H):
    R = hex(H) 
    F = str(R)[2:]
    if len(F) == 1: F = "0" + F ; return F
    else: return F

def Fix_PackEt(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data['wire_type'] = result.wire_type
        if result.wire_type == "varint":
            field_data['data'] = result.data
        if result.wire_type == "string":
            field_data['data'] = result.data
        if result.wire_type == "bytes":
            field_data['data'] = result.data
        elif result.wire_type == 'length_delimited':
            field_data["data"] = Fix_PackEt(result.data.results)
        result_dict[result.field] = field_data
    return result_dict

def DeCode_PackEt(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = Fix_PackEt(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        print(f"error {e}")
        return None

def xBunnEr():
    avatar_list = [
        '902000016', '902000031', '902000011', '902000065',
        '902000204', '902000192', '902000191', '902000179',
        '902000133', '902045001', '902038023', '902048004',
        '902039014', '902000063', '902000306', '902047009'
    ]
    return int(random.choice(avatar_list))

def GLobaL(T , K , V):
    fields =  {1: 3 , 2: {2: 5 , 3: f"{T}"}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '1215' , K , V)

def ChaT_sQ(T , N , U , sQ , K , V):
    fields =  {1: N , 2: {1: int(U) , 3: f"{T}" , 4: str(sQ)}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '1215' , K , V)

def Send_MsG(msg , owner , K , V):
    fields = {
    1: 1,
    2: 2,
    2: {
        1: 0000000,
        2: owner,
        4: msg,
        5: 1757799182,
        7: 2,
        9: {
            1: "MAHIR",
            2: xBunnEr(),
            3: 909000024,
            4: 330,
            5: 909000024,
            7: 2,
            10: 1,
            11: 1,
            12: 0,
            13: {1: 2},
            14: {
                1: "FUCKING",
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            }
        },
        10: "fr",
        13: {3: 1},
        14: ""}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '1215' , K , V)

def Room1v1(room_name, K, V):
    fields = {
        1: 2,
        2: {
            1: 1,
            2: 15,
            3: 0,
            4: room_name,
            6: 2,
            7: 1,
            8: 1,
            9: 1,
            11: 1,
            12: 2,
            14: 3030901227,
            15: {1: "IDC3", 2: 126, 3: "BD"},
            16: "\u0001\u0003\u0004\u0007\t\n\u000b\u0012\u000f\u000e\u0016\u0019\u001a \u001d",
            18: 3030901002000,
            27: 1,
            34: "\u0000\u0001",
            40: "en",
            48: 1,
            49: {1: 2},
        }
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0e0b' , K , V)

def Room2v2(room_name, K, V):
    fields = {
        1: 2,
        2: {
            1: 1,
            2: 15,
            3: 1,
            4: room_name,
            6: 4,
            7: 1,
            8: 1,
            9: 1,
            11: 1,
            12: 2,
            14: 3030901227,
            15: {1: "IDC3", 2: 126, 3: "BD"},
            16: "\u0001\u0003\u0004\u0007\t\n\u000b\u0012\u000f\u000e\u0016\u0019\u001a \u001d",
            18: 3030901002000,
            27: 1,
            34: "\u0000\u0001",
            40: "en",
            48: 1,
            49: {1: 2},
        }
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0e0b' , K , V)

def Room4v4(room_name, K, V):
    fields = {
        1: 2,
        2: {
            1: 1,
            2: 15,
            3: 3,
            4: room_name,
            6: 8,
            7: 1,
            8: 1,
            9: 1,
            11: 1,
            12: 2,
            14: 3030901227,
            15: {1: "IDC3", 2: 126, 3: "BD"},
            16: "\u0001\u0003\u0004\u0007\t\n\u000b\u0012\u000f\u000e\u0016\u0019\u001a \u001d",
            18: 3030901002000,
            27: 1,
            34: "\u0000\u0001",
            40: "en",
            48: 1,
            49: {1: 2},
        }
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0e0b' , K , V)

def nRoom1v1(room_name, K, V):
    """Create room packet - FIXED VERSION"""
    fields = {
        1: 2,
        2: {
            1: 1,
            2: 15,
            3: 0,
            4: room_name,
            6: 2,
            7: 1,
            8: 1,
            9: 1,
            11: 1,
            12: 2,
            14: 3030901227,
            15: [
                {
                    1: "IDC1",
                    2: 3000,
                    3: "BD"
                },
                {
                    1: "IDC2",
                    2: 3000,
                    3: "BD"
                }
            ]
        }
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0e0b' , K , V)

def nRoom2v2(room_name, K, V):
    """Create room packet - FIXED VERSION"""
    fields = {
        1: 2,
        2: {
            1: 1,
            2: 15,
            3: 1,
            4: room_name,
            6: 4,
            7: 1,
            8: 1,
            9: 1,
            11: 1,
            12: 2,
            14: 3030901227,
            15: [
                {
                    1: "IDC1",
                    2: 3000,
                    3: "BD"
                },
                {
                    1: "IDC2",
                    2: 3000,
                    3: "BD"
                }
            ]
        }
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0e0b' , K , V)

def nRoom4v4(room_name, K, V):
    """Create room packet - FIXED VERSION"""
    fields = {
        1: 2,
        2: {
            1: 1,
            2: 15,
            3: 3,
            4: room_name,
            6: 8,
            7: 1,
            8: 1,
            9: 1,
            11: 1,
            12: 2,
            14: 3030901227,
            15: [
                {
                    1: "IDC1",
                    2: 3000,
                    3: "BD"
                },
                {
                    1: "IDC2",
                    2: 3000,
                    3: "BD"
                }
            ]
        }
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0e0b' , K , V)

def nRoom6v6(room_name, K, V):
    """Create room packet - FIXED VERSION"""
    fields = {
        1: 2,
        2: {
            1: 1,
            2: 15,
            3: 5,
            4: room_name,
            6: 12,
            7: 1,
            8: 1,
            9: 1,
            11: 1,
            12: 2,
            14: 36981056,
            15: [
                {
                    1: "IDC1",
                    2: 3000,
                    3: "BD"
                },
                {
                    1: "IDC2",
                    2: 3000,
                    3: "BD"
                }
            ]
        }
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0e0b' , K , V)

def Join_Sq(T , U , rQ , K , V):
    fields = {1: 4 , 2: {1: U , 6: 1 , 8: 1 , 13: f"{T}", 15: str(rQ) , 16: "OR"}} 
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0515' , K , V)

def LeVe_C(cid , K , V):
    fields = {}
    fields[1] = 4
    fields[2] = {}
    fields[2][1] = int(cid)
    fields[2][2] = 5
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '1201' , K , V)

def Send_GhosTs(Uid , Nm , sQ , K , V):
    fields =  {1: 61 , 2: {1: int(Uid) , 2: {1: int(Uid) , 2: 1159, 3: f'{Nm}', 5: 12, 6: 9999999, 7: 1, 8: {2: 1, 3: 1}, 9: 3}, 3: sQ}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0515' , K , V)

def Send_InV(N , U , K , V):
    fields =  {1: 2 , 2: {1: int(U) , 2: "BD" , 4: N}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0515' , K , V)

def trydecByRedZed(pack):
    try:
        r = pack['5']['data']['3']['data']['31']['data']
    except KeyError:
        r = pack['5']['data']['31']['data']
    except:
        return None
    return r

def RedZed_3alamyia_Chat(uid, code , K, I):
    fields = {
        1: 3,
        2: {
            1: uid,
            3: "fr",
            4: str(code)
        }
    }
    redzed_fields = str(CrEaTe_ProTo(fields).hex())
    return GeneRaTePk(str(redzed_fields) ,'1215', K, I)

def quit_caht_redzed(uid,K,I):
    fields = {
        1: 4,
        2: {
            1: uid,
            3: "fr"
        }
    }
    redzed_fields = str(CrEaTe_ProTo(fields).hex())
    return GeneRaTePk(str(redzed_fields) ,'1215', K, I)

def RedZed_SendInv(bot_uid, uid,K,V):
    fields = {1: 33, 2: {1: int(uid), 2: "BD", 3: 1, 4: 1, 6: "ONLY-MAHIR!!", 7: 330, 8: 1000, 9: 100, 10: "DZ", 12: 1, 13: int(uid), 16: 1, 17: {2: 159, 4: "y[WW", 6: 11, 8: "1.118.1", 9: 3, 10: 1}, 18: 306, 19: 18, 24: 902000306, 26: {}, 27: {1: 11, 2: int(bot_uid), 3: 999}, 28: {}, 31: {1: 1, 2: 32768}, 32: 32768, 34: {1: bot_uid, 2: 8, 3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"}}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0515' , K , V)

def RedZed_SendMsg(msg , owner , bot, K, I):
    fields = {
        1: 1,
        2:2,
        2: {
            1: bot,
            2: owner,
            4: msg,
            5: str(time.time()).split('.')[0],
            9: {
                1: "MAHIR",
                2: xBunnEr(),
                3:909000024,
                4: 330,
                5:909000024,
                10: 1,
                11: 1,
                7: 2,
                13: {1:2},
                14: {
                    1: bot,
                    2:8,
                    3: {}
                }
            },
            10: "fr",
            13: {
                2: 1,
                3: 1
            },
            14: {}
        }
    }
    redzed_fields = str(CrEaTe_ProTo(fields).hex())
    return GeneRaTePk(str(redzed_fields) ,'1215', K, I)

def ExiT(K , V):
    fields = {1: 7 , 2: {1: int(00000000)}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0515' , K , V)

def GeneRaTePk(Pk , N , K , V):
    PkEnc = EnC_PacKeT(Pk , K , V)
    _ = DecodE_HeX(int(len(PkEnc) // 2))
    if len(_) == 2: HeadEr = N + "000000"
    elif len(_) == 3: HeadEr = N + "00000"
    elif len(_) == 4: HeadEr = N + "0000"
    elif len(_) == 5: HeadEr = N + "000"
    return bytes.fromhex(HeadEr + _ + PkEnc)

def ResTarTinG():
    print('\n - ResTartinG BoT ... ! ')
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
    python = sys.executable
    os.execl(python, python, *sys.argv)

def AuTo_ResTartinG():
    """Auto restart after 6 hours - FIXED"""
    time.sleep(6 * 60 * 60)
    print('\n - AuTo ResTartinG The BoT ... ! ')
    try:
        p = psutil.Process(os.getpid())
        for f in p.open_files():
            try:
                os.close(f.fd)
            except Exception as e:
                print(f" - Error Close File: {e}")
        for conn in p.net_connections(kind='inet'):
            try:
                if conn.fd != -1:
                    os.close(conn.fd)
            except Exception as e:
                print(f" - Error Close Connection: {e}")
    except Exception as e:
        print(f" - Error Accessing Process Info: {e}")

    python = sys.executable
    os.execl(python, python, *sys.argv)    

def GeT_Time(timestamp):
    last_login = datetime.fromtimestamp(timestamp)
    now = datetime.now()
    diff = now - last_login   
    h , rem = divmod(diff.seconds, 3600)
    m , s = divmod(rem, 60)    
    return h, m, s             

def xMsGFixinG(n):
    return '🗿'.join(str(n)[i:i + 1] for i in range(0 , len(str(n)) , 1))

def LogOuT(A):
    R = requests.Session().get(f'https://100067.connect.garena.com/oauth/logout?access_token={A}&refresh_token=')
    print(' - LoGOuT => ' , R.text)
    if R.status_code == 200 and '0' in R.text: return True
    else: return False
