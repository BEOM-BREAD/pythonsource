# Chapter03. Gradio 실습 — 강의 자료

> Jupyter Notebook 환경 · Gradio로 웹 인터페이스 만들기 · 10개 예제 (하 7 + 중 3)

---

# Part 1. Gradio 설치 및 환경 설정 (매우 상세)

## 1-1. 사전 조건 확인

Chapter02에서 만든 `pyscience` 가상환경을 그대로 사용합니다. 새 터미널을 열 때마다 아래 절차를 먼저 확인하세요.

```bash
# 1) 프로젝트 폴더로 이동
cd /c/pyscience

# 2) 가상환경 활성화 (Git Bash 기준)
source ./.venv/Scripts/activate
```

프롬프트 앞에 `(.venv)`가 붙어야 정상입니다. 안 붙으면 Chapter01~02에서 다룬 가상환경 활성화 문제를 먼저 해결하세요.

## 1-2. Gradio 설치

```bash
uv pip install gradio
```

설치가 끝나면 버전을 확인합니다.

```bash
python -c "import gradio as gr; print(gr.__version__)"
```

숫자(예: `6.26.0`)가 출력되면 정상 설치된 것입니다. 에러가 나면 가상환경이 활성화된 상태인지(`(.venv)` 표시) 다시 확인하세요.

## 1-3. VSCode에서 chapter03 폴더 및 노트북 준비

1. `dataScience` 폴더 안에 `chapter03` 폴더 생성
2. `chapter03` 폴더 안에 `.ipynb` 파일 생성 (예: `ex01_hello_gradio.ipynb`)
3. 노트북 우측 상단에서 커널을 **Python (pyscience)**로 선택 (Chapter02에서 등록한 커널 그대로 사용)

## 1-4. 첫 실행 테스트

아래 코드를 셀에 입력하고 `Shift + Enter`로 실행해봅니다.

```python
import gradio as gr

def greet(name):
    return f"안녕하세요, {name}님!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()
```

**정상이라면:**
- 셀 아래에 텍스트 입력창과 "Submit" 버튼이 있는 화면이 바로 나타납니다 (`inline=True`가 기본값이라 노트북 안에 임베드됨).
- 이름을 입력하고 제출하면 인사말이 출력됩니다.

## 1-5. 실습 중 반드시 지켜야 할 습관 — `demo.close()`

Gradio는 `launch()`할 때마다 **로컬 포트(기본 7860)를 하나씩 점유**합니다. 노트북에서 셀을 여러 번 실행하다 보면 이전 데모가 안 꺼진 채로 새 데모가 또 열려서 포트가 계속 쌓이고, 결국 아래와 같은 에러가 날 수 있습니다.

```
OSError: Cannot find empty port in range: 7860-7860.
```

**해결책**: 확인이 끝난 데모는 아래 코드로 꺼주는 습관을 들이세요.

```python
demo.close()
```

이 강의자료의 모든 예제 노트북 마지막 셀에 `demo.close()` 안내 주석을 넣어뒀습니다.

## 1-6. 여러 명이 동시에 실습할 때 — 포트 충돌 방지

학생들이 각자 노트북에서 동시에 `launch()`를 실행하면 포트(7860)가 겹칠 수 있습니다. 이럴 땐 `server_port`를 학생마다 다르게 지정하세요.

```python
demo.launch(server_port=7861)  # 학생 A
demo.launch(server_port=7862)  # 학생 B
```

## 1-7. 외부 브라우저에서 열고 싶을 때 (선택)

노트북 안이 아니라 별도 브라우저 창에서 보고 싶다면:

```python
demo.launch(inline=False)
```

실행하면 터미널/출력창에 `http://127.0.0.1:7860` 같은 링크가 뜨는데, 이걸 클릭하면 브라우저에서 열립니다.

## 1-8. 외부에서 접속 가능한 임시 링크 만들기 (선택, 주의 필요)

```python
demo.launch(share=True)
```

