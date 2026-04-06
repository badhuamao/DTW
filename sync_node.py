import requests
import json
import base64
import urllib.parse

# 屏蔽安全警告
requests.packages.urllib3.disable_warnings()

SOURCES = {
    "DTW-主力1号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/1/config.json",
    "DTW-主力2号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/2/config.json",
    "DTW-备用3号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/3/config.json",
    "DTW-备用4号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/4/config.json"
}

def get_nodes():
    headers = {'User-Agent': 'Mozilla/5.0'}
    results = []
    
    for name, url in SOURCES.items():
        try:
            r = requests.get(url, timeout=15, headers=headers, verify=False)
            if r.status_code == 200:
                cfg = r.json()
                server = cfg.get('server', '')
                # 获取原始 auth
                auth = cfg.get('auth', 'dongtaiwang.com')
                # 兼容云端可能已经 URL 编码过的情况
                auth = urllib.parse.unquote(auth)
                sni = cfg.get('tls', {}).get('sni') or 'www.microsoft.com'
                
                clean_server = server.split(",")[0] if "," in server else server
                
                # 【核心修复逻辑】
                if name == "DTW-主力2号" or len(auth) > 30 or "%" in auth:
                    # 1. 编码为 Base64
                    b64_auth = base64.b64encode(auth.encode()).decode()
                    # 2. 重点：去掉结尾的等号，防止干扰 v2rayN 解析 @ 符号
                    safe_auth = b64_auth.replace("=", "")
                else:
                    # 简单的明文直接用
                    safe_auth = auth
                
                link = f"hysteria2://{safe_auth}@{clean_server}?sni={sni}&insecure=1&allowInsecure=1#{name}"
                results.append(link)
        except:
            continue
    return results

if __name__ == "__main__":
    node_list = get_nodes()
    if node_list:
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(node_list))
