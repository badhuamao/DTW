import requests
import json
import base64

URLS = [
    "https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/hysteria2/1/config.json",
    "https://gitlab.com/free9999/ipupdate/-/raw/master/backup/img/1/2/ipp/hysteria2/1/config.json"
]

def main():
    headers = {'User-Agent': 'Mozilla/5.0'}
    for url in URLS:
        try:
            r = requests.get(url, timeout=15, headers=headers, verify=False)
            if r.status_code == 200:
                data = r.json()
                auth = data['auth']
                server = data['server']
                sni = data['tls']['sni']
                # 转换成通用格式
                link = f"hysteria2://{auth}@{server}?sni={sni}&insecure=1&allowInsecure=1#AutoSync_Node"
                with open("nodes.txt", "w") as f:
                    f.write(link)
                print("Successfully synced.")
                return
        except:
            continue

if __name__ == "__main__":
    main()
