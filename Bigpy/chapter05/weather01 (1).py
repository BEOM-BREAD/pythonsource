from bs4 import BeautifulSoup
import urllib.request as req
import simplejson as json
import os

#데이터 수집 (https://www.weather.go.kr/w/pop/rss-guide.do)

def fetch_weather_xml(url, save_path):
    # 실제 기상청 서버에 요청해서 xml을 받아오고 파일로 저장
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36"
    }
    res=req.urlopen(req.Request(url, headers=headers)).read().decode('utf-8')

    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(res)

    return res

def main():
    url = "https://www.kma.go.kr/repositary/xml/fct/mon/img/fct_mon1rss_108_20250814.xml"

    base_dir = "C:/source/pythonsource/Bigpy/Py_Scrap/data"
    save_path = os.path.join(base_dir, "weather.xml")

    # 디렉토리 생성 (존재하면 그냥 넘어감)
    os.makedirs(base_dir, exist_ok=True)

    # 실제 기상청 서버에서 XML 가져와서 저장
    xml_content = fetch_weather_xml(url, save_path)

    # XML 파싱
    soup=BeautifulSoup(xml_content, 'html.parser')

    # 제목 출력
    #title1 = soup.find("title").string
    #title2 = soup.find("title").text
    title = soup.find("title").get_text()
    print(f"제목: {title}")
    print("-" * 40)

    # 주차별 기간과 날씨 추출
    weeks=soup.find_all("week")
    weather_data = []
    json_data = {
        "title": title,
        "weeks": []
    }

    for i, week in enumerate(weeks, 1):
        period_tag=week.find(f"week{i}_period")
        weather_tag=week.find(f"week{i}_weather_review")

        if period_tag is None or weather_tag is None:
            continue

        period=period_tag.get_text(strip=True)
        weather=weather_tag.get_text(separator="\n",strip=True)

        print(f"{i}주차: {period}")
        print(f"날씨: {weather}")
        print()

        weather_data.append(f"{i}주차: {period}\n날씨: {weather}\n")

        json_data["weeks"].append({
            "week": i,
            "period": period,
            "weather": weather
        })

    # 파일로 저장(text) 
    output_file=os.path.join(base_dir, "weather_report.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"{title}\n")
        f.write("=" * 40 + "\n\n")
        for data in weather_data:
            f.write(data+"\n")
    
    print(f"날씨 정보가 '{output_file}' 파일로 저장되었습니다.")

    # 파일로 저장 (json) — 반복문 끝난 뒤 한 번만
    json_file = os.path.join(base_dir, "weather_report.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"날씨 정보가 '{json_file}' 파일로 저장되었습니다.")

if __name__=="__main__":
    main()