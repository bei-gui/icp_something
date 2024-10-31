import requests
import urllib.parse
from bs4 import BeautifulSoup
import time
import json

def main():
    while(True):
        print('''


    _                                         __  __    _            
   (_)________     _________  ____ ___  ___  / /_/ /_  (_)___  ____ _
  / / ___/ __ \   / ___/ __ \/ __ `__ \/ _ \/ __/ __ \/ / __ \/ __ `/
 / / /__/ /_/ /  (__  ) /_/ / / / / / /  __/ /_/ / / / / / / / /_/ / 
/_/\___/ .___/  /____/\____/_/ /_/ /_/\___/\__/_/ /_/_/_/ /_/\__, /  
      /_/                                                   /____/   

'''
)
        print(
            "1、企业名称(模糊查询\精准查询)\n"
            "2、域名\n"
            "3、IP反查域名\n"
            "q、退出程序\n"
        )
        choice = input("请选择查询方式：")
        if choice == "1":
            print(
                "1、模糊查询(最多显示100条）\n"
                "2、精准查询（读取org.txt）\n"
                )
            org = input("请选择查询方式：")
            if org == "1":
                keyword = input("请输入关键字：")
                org_icp_query(keyword)
            if org == "2":
                with open("org.txt", "r",encoding='utf-8') as f:
                    for line in f:
                        keyword = line.strip()
                        print(f"正在查询：{keyword}")
                        org_icp_query(keyword)
        if choice == "2":
            with open("domain.txt", "r",encoding='utf-8') as f:
                for line in f:
                    domain = line.strip()
                    print(f"正在查询：{domain}")
                    domain_icp_query(domain)
        if choice == "3":
            with open("ip.txt", "r",encoding='utf-8') as f:
                for line in f:
                    ip = line.strip()
                    print(f"正在查询：{ip}")
                    ip_domain_query(ip)
        if choice == "q":
            break
def org_icp_query(keyword):
    # 发送POST请求
    url = "https://api.uutool.cn/icp/search/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36",
        "Sec-Ch-Ua-Platform": "",
        "Origin": "https://uutool.cn",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://uutool.cn/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    data = {
        "keyword":keyword
    }
    response = requests.post(url, data=data, headers=headers)

    # 检查响应状态
    if response.status_code == 200:
        # 处理JSON数据
        json_data = response.json()
        if json_data["status"] == 1:
            # 提取所需参数值zha
            site_domains = []
            icp_orgs = []
            icp_nos = []

            with open("./org_icp.txt", "a") as f:
                for row in json_data["data"]["rows"]:
                    site_domain, icp_org, icp_no = row["site_domain"], row["icp_org"], row["icp_no"]
                    f.write(f"{site_domain} {icp_org} {icp_no}\n")
                    print(f"{site_domain} {icp_org} {icp_no}\n")
        else:
            print("查询失败，请检查API状态")
            print(json_data["status"])
    else:
        print(f"请求失败，状态码：{response.status_code}")
def domain_icp_query(domain):
    # 发送POST请求
    url = "https://api.uutool.cn/beian/icp/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36",
        "Sec-Ch-Ua-Platform": "",
        "Origin": "https://uutool.cn",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://uutool.cn/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    data = {
        "domain":domain
    }
    response = requests.post(url, data=data, headers=headers)

    # 检查响应状态
    if response.status_code == 200:
        # 处理JSON数据
        json_data = response.json()
        if json_data["status"] == 1:
            # 提取所需参数值
            domains = []
            icp_orgs = []
            icp_nos = []

            with open("./domain_icp.txt", "a") as f:
                    site_domain, icp_org, icp_no = json_data['data']["domain"], json_data['data']["icp_org"], json_data['data']["icp_no"]
                    f.write(f"{site_domain}\t{icp_org}\t{icp_no}\n")
                    print(f"{site_domain}\t{icp_org}\t{icp_no}\n")
        else:
            print("查询失败，请检查API状态")
            print(json_data["status"])
    else:
        print(f"请求失败，状态码：{response.status_code}")
def ip_domain_query(ip):
    url = "https://api.webscan.cc"
    headers = {
    "Origin": "https://www.webscan.cc",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.webscan.cc/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh"
    }
    data = {
            'action': 'query',
            'ip': ip 
        }
    response = requests.post(url, data=data, headers=headers)
    #soup = BeautifulSoup(response.content, 'html.parser')
    try:
        #title = soup.find('li', class_='J_link').find('span').get_text()
        #domain = soup.find('a', class_='domain').get('href')
        

        # 将响应体转换为Python对象
        response_body = response.text
        data = json.loads(response_body)
        print(data)
        if response_body != "null":
        # 遍历数据，提取title和ip
            for item in data:
                domain = item.get('domain')
                title = item.get('title')
                if title:# 如果标题不为空
                    with open("./ip_domain.txt", "a") as f:
                        f.write(f"{ip}\t{domain}\t{title}\n")
                        print(f"{ip}\t{domain}\t{title}\n")
                else:
                    break
 
    except AttributeError:
        print("未找到域名信息")
if __name__ == "__main__":
    main()