- 72시간 동안 유효한 공개 링크(`https://xxxx.gradio.live`)가 생성되어, 외부에서도 접속 가능합니다.
- 데모/발표용으로는 유용하지만, **DB 접속 정보가 담긴 예제(ex10)에서는 사용을 권장하지 않습니다.** 개인 서버가 인터넷에 노출되는 것이므로 강의 중 이 옵션은 신중하게 안내해주세요.

## 1-9. 자주 발생하는 에러 체크리스트

| 증상 | 원인 | 해결 |
|---|---|---|
| `ModuleNotFoundError: No module named 'gradio'` | 설치 안 됨 또는 잘못된 커널 선택 | `.venv` 활성화 후 재설치, 커널을 `Python (pyscience)`로 재선택 |
| `OSError: Cannot find empty port` | 이전 데모가 안 꺼진 채 누적됨 | `demo.close()` 습관화, 최후 수단으로 커널 재시작(Restart Kernel) |
| 화면이 안 뜨고 빈 셀만 보임 | `inline=True` 렌더링 지연, 또는 브라우저 확장 프로그램 충돌 | 몇 초 대기 후 재실행, 그래도 안 되면 `inline=False`로 전환해 브라우저에서 확인 |
| 이미지 업로드 후 에러 | 컴포넌트가 기대하는 배열 형태(numpy)와 실제 처리 코드 불일치 | `input_image.shape`를 출력해서 실제 들어온 형태 확인 |
| ex10에서 `ORA-01017` 등 DB 에러 | Chapter02에서 겪은 것과 동일한 원인 | Chapter02 트러블슈팅 표 참고 (계정/비밀번호, PDB 이름 등) |
| 버튼을 눌러도 반응 없음 (`gr.Blocks` 사용 시) | `.click()` 이벤트 연결 누락 | 버튼 변수에 `.click(fn=..., inputs=..., outputs=...)`가 제대로 연결됐는지 확인 |

---

# Part 2. 예제 (10개 = 하 7 + 중 3)

## 예제01 (하). Hello Gradio — 첫 인터페이스 만들기

**파일명:** `ex01_hello_gradio.ipynb`

### 🎯 학습 목표
- `gr.Interface`로 가장 기본적인 웹 인터페이스를 만드는 흐름을 익힌다.
- "함수 하나 → 입력창 하나 → 출력창 하나"라는 Gradio의 기본 구조를 이해한다.

### 💡 강의 포인트
- Gradio의 핵심은 **"평범한 파이썬 함수를 웹 화면으로 자동 변환해준다"**는 것.
- `demo.launch()`를 실행하면 로컬 서버가 켜지고, 노트북 안에 화면이 바로 임베드됩니다.

### 💻 코드
```python
import gradio as gr

def greet(name):
    return f"안녕하세요, {name}님! 반갑습니다."

demo = gr.Interface(
    fn=greet,
    inputs="text",
    outputs="text",
    title="첫 Gradio 인터페이스",
    description="이름을 입력하면 인사말을 보여줍니다.",
)
demo.launch()
```
```python
# demo.close()
```

### ❓ 생각해볼 질문
1. `inputs="text"` 대신 `inputs="number"`로 바꾸면 화면이 어떻게 달라질까?
2. `title`과 `description`을 지우면 화면에서 무엇이 사라질까?

---

## 예제02 (하). 텍스트 변환기 — 여러 출력 한 번에 보여주기

**파일명:** `ex02_텍스트_변환기.ipynb`

### 🎯 학습 목표
- 하나의 입력으로 **여러 개의 결과**를 동시에 보여주는 방법을 익힌다.

### 💡 강의 포인트
- 함수가 값을 여러 개 `return`하면 `outputs` 리스트 순서와 1:1로 매칭됩니다.

### 💻 코드
```python
import gradio as gr

def transform_text(sentence):
    upper_text = sentence.upper()
    lower_text = sentence.lower()
    reversed_text = sentence[::-1]
    length = len(sentence)
    return upper_text, lower_text, reversed_text, length

demo = gr.Interface(
    fn=transform_text,
    inputs=gr.Textbox(label="문장을 입력하세요", placeholder="예: Hello Gradio"),
    outputs=[
        gr.Textbox(label="대문자 변환"),
        gr.Textbox(label="소문자 변환"),
        gr.Textbox(label="문자열 뒤집기"),
        gr.Number(label="글자 수"),
    ],
    title="텍스트 변환기",
)
demo.launch()
```

