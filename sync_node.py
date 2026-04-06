import requests
import json
import base64
import urllib.parse

# 屏蔽安全警告
requests.packages.urllib3.disable_warnings()

# 对应你 4 个 .bat 文件里的云端精准路径
SOURCES = {
    "DTW-主力1号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/1/config.json",
    "DTW-主力2号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/2/config.json",
    "DTW-备用3号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/3/config.json",
    "DTW-备用4号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/4/config.json"
}

def fetch_all():
    headers = {'User-Agent': 'Mozilla/5.0'}
    all_links = []
    
    for name, url in SOURCES.items():
        try:
            r = requests.get(url, timeout=15, headers=headers, verify=False)
            if r.status_code == 200:
                cfg = r.json()
                
                # 提取基础字段
                server = cfg.get('server', '')
                auth = urllib.parse.unquote(cfg.get('auth', 'dongtaiwang.com'))
                sni = cfg.get('tls', {}).get('sni') or 'www.microsoft.com'
                
                # 保持原始 server 字符串（保留端口跳跃能力）
                # v2rayN 和部分电视插件其实是认这个的
                clean_server = server.split(",")[0] if "," in server else server

                # 【主力2号识别核心逻辑】
                if name == "DTW-主力2号" or len(auth) > 30 or "%" in auth:
                    # 转 Base64 并去掉等号，末尾补冒号，解决 v2rayN 识别 Bug
                    b64_auth = base64.b64encode(auth.encode()).decode().replace("=", "")
                    safe_auth = b64_auth + ":"
                else:
                    safe_auth = auth
                
                link = f"hysteria2://{safe_auth}@{clean_server}?sni={sni}&insecure=1&allowInsecure=1#{name}"
                all_links.append(link)
                print(f"✅ {name} 还原成功")
        except:
            continue
    return all_links

if __name__ == "__main__":
    nodes = fetch_all()
    if nodes:
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(nodes))
