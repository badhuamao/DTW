import requests
import json
import base64
import urllib.parse
import yaml  # 记得在 Actions 里安装 PyYAML

# 屏蔽安全警告
requests.packages.urllib3.disable_warnings()

SOURCES = {
    "DTW-主力1号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/1/config.json",
    "DTW-主力2号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/2/config.json",
    "DTW-备用3号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/3/config.json",
    "DTW-备用4号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/4/config.json"
}

def fetch_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    nodes_info = []
    
    for name, url in SOURCES.items():
        try:
            r = requests.get(url, timeout=15, headers=headers, verify=False)
            if r.status_code == 200:
                cfg = r.json()
                # 提取核心字段
                server_full = cfg.get('server', '')
                # 处理 IPv6 和端口
                if "]:" in server_full:
                    host = server_full.split("]:")[0].replace("[", "")
                    port = int(server_full.split("]:")[1].split(",")[0])
                else:
                    host = server_full.split(":")[0]
                    port = int(server_full.split(":")[1].split(",")[0])
                
                auth = urllib.parse.unquote(cfg.get('auth', 'dongtaiwang.com'))
                sni = cfg.get('tls', {}).get('sni') or 'www.microsoft.com'
                
                nodes_info.append({
                    "name": name,
                    "server": host,
                    "port": port,
                    "auth": auth,
                    "sni": sni
                })
        except:
            continue
    return nodes_info

def generate_clash_yaml(nodes):
    clash_config = {
        "port": 7890,
        "socks-port": 7891,
        "allow-lan": True,
        "mode": "rule",
        "log-level": "info",
        "proxies": [],
        "proxy-groups": [
            {
                "name": "🚀 节点选择",
                "type": "select",
                "proxies": [n["name"] for n in nodes]
            }
        ],
        "rules": [
            "MATCH,🚀 节点选择"
        ]
    }

    for n in nodes:
        clash_config["proxies"].append({
            "name": n["name"],
            "type": "hysteria2",
            "server": n["server"],
            "port": n["port"],
            "password": n["auth"],
            "sni": n["sni"],
            "skip-cert-verify": True
        })
    
    with open("tv.yaml", "w", encoding="utf-8") as f:
        yaml.dump(clash_config, f, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    raw_nodes = fetch_data()
    if raw_nodes:
        # 生成原来的 nodes.txt (URI格式)
        with open("nodes.txt", "w", encoding="utf-8") as f:
            links = []
            for n in raw_nodes:
                # 这里的 safe_auth 逻辑保留你之前的识别代码
                safe_auth = n["auth"]
                if n["name"] == "DTW-主力2号" or len(n["auth"]) > 30:
                    safe_auth = base64.b64encode(n["auth"].encode()).decode().replace("=", "") + ":"
                
                server_str = f"[{n['server']}]:{n['port']}" if ":" in n['server'] else f"{n['server']}:{n['port']}"
                links.append(f"hysteria2://{safe_auth}@{server_str}?sni={n['sni']}&insecure=1&allowInsecure=1#{n['name']}")
            f.write("\n".join(links))
        
        # 生成新的 tv.yaml
        generate_clash_yaml(raw_nodes)
        print("✅ nodes.txt & tv.yaml 更新成功")
