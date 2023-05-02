import requests
from lxml import etree

urlbase = "https://pvp.qq.com/web201605/herolist.shtml"
henders = {
    # "cookie": "LW_sid=O1I6j7i1i4i630g6E4X1t6V8m3; LW_uid=M1t6l7F1Y4Z6p0Q6c4N1v63804; eas_sid=X19647E1T436s0D6X4P1M63857; eas_entry=https%3A%2F%2Fwww.google.com%2F; PTTuserFirstTime=1671408000000; PTTosSysFirstTime=1671408000000; PTTosFirstTime=1671408000000; ts_refer=www.google.com/; pgv_pvid=6416069124; ts_uid=8382959210; weekloop=0-0-0-52; ieg_ingame_userid=5qWHNKkUBz6OagLDJIIOAM4vCroXWUst; pvpqqcomrouteLine=index_herolist_herodetail_herodetail_herodetail_herodetail_index; tokenParams=%3FG_Biz%3D18%26tid%3D146986; pgv_info=ssid=s184938457&pgvReferrer=; isHostDate=19346; isOsSysDate=19346; isOsDate=19346; ts_last=pvp.qq.com/web201605/herolist.shtml; PTTDate=1671462175214",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
# 獲取所有index
resp = requests.get(urlbase, headers=henders)
e = etree.HTML(resp.text)
index: list = e.xpath("//div [@class='herolist-content']/ul//li/a/attribute::href")
# 轉換並封裝成list
index_list: list = []
for i in index:
    index_list.append(i.strip("herodetail.shtm/"))

# 遍歷替換url並發送請求
for i in index_list:
    # 把每個角色每個造型都薅下來
    for e in range(1, 8):
        d_img_resp = requests.get(f"https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{i}/{i}-bigskin-{e}.jpg",
                                  headers=henders).content
        # 如果找不到剛好字數19，找不到就直接結束這角色循環
        if len(d_img_resp) == 19:
            break
        # 如果找到了就寫入。
        else:
            with open(f"{i}-{e}.jpg", "wb") as f:
                f.write(d_img_resp)