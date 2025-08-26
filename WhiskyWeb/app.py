# app.py

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

# Flask 앱 생성
app = Flask(__name__, static_folder="static")
# CORS(Cross-Origin Resource Sharing) 설정 - 다른 출처의 요청을 허용
CORS(app)

# 위스키 데이터 (기존 자바스크립트 데이터를 파이썬 딕셔너리 리스트로 변환)
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
    },
    {
        "name": "위스키 이름",
        "image": "https://placehold.co/400x400/F0E0D0/544C40?text=Yamaz",
        "flavor": ["과일", "바닐라"],
        "description": "위스키 설명"
    }
    
]

@app.route("/api/whiskies")
def get_whiskies():
    return jsonify(whiskies_data)


# 기본 루트에서 index.html 제공
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    

"""
    {
        "name": "위스키 이름",
        "image": "https://placehold.co/400x400/F0E0D0/544C40?text=Yamaz",
        "flavor": ["과일", "바닐라"],
        "description": "위스키 설명"
    }

"""
