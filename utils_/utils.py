import os, sys, traceback, requests, re
sys.path.append(os.getcwd()) # 根目录
from config import ROBOTID

def try_except_code(function):
    """处理python的异常,以及requests请求异常。在需要的函数名前面使用装饰器语法@try_except_code调用
    捕获requests异常时,需要在使用地方的响应后面加一句response.raise_for_status()来检查响应的状态码,如果状态码表明请求失败,则抛出一个HTTPError异常,然后就可以用此函数捕获异常。如果状态码表明请求成功,则什么也不会发生,函数会直接返回
    """
    def wrapper(*args, **kwargs):
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            # trace_back = traceback.format_exc()
            # print("出错文件和行号:")
            # traceback.print_tb(e.__traceback__)
            # print("错误信息:", str(e))
            # 获取异常信息
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # 获取文件名和行号
            file_name = traceback.extract_tb(exc_tb)[-1][0]
            line_number = traceback.extract_tb(exc_tb)[-1][1]
            # 输出错误信息
            print("出错文件:", file_name)
            print("出错位置:", line_number, '行')
            print("出错类型:", exc_type.__name__)
            print("错误信息:", str(e))
            result = None
        except requests.exceptions.RequestException:
            # 处理 requests 异常
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # 获取文件名和行号
            file_name = traceback.extract_tb(exc_tb)[-1][0]
            line_number = traceback.extract_tb(exc_tb)[-1][1]
            # 输出错误信息
            print("出错文件:", file_name)
            print("出错位置:", line_number, '行')
            print("出错类型:", exc_type.__name__)
            print("错误信息:", str(exc_obj))
            result = None
        except requests.exceptions.HTTPError as e:
            # 处理 HTTP 异常
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # 获取文件名和行号
            file_name = traceback.extract_tb(exc_tb)[-1][0]
            line_number = traceback.extract_tb(exc_tb)[-1][1]
            # 输出错误信息
            print("出错文件:", file_name)
            print("出错位置:", line_number, '行')
            print("出错类型:", exc_type.__name__)
            print("错误信息:", str(e))
            result = None
        return result
    return wrapper

@try_except_code
def dingding_notice(content, robot_id=ROBOTID):
    """钉钉提醒"""
    url = f'https://oapi.dingtalk.com/robot/send?access_token={robot_id}'
    msg = {
            "msgtype": "text",
            "text": {"content": content}
        }
    headers = {"Content-Type": "application/json;charset=utf-8"}
    response = requests.post(url=url,json=msg,headers=headers,timeout=10).json()
    return response

def is_valid_contact(contact):
    """判断手机号或邮箱地址是否有效"""
    phone_pattern = r'^1[3-9]\d{9}$'
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(phone_pattern, contact) or re.match(email_pattern, contact))

def is_valid_address(address):
    """
    判断区块链地址是否合法
    :param address: 区块链地址
    :return: True or False
    """
    # 比特币地址
    btc_pattern = r'^[13][a-km-zA-HJ-NP-Z0-9]{26,33}$'
    # 以太坊地址
    eth_pattern = r'^0x[a-fA-F0-9]{40}$'
    # 莱特币地址
    ltc_pattern = r'^[LM3][a-km-zA-HJ-NP-Z0-9]{26,33}$'
    # TRX地址
    trx_pattern = r'^T[a-km-zA-HJ-NP-Z0-9]{33}$'

    if re.match(btc_pattern, address):
        return True
    elif re.match(eth_pattern, address):
        return True
    elif re.match(ltc_pattern, address):
        return True
    elif re.match(trx_pattern, address):
        return True
    else:
        return False
        
if __name__ == '__main__':

    print(is_valid_contact('13512345678'))  # 输出 True
    print(is_valid_contact('test@example.com'))  # 输出 True
    print(is_valid_contact('invalid_contact'))  # 输出 False
    print(is_valid_address('0x85C2e939D0261d587402E4D29b5e75AF0Afa4E9F'))  # 输出 True
