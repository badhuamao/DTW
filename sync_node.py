import requests
import json
import base64
import urllib.parse

# 禁用 SSL 验证警告
requests.packages.urllib3.disable_warnings()

# 根据你提供的 .bat 文件总结出的四个精准源
SOURCES = {
    "DTW-主力1号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/1/config.json",
    "DTW-主力2号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/2/config.json",
    "DTW-备用3号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/3/config.json",
    "DTW-备用4号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/4/config.json"
}

def fetch_and_convert():
    headers = {'User-Agent': 'Mozilla/5.0'}
    all_nodes = []
    
    for name, url in SOURCES.items():
        try:
            # 每个源尝试抓取
            r = requests.get(url, timeout=10, headers=headers, verify=False)
            if r.status_code == 200:
                data = r.json()
                raw_server = data.get('server', '')
                auth = data.get('auth', 'dongtaiwang.com')
                sni = data.get('tls', {}).get('sni', 'www.microsoft.com')
                
                # 处理端口跳跃：保留主端口，丢弃 v2rayN 不认的范围
                clean_server = raw_server.split(",")[0] if "," in raw_server else raw_server
                
                # 构造明文 URL 格式（v2rayN 兼容性最好）
                safe_auth = urllib.parse.quote(auth)
                link = f"hysteria2://{safe_auth}@{clean_server}?sni={sni}&insecure=1&allowInsecure=1#{name}"
                all_nodes.append(link)
                print(f"成功同步: {name}")
        except:
            print(f"失败跳过: {name}")
            continue
            
    return all_nodes

if __name__ == "__main__":
    node_list = fetch_and_convert()
    if node_list:
        with open("nodes.txt", "w", encoding="utf-8") as f:
            # 换行拼接，方便订阅导入
            f.write("\n".join(node_list))
