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
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    for url in URLS:
        try:
            r = requests.get(url, timeout=15, headers=headers, verify=False)
            if r.status_code == 200:
                data = r.json()
                raw_server = data.get('server', '')
                auth = data.get('auth', 'dongtaiwang.com')
                # 优先级：云端 SNI > 微软伪装
                sni = data.get('tls', {}).get('sni') or 'www.microsoft.com'
                
                # 1. 提取主端口 (处理逗号和范围)
                clean_server = raw_server.split(",")[0] if "," in raw_server else raw_server

                # 2. 构造【明文版】标准链接 (V2RayN 兼容性最好)
                # 这里的 auth 不进行 Base64，直接填进去，但要经过 URL 编码
                safe_auth = urllib.parse.quote(auth)
                
                # 加上 mport 参数，万一你想手动开启端口跳跃呢
                mport = ""
                if "," in raw_server:
                    mport = f"&mport={raw_server.split(',', 1)[1]}"

                link = f"hysteria2://{safe_auth}@{clean_server}?sni={sni}&insecure=1&allowInsecure=1{mport}#DTW_AutoSync"
                
                return link
        except Exception as e:
            print(f"Error: {e}")
            continue
    return None

if __name__ == "__main__":
    node_link = get_node()
    if node_link:
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write(node_link)
