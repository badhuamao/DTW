import requests
import json
import base64
import urllib.parse

# 屏蔽安全警告
requests.packages.urllib3.disable_warnings()

# 对应你那 4 个 .bat 文件里的云端地址
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
                
                # 1. 提取核心字段
                server = cfg.get('server', '')
                auth = cfg.get('auth', 'dongtaiwang.com')
                sni = cfg.get('tls', {}).get('sni') or 'www.microsoft.com'
                
                # 2. 修复端口识别（只取第一个主端口）
                clean_server = server.split(",")[0] if "," in server else server
                
                # 3. 【核心修复】Auth 兼容性处理
                # 如果暗号太复杂或者带特殊符号（如 %），强制用 Base64 包装
                if "%" in auth or len(auth) > 30:
                    # 去掉可能存在的 URL 编码还原成原始暗号再 Base64
                    raw_auth = urllib.parse.unquote(auth)
                    safe_auth = base64.b64encode(raw_auth.encode()).decode()
                else:
                    # 简单的 dongtaiwang.com 直接用明文，识别率最高
                    safe_auth = auth
                
                # 4. 生成链接
                link = f"hysteria2://{safe_auth}@{clean_server}?sni={sni}&insecure=1&allowInsecure=1#{name}"
                results.append(link)
                print(f"✅ {name} 同步成功")
        except Exception as e:
            print(f"❌ {name} 失败: {e}")
            
    return results

if __name__ == "__main__":
    node_list = get_nodes()
    if node_list:
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(node_list))
        print("--- 任务全部完成 ---")
