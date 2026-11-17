"""단계별 해설 음성(mp3)을 Azure TTS 로 만든다.

사용법:  py -3.12 make_voice.py            (바뀐 대본만 다시 만든다)
         py -3.12 make_voice.py --all      (전부 다시 만든다)

환경변수 AZURE_SUBSCRIPTION_KEY, AZURE_SERVICE_REGION 이 필요하다. 키는 만들 때만 쓰고 페이지에는 들어가지 않는다.
결과: audio/step00.mp3 ~ step11.mp3, audio/manifest.json (대본 해시 → 바뀐 것만 다시 만들기)
"""
import hashlib
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

VOICE = "ko-KR-HyunsuMultilingualNeural"
RATE = "0%"

# 수식은 칠판을 읽듯 말로 바꾼다 (f(x) → 에프 엑스, ln|t| → 엘엔 절댓값 티)
SCRIPT = [
    # 0 문제
    "2023학년도 6월 모의평가 28번입니다. 최고차항의 계수가 2분의 1인 삼차함수 에프 엑스에 대하여, "
    "함수 지 엑스는 에프 엑스가 0이 아닐 때 엘엔 절댓값 에프 엑스이고, 에프 엑스가 0일 때 1입니다. "
    "조건 가, 나, 다를 만족시킬 때, 지 엑스의 극솟값을 구해 봅시다.",
    # 1 조건 살펴보기
    "조건을 하나씩 읽어 봅시다. 조건 가는, 지 엑스가 끊기는 곳이 엑스 이퀄 1 하나뿐이라는 뜻입니다. "
    "조건 나에서는 엑스 이퀄 2에서 지는 극대이고 절댓값 지는 극소이므로, 지 2는 0 이하여야 합니다. "
    "조건 다는, 에프 엑스가 1 또는 마이너스 1이 되는 곳이 모두 세 개라는 뜻입니다. 그래프를 그려서 한 단계씩 풀어 봅시다.",
    # 2 겉함수와 조건 (가)
    "위쪽 분홍색 곡선이 겉함수 와이 이퀄 엘엔 절댓값 티입니다. 티가 0에 가까워지면 음의 무한대로 발산하므로, "
    "지 엑스는 에프 엑스가 0인 점에서 불연속입니다. 삼차방정식 에프 엑스 이퀄 0은 실근을 적어도 하나 가지므로, "
    "조건 가에 의해 그 실근은 엑스 이퀄 1 하나뿐입니다.",
    # 3 f 의 부호
    "최고차항의 계수가 양수이므로, 엑스가 1보다 작으면 에프 엑스는 음수이고, 엑스가 1보다 크면 에프 엑스는 양수입니다. "
    "아래쪽 파란 곡선 티 이퀄 에프 엑스가 엑스 이퀄 1에서 한 번만 엑스 축을 가로지르는 것을 확인하세요.",
    # 4 합성함수의 극값
    "겉함수는 티가 양수인 범위에서 증가합니다. 따라서 합성함수의 극값에 의해, 엑스가 1보다 큰 범위에서 "
    "지의 극값은 속함수 에프의 극값과 같은 점에서 같은 종류로 생깁니다. 조건 나에서 지가 엑스 이퀄 2에서 극대이므로, "
    "에프도 엑스 이퀄 2에서 극대입니다.",
    # 5 |g| 극소
    "만약 지 2가 양수라면, 엑스 이퀄 2 근방에서 절댓값 지 엑스는 지 엑스와 같아서 극대가 됩니다. "
    "그러면 절댓값 지가 극소라는 조건에 어긋납니다. 따라서 지 2는 0 이하이고, 에프 2는 0보다 크고 1 이하입니다.",
    # 6 g = 0 ⇔ f = ±1
    "조건 다의 방정식 지 엑스 이퀄 0은 엘엔 절댓값 에프 엑스 이퀄 0, 곧 에프 엑스가 1 또는 마이너스 1인 것과 같습니다. "
    "티 이퀄 마이너스 1에서 내려온 점선처럼, 에프 엑스 이퀄 마이너스 1인 점은 엑스가 1보다 작은 범위에 하나뿐입니다.",
    # 7 f(2) < 1
    "에프 2가 1보다 작다면, 에프 엑스 이퀄 1인 점은 극소점 베타보다 오른쪽에 하나뿐입니다. "
    "그러면 실근은 모두 두 개여서 조건 다에 어긋납니다.",
    # 8 f(2) = 1
    "에프 2가 1이면, 엑스 이퀄 2와 베타보다 오른쪽의 한 점, 두 곳에서 에프 엑스가 1이 됩니다. "
    "마이너스 1이 되는 점까지 합쳐 실근이 세 개입니다. 따라서 에프 2는 1입니다.",
    # 9 f(x) 구하기
    "에프 엑스는 엑스 이퀄 2에서 극대이고 에프 2는 1이므로, 에프 엑스 마이너스 1은 엑스 마이너스 2의 제곱을 인수로 가집니다. "
    "에프 엑스 마이너스 1을 2분의 1 곱하기 엑스 마이너스 2의 제곱 곱하기 엑스 마이너스 씨로 놓고, "
    "에프 1 이퀄 0을 대입하면 씨는 3입니다.",
    # 10 답
    "중근 2와 단순근 3 사이의 극소점은 엑스 이퀄 3분의 8입니다. 에프 3분의 8은 1 더하기 2분의 1 곱하기 9분의 4 곱하기 "
    "마이너스 3분의 1, 곧 27분의 25입니다. 따라서 지 엑스의 극솟값은 엘엔 27분의 25, 정답은 5번입니다.",
    # 11 되돌아보기
    "처음부터 되돌아봅시다. 조건 가로 에프 엑스 이퀄 0의 실근이 1 하나임을, 조건 나로 에프 2가 1 이하임을, "
    "조건 다로 에프 2가 정확히 1임을 알았습니다. 그 결과 극솟값 엘엔 27분의 25를 얻었습니다.",
]


