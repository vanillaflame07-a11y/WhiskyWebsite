from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

# -------------------------------
# 위스키 데이터
# -------------------------------
whiskies_data = [
    {
        "name": "글렌리벳 12년",
        "image": "https://placehold.co/400x400/FFD89C/6B4A00?text=Glenlivet",
        "flavor": ["과일", "플로럴"],
        "description": "가볍고 신선한 과일 향이 특징이며, 부드러운 목 넘김으로 위스키 입문자에게 사랑받는 싱글몰트입니다."
    },
    {
        "name": "글렌피딕 12년",
        "image": "https://placehold.co/400x400/D4F0BA/3C542E?text=Glenfiddich",
        "flavor": ["배", "사과", "오크"],
        "description": "싱글몰트의 대명사로 불리며, 신선한 과일과 미묘한 오크 향이 조화로운 부드러운 위스키입니다."
    },
    {
        "name": "발베니 더블우드 12년",
        "image": "https://placehold.co/400x400/E3C293/5F4628?text=Balvenie",
        "flavor": ["바닐라", "꿀", "셰리"],
        "description": "두 종류의 오크통에서 숙성하여 부드러운 바닐라와 달콤한 꿀, 약간의 셰리 향이 어우러지는 복합적인 맛이 매력적입니다."
    },
    {
        "name": "맥캘란 12년",
        "image": "https://placehold.co/400x400/A05C5C/301A1A?text=Macallan",
        "flavor": ["건과일", "견과류", "초콜릿"],
        "description": "강렬한 셰리 풍미가 특징이며, 풍부한 건과일과 초콜릿 향이 진하고 깊은 인상을 남기는 위스키입니다."
    },
    {
        "name": "탈리스커 10년",
        "image": "https://placehold.co/400x400/87B4C6/2A3B43?text=Talisker",
        "flavor": ["바닷바람", "피트", "스모키"],
        "description": "스카이 섬의 거친 자연을 닮은 강렬한 바닷바람과 후추 향, 은은한 스모키함이 공존하는 개성 있는 위스키입니다."
    },
    {
        "name": "라프로익 10년",
        "image": "https://placehold.co/400x400/808080/FFFFFF?text=Laphroaig",
        "flavor": ["피트", "스모키", "요오드"],
        "description": "세상에서 가장 강한 피트 위스키 중 하나로, 병원 소독약 같은 독특하고 강렬한 향이 매니아층을 형성하고 있습니다."
    },
    {
        "name": "야마자키 12년",
        "image": "https://placehold.co/400x400/F0E0D0/544C40?text=Yamazaki",
        "flavor": ["과일", "바닐라", "오크"],
        "description": "일본 위스키의 선구자로 부드럽고 섬세한 맛이 특징입니다. 과일과 오크의 풍미가 조화롭고 깔끔합니다."
    }
]

# -------------------------------
# 테스트 질문/점수/타입 데이터
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
# API 엔드포인트
# -------------------------------
@app.route("/api/whiskies")
def get_whiskies():
    return jsonify(whiskies_data)

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
