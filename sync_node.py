import requests
import json
import urllib.parse

# 禁用 SSL 警告
requests.packages.urllib3.disable_warnings()

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
                # 直接取明文暗号
                auth = data.get('auth', 'dongtaiwang.com')
                # 强制补全 SNI
                sni = data.get('tls', {}).get('sni') or 'www.microsoft.com'
                
                # 1. 提取主端口 (处理逗号和范围)
                clean_server = raw_server.split(",")[0] if "," in raw_server else raw_server

                # 2. 构造【明文】标准链接
                # V2RayN 识别这种格式最稳：hysteria2://密码@IP:端口?参数
                safe_auth = urllib.parse.quote(auth)
                link = f"hysteria2://{safe_auth}@{clean_server}?sni={sni}&insecure=1&allowInsecure=1#DTW_AutoSync"
                
                return link
        except:
            continue
    return None

if __name__ == "__main__":
    node_link = get_node()
    if node_link:
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write(node_link)