def tts(text: str, out: Path) -> None:
    key, region = os.environ["AZURE_SUBSCRIPTION_KEY"], os.environ["AZURE_SERVICE_REGION"]
    ssml = (f'<speak version="1.0" xml:lang="ko-KR"><voice name="{VOICE}">'
            f'<prosody rate="{RATE}">{escape(text)}</prosody></voice></speak>').encode("utf-8")
    req = urllib.request.Request(
        f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1", data=ssml, method="POST",
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/ssml+xml",
                 "X-Microsoft-OutputFormat": "audio-24khz-96kbitrate-mono-mp3", "User-Agent": "ln-abs-voice"})
    for attempt in range(6):   # 학교망 일시 오류 대비 재시도
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                out.write_bytes(r.read()); return
        except Exception as e:  # noqa: BLE001
            if attempt == 5: raise
            wait = 3 * 1.5 ** attempt
            print(f"  재시도 {attempt + 1} ({wait:.0f}초 뒤): {e}")
            time.sleep(wait)


def main() -> None:
    here = Path(__file__).resolve().parent
    adir = here / "audio"; adir.mkdir(exist_ok=True)
    mf = adir / "manifest.json"
    old = json.loads(mf.read_text(encoding="utf-8")) if mf.exists() else {}
    new = {}
    for i, text in enumerate(SCRIPT):
        name = f"step{i:02d}.mp3"; h = hashlib.sha1((VOICE + RATE + text).encode()).hexdigest()[:12]
        new[name] = h
        if "--all" not in sys.argv and old.get(name) == h and (adir / name).exists():
            continue
        tts(text, adir / name)
        print(f"{name}  {(adir / name).stat().st_size // 1024} KB")
    mf.write_text(json.dumps(new, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
