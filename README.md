# ln|f(x)| 의 극솟값 — 입체 풀이

2023학년도 6월 모의평가 28번을 three.js 입체 풀이 페이지로 만든 것입니다. `index.html` 을 브라우저(Chrome·Edge)로 엽니다. three.js·MathJax 는 CDN 에서 받으므로 인터넷이 필요합니다.

## 구성 (12단계)

| 단계 | 내용 | 가운데 그래프 |
|---|---|---|
| 1 문제 | 문제와 보기 | — |
| 2 조건 살펴보기 | (가)(나)(다) 한 줄 요약 | — |
| 3~4 STEP 1 | 겉함수 ln\|t\| 와 조건 (가), f 의 부호 | t = f(x), x = 1 에서 g 불연속 |
| 5~6 STEP 2 | 합성함수의 극값, \|g\| 극소 ⇒ 0 < f(2) ≤ 1 | x = 2 의 수평 접선, f(2) > 1 인 반례 곡선 |
| 7~9 STEP 3 | g = 0 ⇔ f = ±1, f(2) < 1 반례, f(2) = 1 | t = 1, t = −1 판과 교점 |
| 10~11 STEP 4 | f(x) = ½(x−2)²(x−3)+1, 극소점 8/3, 답 ln(25/27) | 극소점 (8/3, 25/27) |
| 12 | 전체 되돌아보기 | — |

그래프는 원문 TikZ 그림의 배치를 따릅니다. 위에는 가로축 t 위에 겉함수 y = ln|t| 를, 아래에는 x 축을 아래쪽으로 향하게 그려 속함수 t = f(x) 를 그리고, t = ±1 에서 점선으로 잇습니다. 곡선 튜브 반지름은 0.15 입니다.

곡선은 f(1) = 0, f′(2) = 0, f(2) = m 인 삼차함수 족에서 단계마다 m 을 바꿔 그립니다 (반례 m = 1.3, 0.75, 정답 m = 1).

## 조작

- → / Space 다음, ← 이전, Home 처음부터, "자동 재생" 버튼
- 끌기 회전, 휠 확대·축소, 오른쪽 끌기 이동, 두 번 클릭 원래 시점

## 글꼴 다시 넣기

문장이나 수식을 고친 뒤에는 화면에 쓰인 글자만 담은 글꼴 부분집합을 다시 넣어야 합니다.

```
py -3.12 build_fonts.py "C:\Users\user\.claude\skills\latex2three3d\fonts\NotoSansKR[wght].ttf" "C:\Users\user\.claude\skills\latex2three3d\fonts\GowunBatang-Bold.ttf"
```

글꼴은 SIL Open Font License (google/fonts ofl/notosanskr, ofl/gowunbatang) 입니다.

## 해설 음성

단계마다 Azure Neural 음성(`ko-KR-HyunsuMultilingualNeural`) 해설이 나옵니다. 전체 약 3분 50초입니다.

- 첫 클릭이나 키 입력 뒤부터 소리가 납니다 (브라우저 자동 재생 정책). 단계를 넘기면 그 단계의 해설이 처음부터 나옵니다.
- 오른쪽 위 "🔊 음성" 버튼으로 끄고 켭니다. 주소에 `?mute` 를 붙이면 꺼진 채로 시작합니다.
- "자동 재생"은 해설이 끝나고 1.6초 뒤에 다음 단계로 넘어갑니다.
- 음성 파일은 `audio/step00.mp3` ~ `step11.mp3` 입니다. 대본은 `make_voice.py` 의 `SCRIPT` 에 있고, 고친 뒤 아래를 실행하면 바뀐 단계만 다시 만듭니다.

```
py -3.12 make_voice.py
```

환경변수 `AZURE_SUBSCRIPTION_KEY`, `AZURE_SERVICE_REGION` 이 필요합니다. 키는 음성을 만들 때만 쓰고 페이지에는 들어가지 않습니다.
