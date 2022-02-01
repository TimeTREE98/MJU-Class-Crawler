import csv
import requests as r
from bs4 import BeautifulSoup as BS4

s = r.Session()
s.headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
}
data = {
    "attribute": "login_standby",
    "user_id": "명지대 아이디",
    "passwd": "명지대 비번",
}
servletHtml = (s.post("https://class.mju.ac.kr/sug/servlet", data=data)).text
servletSoup = BS4(servletHtml, "html.parser")
servletList = servletSoup.select("td > a")

f = open("./mjuSubject.csv", "w", newline="", encoding="utf-8-sig")
wr = csv.writer(f)
wr.writerow(
    [
        "과목",
        "학년",
        "강좌번호",
        "교과목명",
        "교과목번호",
        "학점",
        "시간",
        "담당교수",
        "단계",
        "시간및강의실",
        "비고",
    ]
)

for servlet in servletList:
    if "javascript:openWindowLecture" not in servlet.get("href"):
        continue
    test, small_tp, display_div, lect_dept = (
        servlet.get("href").split("('")[1].split("')")[0].split("','")
    )
    subjectUrl = f"https://class.mju.ac.kr/sug/servlet?attribute=lect_list&small_tp={small_tp}&display_div={display_div}&lect_dept={lect_dept}"
    subjectInfoHtml = (s.get(subjectUrl)).text
    subjectSoup = BS4(subjectInfoHtml, "html.parser")
    subjectsList = subjectSoup.select("tr")
    for subjects in subjectsList:
        if "건이 조회되었습니다" in subjects.text:
            continue
        학년 = (
            subjects.select("td")[0]
            .text.replace("\t", "")
            .replace("\r\n", "")
            .replace("\n", "")
        )
        강좌번호 = subjects.select("td")[1].text.replace("\t", "").replace("\r\n", "")
        교과목명 = subjects.select("td")[2].text.replace("\t", "").replace("\r\n", "")
        교과목번호 = subjects.select("td")[3].text.replace("\t", "").replace("\r\n", "")
        학점 = subjects.select("td")[4].text.replace("\t", "").replace("\r\n", "")
        시간 = subjects.select("td")[5].text.replace("\t", "").replace("\r\n", "")
        담당교수 = subjects.select("td")[6].text.replace("\t", "").replace("\r\n", "")
        단계 = subjects.select("td")[10].text.replace("\t", "").replace("\r\n", "")
        시간및강의실 = subjects.select("td")[11].text.replace("\t", "").replace("\r\n", "")
        비고 = subjects.select("td")[12].text.replace("\t", "").replace("\r\n", "")
        if "[신" in 학년:
            continue
        if "학년" in 학년:
            continue
        print(
            servlet.text,
            학년,
            강좌번호,
            교과목명,
            교과목번호,
            학점,
            시간,
            담당교수,
            단계,
            시간및강의실,
            비고,
        )
        wr.writerow(
            [
                servlet.text,
                학년,
                강좌번호,
                교과목명,
                교과목번호,
                학점,
                시간,
                담당교수,
                단계,
                시간및강의실,
                비고,
            ]
        )
