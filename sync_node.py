import requests
import json
import base64
import urllib.parse

# 屏蔽 SSL 验证警告
requests.packages.urllib3.disable_warnings()

# 对应你那 4 个 .bat 文件中的云端精准路径
SOURCES = {
    "DTW-主力1号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/1/config.json",
    "DTW-主力2号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/2/config.json",
    "DTW-备用3号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/3/config.json",
    "DTW-备用4号": "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/4/config.json"
}

def fetch_all_nodes():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    all_links = []
    
    for name, url in SOURCES.items():
        try:
            # 增加超时重试机制
            r = requests.get(url, timeout=15, headers=headers, verify=False)
            if r.status_code == 200:
                data = r.json()
                
                # 提取关键字段
                raw_server = data.get('server', '')
                auth = data.get('auth', 'dongtaiwang.com')
                # 还原可能存在的 URL 编码
                auth = urllib.parse.unquote(auth)
                sni = data.get('tls', {}).get('sni') or 'www.microsoft.com'
                
                # 处理服务器地址（只取第一个主端口，保留 IPv6 的方括号）
                clean_server = raw_server.split(",")[0] if "," in raw_server else raw_server

                # 【核心兼容性处理：针对 v2rayN 的解析 Bug】
                # 如果是主力2号的长暗号，或者带特殊符号，使用“Base64+去等号+补冒号”策略
                if name == "DTW-主力2号" or len(auth) > 30 or "%" in auth:
                    # 1. 转 Base64
                    b64_auth = base64.b64encode(auth.encode()).decode()
                    # 2. 去掉结尾等号（防止干扰 @ 符号匹配）
                    clean_auth = b64_auth.replace("=", "")
                    # 3. 补一个冒号（伪装成“用户:密码”结构，骗过 v2rayN 解析器）
                    safe_auth = clean_auth + ":"
                else:
                    # 简单的 dongtaiwang.com 直接用明文，识别最快
                    safe_auth = auth
                
                # 构造最终的标准化链接
                link = f"hysteria2://{safe_auth}@{clean_server}?sni={sni}&insecure=1&allowInsecure=1#{name}"
                all_links.append(link)
                print(f"成功抓取: {name}")
            else:
                print(f"源失效 ({r.status_code}): {name}")
        except Exception as e:
            print(f"请求出错 ({name}): {e}")
            continue
            
    return all_links

if __name__ == "__main__":
    nodes = fetch_all_nodes()
    if nodes:
        with open("nodes.txt", "w", encoding="utf-8") as f:
            # 换行排列，确保 v2rayN 批量导入顺滑
            f.write("\n".join(nodes))
        print(f"\n任务完成：已更新 {len(nodes)} 个节点到 nodes.txt")
