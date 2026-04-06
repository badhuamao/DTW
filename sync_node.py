import requests
import json
import base64
import urllib.parse

URLS = [
    "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/1/config.json",
    "https://gitlab.com/free9999/ipupdate/-/raw/master/backup/img/1/2/ipp/hysteria2/1/config.json"
]

def get_node():
    headers = {'User-Agent': 'Mozilla/5.0'}
    for url in URLS:
        try:
            r = requests.get(url, timeout=15, headers=headers, verify=False)
            if r.status_code == 200:
                data = r.json()
                raw_server = data.get('server', '')
                auth = data.get('auth', '')
                sni = data.get('tls', {}).get('sni', 'www.microsoft.com')
                
                # 1. 修复端口逻辑
                if "," in raw_server:
                    clean_server = raw_server.split(",")[0]
                else:
                    clean_server = raw_server

                # 2. 【核心修复】将 auth 进行 Base64 编码，解决识别问题
                # 这是最符合 HY2 标准且 v2rayN 绝对认识的写法
                b64_auth = base64.b64encode(auth.encode()).decode()

                # 3. 构造链接（不带 @ 符号前面的明文，直接用编码后的字符串）
                link = f"hysteria2://{b64_auth}@{clean_server}?sni={sni}&insecure=1&allowInsecure=1#DTW_AutoSync"
                
                return link
        except:
            continue
    return None

if __name__ == "__main__":
    node_link = get_node()
    if node_link:
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write(node_link)