### ❓ 생각해볼 질문
1. 함수가 4개 값을 반환하는데 `outputs` 리스트가 3개뿐이라면 어떤 에러가 날까?
2. 컴포넌트를 직접 지정(`gr.Textbox(...)`)하는 것과 문자열(`"text"`)만 쓰는 것의 차이는?

---

## 예제03 (하). 숫자 계산기 — 다양한 입력 컴포넌트

**파일명:** `ex03_숫자_계산기.ipynb`

### 🎯 학습 목표
- `gr.Number`, `gr.Radio` 등 다양한 입력 컴포넌트를 사용해본다.

### 💡 강의 포인트
- 0으로 나누기 같은 예외 상황을 미리 처리하는 방어적 코딩 습관을 짚어주기 좋은 예제.

### 💻 코드
```python
import gradio as gr

def calculate(num1, num2, operator):
    if operator == "덧셈 (+)":
        result = num1 + num2
    elif operator == "뺄셈 (-)":
        result = num1 - num2
    elif operator == "곱셈 (*)":
        result = num1 * num2
    elif operator == "나눗셈 (/)":
        if num2 == 0:
            return "0으로는 나눌 수 없습니다!"
        result = num1 / num2
    else:
        result = "알 수 없는 연산자"
    return f"결과 : {result}"

demo = gr.Interface(
    fn=calculate,
    inputs=[
        gr.Number(label="첫 번째 숫자"),
        gr.Number(label="두 번째 숫자"),
        gr.Radio(["덧셈 (+)", "뺄셈 (-)", "곱셈 (*)", "나눗셈 (/)"], label="연산자를 선택하세요"),
    ],
    outputs=gr.Textbox(label="계산 결과"),
    title="간단한 숫자 계산기",
)
demo.launch()
```

### ❓ 생각해볼 질문
1. `gr.Radio` 대신 `gr.Dropdown`을 쓰면 화면이 어떻게 달라 보일까?
2. 0으로 나누는 예외 처리를 빼면 어떤 에러 화면이 뜰까?

---

## 예제04 (하). 이미지 업로드 + 흑백 변환기

**파일명:** `ex04_이미지_흑백변환.ipynb`

### 🎯 학습 목표
- `gr.Image`로 이미지를 업로드받고 처리 결과를 다시 이미지로 보여주는 흐름을 익힌다.

### 💡 강의 포인트
- Gradio는 이미지를 기본적으로 **numpy 배열**로 받아옵니다.

### 💻 코드
```python
import gradio as gr
import numpy as np

def to_grayscale(input_image):
    gray = np.dot(input_image[..., :3], [0.299, 0.587, 0.114])
    gray_image = np.stack([gray, gray, gray], axis=-1).astype(np.uint8)
    return gray_image

demo = gr.Interface(
    fn=to_grayscale,
    inputs=gr.Image(label="원본 이미지 업로드"),
    outputs=gr.Image(label="흑백 변환 결과"),
    title="이미지 흑백 변환기",
)
demo.launch()
```

### ❓ 생각해볼 질문
1. R,G,B 가중치를 전부 0.333(균등)으로 바꾸면 결과가 어떻게 달라질까?
2. 이미지 대신 "이미지 크기"만 텍스트로 알려주는 함수로 바꾸려면?

---

## 예제05 (하). 배달 메뉴 가격 계산기 — Chapter02 데이터 재활용

**파일명:** `ex05_메뉴_가격계산기.ipynb`

### 🎯 학습 목표
- `gr.Dropdown` + `gr.Slider` 조합으로 실시간 갱신 인터페이스를 만든다.

### 💡 강의 포인트
- 지금은 딕셔너리로 가격을 고정했지만, ex10에서 실제 Oracle DB로 바꿔서 연결합니다.

