import requests
import json
import base64
import urllib.parse

# 动态网云端配置源
URLS = [
    "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/1/config.json",
    "https://gitlab.com/free9999/ipupdate/-/raw/master/backup/img/1/2/ipp/hysteria2/1/config.json"
]

def get_node():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    for url in URLS:
        try:
            # 禁用 SSL 验证以应对某些环境下的证书问题
            r = requests.get(url, timeout=15, headers=headers, verify=False)
            if r.status_code == 200:
                data = r.json()
                
                # 1. 提取核心字段
                raw_server = data.get('server', '')
                auth = data.get('auth', '')
                sni = data.get('tls', {}).get('sni', 'www.microsoft.com')
                
                # 2. 关键修复：处理非标端口格式 (v2rayN 识别修正)
                # 如果 server 是 "1.2.3.4:1234,2000-3000"，只取 "1.2.3.4:1234"
                if "," in raw_server:
                    clean_server = raw_server.split(",")[0]
                else:
                    clean_server = raw_server
                
                # 3. 构造标准 Hysteria2 链接
                # 编码备注：auth 里的特殊字符需要转义
                safe_auth = urllib.parse.quote(auth)
                link = f"hysteria2://{safe_auth}@{clean_server}?sni={sni}&insecure=1&allowInsecure=1#DTW_AutoSync"
                
                return link
        except Exception as e:
            print(f"源 {url} 同步失败: {e}")
            continue
    return None

if __name__ == "__main__":
    node_link = get_node()
    if node_link:
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write(node_link)
        print("✅ 节点同步并转换成功！")
    else:
        print("❌ 未能获取到有效节点。")
