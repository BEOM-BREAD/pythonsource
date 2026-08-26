import yt_dlp
import os
# pip install -U yt-dlp   (오래된 버전이면 봇 감지에 더 잘 걸림 -> 항상 최신 버전 유지 권장)

url = "https://www.youtube.com/watch?v=WJRQgGI83zU"

save_dir = "C:/source/pythonsource/Bigpy/Py_Scrap/"
os.makedirs(save_dir, exist_ok=True)  # 쿠키 저장용 폴더를 미리 만들어둠 (yt-dlp가 자동 생성 안 해줌)

ydl_opts = {
    'outtmpl': f'{save_dir}/%(title)s.%(ext)s',

    # 이 PC는 Firefox가 설치되어 있지 않아 cookiesfrombrowser 방식이 동작하지 않음
    # -> 크롬 확장 'Get cookies.txt LOCALLY'로 내보낸 cookies.txt를 직접 사용
    #    (브라우저 실행 여부, 종류와 무관하게 항상 동작하는 가장 안정적인 방법)
    'cookiefile': f'{save_dir}/cookies.txt',

    # ffmpeg가 없어도 동작하도록 병합이 필요 없는 단일 파일 포맷을 우선 선택
    # ffmpeg 설치 후에는 이 줄을 지우면 최고화질(영상+음성 병합)로 받아짐
    'format': 'best',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("동영상 다운로드 완료!")