### 💻 코드
```python
import gradio as gr

menu_prices = {
    "떡볶이": 9000, "치킨": 22000, "피자": 25000,
    "짜장면": 8000, "마라탕": 13000, "돈까스": 11000,
}

def calculate_total(menu, quantity):
    unit_price = menu_prices[menu]
    total = unit_price * quantity
    return f"{menu} {quantity}개 주문 -> 총 결제 금액 : {total:,}원"

demo = gr.Interface(
    fn=calculate_total,
    inputs=[
        gr.Dropdown(list(menu_prices.keys()), label="메뉴 선택"),
        gr.Slider(minimum=1, maximum=10, step=1, label="수량"),
    ],
    outputs=gr.Textbox(label="주문 요약"),
    title="배달 메뉴 가격 계산기",
)
demo.launch()
```

### ❓ 생각해볼 질문
1. `Slider`의 `step` 값을 2로 바꾸면 수량을 몇 개씩 조절하게 될까?
2. 메뉴를 2개 이상 동시에 선택해서 합산하려면 어떤 컴포넌트로 바꿔야 할까? (`gr.CheckboxGroup` 힌트)

---

## 예제06 (하). 에코 챗봇 — ChatInterface 맛보기

**파일명:** `ex06_에코_챗봇.ipynb`

### 🎯 학습 목표
- `gr.ChatInterface`로 대화형 채팅 화면을 만들어본다.

### 💡 강의 포인트
- 함수 안 로직만 AI 모델 호출로 바꾸면 진짜 챗봇이 됩니다.

### 💻 코드
```python
import gradio as gr

def echo_bot(message, history):
    return f"너가 말한 건: '{message}' 이지?"

demo = gr.ChatInterface(
    fn=echo_bot,
    title="에코 챗봇",
    description="입력한 말을 그대로 따라 하는 간단한 챗봇입니다.",
)
demo.launch()
```

### ❓ 생각해볼 질문
1. `history`를 실제로 활용해서 "지금까지 몇 번 대화했는지" 세는 챗봇으로 바꾸려면?
2. `gr.Interface`와 `gr.ChatInterface`는 화면 모양이 어떻게 다를까?

---

## 예제07 (하). 카테고리별 요약 정보 조회기

**파일명:** `ex07_카테고리_요약조회.ipynb`

### 🎯 학습 목표
- 딕셔너리로 "선택한 항목에 맞는 정보"를 찾아 보여주는 함수를 만든다.

### 💡 강의 포인트
- 구조 자체는 이후 Oracle DB 조회 결과를 보여주는 방식(ex10)과 동일합니다.

### 💻 코드
```python
import gradio as gr

category_summary = {
    "분식": {"평균가격": 8500,  "평균평점": 4.3, "인기메뉴": "떡볶이"},
    "치킨": {"평균가격": 22000, "평균평점": 4.7, "인기메뉴": "양념치킨"},
    "피자": {"평균가격": 25500, "평균평점": 4.2, "인기메뉴": "포테이토피자"},
    "중식": {"평균가격": 10000, "평균평점": 4.3, "인기메뉴": "마라탕"},
    "일식": {"평균가격": 12000, "평균평점": 4.4, "인기메뉴": "초밥세트"},
}

def show_summary(category):
    info = category_summary[category]
    return info["평균가격"], info["평균평점"], info["인기메뉴"]

demo = gr.Interface(
    fn=show_summary,
    inputs=gr.Dropdown(list(category_summary.keys()), label="카테고리 선택"),
    outputs=[
        gr.Number(label="평균 가격(원)"),
        gr.Number(label="평균 평점"),
        gr.Textbox(label="인기 메뉴"),
    ],
    title="카테고리별 요약 조회기",
)
demo.launch()
```

### ❓ 생각해볼 질문
1. 딕셔너리에 "주문건수" 항목을 추가하려면 `outputs`에는 무엇을 더해야 할까?
2. 정적 딕셔너리 대신 pandas DataFrame에서 값을 뽑아오도록 바꾸려면?

---

## 예제08 (중). gr.Blocks — 레이아웃을 직접 설계하는 BMI 계산기

**파일명:** `ex08_blocks_BMI계산기.ipynb`

