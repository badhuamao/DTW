import requests
import json
import base64
import urllib.parse

requests.packages.urllib3.disable_warnings()

SOURCES = {
    "TV-主力1": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/1/config.json",
    "TV-主力2": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/2/config.json",
    "TV-备用3": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/3/config.json",
    "TV-备用4": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/4/config.json"
}

def get_tv_nodes():
    headers = {'User-Agent': 'Mozilla/5.0'}
    results = []
    
    for name, url in SOURCES.items():
        try:
            r = requests.get(url, timeout=15, headers=headers, verify=False)
            if r.status_code == 200:
                cfg = r.json()
                
                # 1. 提取基础信息
                server = cfg.get('server', '')
                auth = urllib.parse.unquote(cfg.get('auth', 'dongtaiwang.com'))
                sni = cfg.get('tls', {}).get('sni') or 'www.microsoft.com'
                
                # 2. 【电视优化】只取第一个端口，拒绝端口跳跃范围
                # 电视端插件如果看到 28000-29000 经常会直接断开
                clean_server = server.split(",")[0] if "," in server else server
                
                # 3. 【电视优化】全量 Base64 化处理，加冒号伪装
                # 这样不管是 v2rayNG 还是 Clash Meta 电视版都能 100% 识别
                b64_auth = base64.b64encode(auth.encode()).decode().replace("=", "")
                safe_auth = b64_auth + ":"
                
                # 4. 【电视优化】注入流量控制参数
                # 明确告诉电视插件带宽限制，防止 SmartTube 瞬间拉取导致 UDP 溢出
                params = {
                    "sni": sni,
                    "insecure": "1",
                    "upmbps": "20",   # 限制上传 20Mbps
                    "downmbps": "100" # 限制下载 100Mbps
                }
                param_str = urllib.parse.urlencode(params)
                
                link = f"hysteria2://{safe_auth}@{clean_server}?{param_str}#{name}"
                results.append(link)
                print(f"TV版同步成功: {name}")
        except:
            continue
    return results

if __name__ == "__main__":
    nodes = get_tv_nodes()
    if nodes:
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(nodes))
