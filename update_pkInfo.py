import requests
import json
import os
import re

if "JD_COOKIE" in os.environ:
    secret = os.environ["JD_COOKIE"]
    pt_pin = re.findall(r'pt_pin=(.*?)&', secret)[0]
    pt_key = re.findall(r'pt_key=(.*?)$', secret)[0]
    cookies = {"pt_pin": pt_pin, "pt_key": pt_key}


def getTemplate(cookies, functionId, body):
    headers = {
        'User-Agent': 'jdapp;iPhone;9.0.8;13.6;Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Host': 'api.m.jd.com',
        'Referer': 'https://jdsupermarket.jd.com/game',
        'Origin': 'https://jdsupermarket.jd.com',
    }

    params = (
        ('appid', 'jdsupermarket'),
        ('functionId', functionId),
        ('clientVersion', '8.0.0'),
        ('client', 'm'),
        ('body', json.dumps(body)),
    )

    response = requests.get('https://api.m.jd.com/api',
                            headers=headers, params=params, cookies=cookies)
    return response.json()


data = getTemplate(cookies, "smtg_getTeamPkDetailInfo", {})[
    "data"]["result"]
if data["joinStatus"] == 0:
    exit()

info = {
    "pkActivityId": data["pkActivityId"],
    "teamId": data["teamId"],
    "inviteCode": ["IhM_beyxYPwg82i6iw", "YF5-KbvnOA", "eU9YaLm0bq4i-TrUzSUUhA"]
}

with open("jd_smPkInfo.json", "r") as f:
    old_data = json.load(f)


if info["pkActivityId"] == old_data["pkActivityId"]:
    print("pkActivityId 没有变化")
else:
    print("pkActivityId 更新", info["pkActivityId"])
    with open("jd_smPkInfo.json", "w") as f:
        json.dump(info, f)
        print("持久化成功")