### 🎯 학습 목표
- `gr.Blocks`로 컴포넌트 배치를 직접 설계하는 법을 익힌다.
- 버튼 클릭 이벤트(`.click()`)로 원하는 타이밍에 함수를 실행시킨다.

### 💡 강의 포인트
- `gr.Interface`는 흐름이 고정되어 있지만, `gr.Blocks`는 자유롭게 설계할 수 있음.
- `gr.Row()`, `gr.Column()`으로 화면을 가로/세로로 나누는 감각이 핵심.

> ⚠️ 여기서부터 난이도가 한 단계 올라갑니다.

### 💻 코드
```python
import gradio as gr

def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    if bmi < 18.5:
        category = "저체중"
    elif bmi < 23:
        category = "정상"
    elif bmi < 25:
        category = "과체중"
    else:
        category = "비만"
    return f"{bmi:.1f}", category

with gr.Blocks(title="BMI 계산기") as demo:
    gr.Markdown("## 📏 BMI(체질량지수) 계산기")

    with gr.Row():
        height_input = gr.Number(label="키(cm)")
        weight_input = gr.Number(label="몸무게(kg)")

    calc_btn = gr.Button("계산하기")

    with gr.Row():
        bmi_output = gr.Textbox(label="BMI 수치")
        category_output = gr.Textbox(label="체중 분류")

    calc_btn.click(
        fn=calculate_bmi,
        inputs=[height_input, weight_input],
        outputs=[bmi_output, category_output],
    )

demo.launch()
```

### ❓ 생각해볼 질문
1. `calc_btn.click(...)` 코드를 지우면 왜 버튼을 눌러도 반응이 없을까?
2. `gr.Row()` 대신 `gr.Column()`으로 바꾸면 배치가 어떻게 달라질까?
3. `gr.Interface`로는 왜 이런 자유로운 레이아웃을 만들기 어려울까?

---

## 예제09 (중). CSV 업로드 → pandas 표 + matplotlib 그래프 대시보드

**파일명:** `ex09_csv_업로드_대시보드.ipynb`

### 🎯 학습 목표
- `gr.File`로 파일을 업로드받아 pandas로 읽는 흐름을 익힌다.
- 표(DataFrame)와 그래프(matplotlib)를 동시에 출력하는 법을 익힌다.

### 💡 강의 포인트
- Gradio는 matplotlib `Figure`를 그대로 `outputs`에 넣으면 이미지처럼 그려줍니다.
- `gr.File`은 업로드 파일의 경로(path)를 문자열로 돌려준다는 점이 특징.

### 💻 코드
```python
import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rc('font', family='Malgun Gothic')
mpl.rc('axes', unicode_minus=False)

def analyze_csv(file):
    df = pd.read_csv(file.name, encoding="utf-8-sig")
    numeric_df = df.select_dtypes(include="number")
    summary_table = numeric_df.describe().round(2)

    fig, ax = plt.subplots(figsize=(6, 4))
    if len(numeric_df.columns) > 0:
        first_col = numeric_df.columns[0]
        ax.hist(numeric_df[first_col], bins=10, color="skyblue", edgecolor="black")
        ax.set_title(f"{first_col} 분포")
    else:
        ax.text(0.5, 0.5, "숫자형 컬럼이 없습니다", ha="center")

    return summary_table, fig

demo = gr.Interface(
    fn=analyze_csv,
    inputs=gr.File(label="CSV 파일 업로드", file_types=[".csv"]),
    outputs=[
        gr.Dataframe(label="요약 통계표"),
        gr.Plot(label="분포 히스토그램"),
    ],
    title="CSV 업로드 분석 대시보드",
    description="CSV 파일을 올리면 요약 통계와 히스토그램을 함께 보여줍니다.",
)
demo.launch()
```

### ❓ 생각해볼 질문
1. 숫자형 컬럼이 여러 개면 왜 첫 번째 컬럼만 그릴까? 전체를 그리려면?
2. `gr.Dataframe`과 `gr.Plot`을 한 화면에 같이 두면 어떤 점이 편리할까?

---

## 예제10 (중). Oracle DB 실시간 조회 대시보드 — Chapter02 종합

**파일명:** `ex10_oracle_실시간대시보드.ipynb`

