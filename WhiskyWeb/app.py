import requests
import csv
import io
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

# -------------------------------
# 1. '웹에 게시'를 통해 생성된 CSV 링크를 여기에 붙여넣으세요.
# -------------------------------
SHEET_URL = "https://docs.google.com/spreadsheets/d/1HA055BZ-PsNbKgk8KjKCGsoBGJ-ahANAXxsoRGiW5XA/edit?usp=sharing"

# -------------------------------
# 2. 위스키 데이터를 구글 시트에서 가져오는 함수
# -------------------------------
def get_whiskies_from_sheet():
    """게시된 구글 시트 CSV 링크에서 위스키 데이터를 가져와 파싱합니다."""
    response = requests.get(SHEET_URL)
    response.raise_for_status()  # 요청이 실패하면 에러를 발생시킵니다.

    # CSV 데이터를 파이썬 딕셔너리 리스트로 변환합니다.
    csv_file = io.StringIO(response.content.decode('utf-8'))
    reader = csv.DictReader(csv_file)
    data = list(reader)

    # 프론트엔드가 사용할 수 있도록 'flavor' 항목을 문자열에서 리스트로 변환합니다.
    for item in data:
        if item.get('flavor'):
            item['flavor'] = [f.strip() for f in item['flavor'].split(',')]
    return data

# -------------------------------
# 3. 질문, 점수, 타입 데이터 (기존과 동일)
#    (이 데이터들도 위스키처럼 별도 시트로 만들어 가져올 수 있습니다.)
# -------------------------------
questions = [
    {
        "id": "q1",
        "text": "Q1. 지금 디저트를 고른다면?",
        "options": [
            {"value": "fruit", "label": "A. 과일 타르트 🍏"},
            {"value": "choco", "label": "B. 초콜릿 케이크 🍫"}
        ]
    },
    {
        "id": "q2",
        "text": "Q2. 여행지에서 더 끌리는 풍경은?",
        "options": [
            {"value": "sea", "label": "A. 바닷바람 🌊"},
            {"value": "forest", "label": "B. 숲속의 나무 향기 🌲"}
        ]
    },
    {
        "id": "q3",
        "text": "Q3. 저녁에 불멍할 때 더 좋은 건?",
        "options": [
            {"value": "campfire", "label": "A. 은은한 모닥불 향 🔥"},
            {"value": "bbq", "label": "B. 강렬한 바비큐 연기 🍖"}
        ]
    },
    {
        "id": "q4",
        "text": "Q4. 카페에 가면 더 땡기는 건?",
        "options": [
            {"value": "latte", "label": "A. 카라멜 마키아토/바닐라 라떼 ☕"},
            {"value": "espresso", "label": "B. 진한 에스프레소 ☕"}
        ]
    },
    {
        "id": "q5",
        "text": "Q5. 술 마신 뒤 어떤 느낌이 더 좋아요?",
        "options": [
            {"value": "light", "label": "A. 산뜻하게 사라지는 여운 🌬️"},
            {"value": "heavy", "label": "B. 진하게 오래 남는 여운 🕰️"}
        ]
    },
    {
        "id": "q6",
        "text": "Q6. 파티에서 내가 고를 안주는?",
        "options": [
            {"value": "popcorn", "label": "A. 구운 옥수수, 캐러멜 팝콘 🍿"},
            {"value": "nuts", "label": "B. 구운 견과류, 치즈 🧀"}
        ]
    }
]

scores = {
    "fruit": {"fruit": 2, "japan": 1},
    "choco": {"dried": 2, "nutty": 1},
    "sea": {"sea": 2, "smoky_light": 1},
    "forest": {"vanilla": 2, "spicy": 1},
    "campfire": {"smoky_light": 2, "vanilla": 1},
    "bbq": {"smoky_heavy": 3},
    "latte": {"vanilla": 2, "bourbon": 1},
    "espresso": {"nutty": 2, "spicy": 1},
    "light": {"fruit": 2, "japan": 1},
    "heavy": {"dried": 2, "smoky_heavy": 1},
    "popcorn": {"bourbon": 2, "vanilla": 1},
    "nuts": {"nutty": 2, "spicy": 1}
}

whisky_types = {
    "fruit": "가볍고 달콤한 과일 타입 (글렌리벳 12, 글렌피딕 12 등)",
    "vanilla": "부드러운 바닐라·꿀 타입 (발베니 더블우드, 아벨라워 12 등)",
    "nutty": "고소·견과·구운 빵 타입 (글렌드로낙 12, 맥캘란 12 등)",
    "spicy": "스파이시·따뜻한 타입 (글렌드로낙 15, 맥캘란 셰리 오크 등)",
    "dried": "진한 과일잼·건과일 타입 (글렌드로낙 18, 아벨라워 아부나흐 등)",
    "sea": "바닷바람·짭짤한 타입 (탈리스커 10, 올드 풀트니 등)",
    "smoky_light": "은은한 스모키 타입 (하이랜드 파크 12, 보모어 12 등)",
    "smoky_heavy": "강렬한 스모키/피트 타입 (라프로익 10, 라가불린 16, 아드벡 10 등)",
    "bourbon": "미국 버번 타입 (메이커스 마크, 버팔로 트레이스 등)",
    "japan": "일본 위스키 타입 (야마자키 12, 하쿠슈 등)"
}

# -------------------------------
# 4. API 엔드포인트
# -------------------------------
@app.route("/api/whiskies")
def get_whiskies():
    try:
        whiskies_data = get_whiskies_from_sheet()
        return jsonify(whiskies_data)
    except requests.RequestException as e:
        # 네트워크 에러 등 URL 요청 실패 시
        return jsonify({"error": f"Failed to fetch data from Google Sheets: {e}"}), 503
    except Exception as e:
        # 데이터 처리 중 에러 발생 시
        return jsonify({"error": f"An error occurred while processing data: {e}"}), 500

@app.route("/api/questions")
def get_questions():
    return jsonify(questions)

@app.route("/api/scores")
def get_scores():
    return jsonify(scores)

@app.route("/api/whiskytypes")
def get_whiskytypes():
    return jsonify(whisky_types)

# -------------------------------
# 기본 루트에서 index.html 제공
# -------------------------------
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