### 🎯 학습 목표
- 카테고리를 선택하면 즉시 Oracle DB에 쿼리를 날려 결과를 보여주는 흐름을 만든다.
- Chapter02(Oracle)와 Chapter03(Gradio)을 하나로 합치는 종합 실습.

### 💡 강의 포인트
- `with` 구문으로 매번 접속/해제하는 패턴은 Chapter02에서 배운 것을 재사용.
- `DELIVERY_ORDERS` 테이블과 `.env` 설정이 필요합니다.

> ⚠️ Chapter03에서 가장 난이도가 높은 예제입니다.

### 💻 코드
```python
import os
from dotenv import load_dotenv
import oracledb
import pandas as pd
import gradio as gr
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rc('font', family='Malgun Gothic')
mpl.rc('axes', unicode_minus=False)

load_dotenv()
USER = os.getenv("ORACLE_USER")
PASSWORD = os.getenv("ORACLE_PASSWORD")
DSN = os.getenv("ORACLE_DSN")

def query_category(category):
    # 바인드 변수(:category)로 SQL Injection을 방지합니다.
    query = "SELECT * FROM DELIVERY_ORDERS WHERE CATEGORY = :category"
    with oracledb.connect(user=USER, password=PASSWORD, dsn=DSN) as conn:
        df = pd.read_sql(query, conn, params={"category": category})

    if len(df) == 0:
        empty_df = pd.DataFrame({"안내": ["해당 카테고리의 데이터가 없습니다."]})
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "데이터 없음", ha="center")
        return empty_df, fig

    summary = df[["PRICE", "RATING"]].describe().round(1)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(df["PRICE"], bins=8, color="salmon", edgecolor="black")
    ax.set_title(f"'{category}' 카테고리 가격 분포 (n={len(df)}건)")
    ax.set_xlabel("가격")
    ax.set_ylabel("건수")

    return summary, fig

with gr.Blocks(title="배달 주문 실시간 대시보드") as demo:
    gr.Markdown("## 🍽️ 카테고리별 주문 데이터 실시간 조회")
    gr.Markdown("카테고리를 선택하면 Oracle DB에서 즉시 데이터를 조회합니다.")

    with gr.Row():
        category_dropdown = gr.Dropdown(["분식", "치킨", "피자", "중식", "일식"], label="카테고리 선택")
        search_btn = gr.Button("조회하기")

    with gr.Row():
        summary_output = gr.Dataframe(label="요약 통계")
        plot_output = gr.Plot(label="가격 분포")

    search_btn.click(
        fn=query_category,
        inputs=category_dropdown,
        outputs=[summary_output, plot_output],
    )

demo.launch()
```

### ❓ 생각해볼 질문
1. `:category` 바인드 변수 대신 `f"WHERE CATEGORY = '{category}'"`처럼 문자열을 직접 끼워 넣으면 어떤 보안 문제가 생길까? (SQL Injection)
2. 버튼을 누를 때마다 매번 새로 DB에 접속하는 지금 방식은, 사용자가 100번 누르면 어떤 부담이 생길까? (Chapter04 예고)

---

# 정리

| 예제 | 난이도 | 핵심 컴포넌트/개념 | Chapter02와의 연결 |
|---|---|---|---|
| ex01 | 하 | `gr.Interface` 기본 | - |
| ex02 | 하 | 다중 출력 | - |
| ex03 | 하 | `gr.Number`, `gr.Radio` | - |
| ex04 | 하 | `gr.Image` | - |
| ex05 | 하 | `gr.Dropdown`, `gr.Slider` | 배달 메뉴 데이터 |
| ex06 | 하 | `gr.ChatInterface` | - |
| ex07 | 하 | 다중 출력 + 딕셔너리 조회 | 카테고리 요약 |
| ex08 | 중 | `gr.Blocks`, `.click()`, `Row/Column` | - |
| ex09 | 중 | `gr.File`, `gr.Dataframe`, `gr.Plot` | Chapter01 CSV 재활용 |
| ex10 | 중 | Oracle 실시간 연동 + `gr.Blocks` | Chapter02 전체 종합 |
