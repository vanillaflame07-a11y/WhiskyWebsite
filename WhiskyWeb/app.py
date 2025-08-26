# app.py — Google Sheets 공개 CSV를 "DB처럼" 읽는 버전 (flavor는 쉼표(,) 구분)
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os, time, csv, io, requests

app = Flask(__name__, static_folder="static")
CORS(app)

# ✅ 한글 JSON을 유니코드 이스케이프 없이, UTF-8로 내보내기
app.config["JSON_AS_ASCII"] = False
app.config["JSONIFY_MIMETYPE"] = "application/json; charset=utf-8"

# ====== 설정 ======
# 각 시트(탭)를 "웹에 게시 -> CSV"로 만든 URL을 Render 환경변수에 넣어두세요.
CSV_URLS = {
    "whiskies": os.getenv("WHISKIES_CSV"),
    "questions": os.getenv("QUESTIONS_CSV"),
    "options": os.getenv("OPTIONS_CSV"),
    "scores": os.getenv("SCORES_CSV"),
    "types": os.getenv("TYPES_CSV"),
}

# 캐시 TTL(초). Render 무료 플랜이면 너무 짧게 하지 말 것.
CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))

_cache = {
    "ts": 0.0,
    "whiskies": [],
    "questions": [],
    "scores": {},
    "types": {},
}

def _fetch_csv(url: str):
    """주어진 공개 CSV URL을 요청해서 Dict 리스트로 반환."""
    if not url:
        return []
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    r.encoding = "utf-8"   # ✅ 한글 깨짐 방지: UTF-8로 강제 지정
    f = io.StringIO(r.text)
    return list(csv.DictReader(f))

def _refresh_cache():
    rows_w = _fetch_csv(CSV_URLS["whiskies"])
    rows_q = _fetch_csv(CSV_URLS["questions"])
    rows_o = _fetch_csv(CSV_URLS["options"])
    rows_s = _fetch_csv(CSV_URLS["scores"])
    rows_t = _fetch_csv(CSV_URLS["types"])

    # --- whiskies ---
    whiskies = []
    for r in rows_w:
        # flavor: "과일,플로럴" 처럼 쉼표(,) 구분 → 리스트
        raw_flavor = r.get("flavor", "") or ""
        flavors = [x.strip() for x in raw_flavor.split(",")] if raw_flavor else []
        whiskies.append({
            "name": (r.get("name") or "").strip(),
            "image": (r.get("image") or "").strip(),
            "flavor": flavors,
            "description": (r.get("description") or "").strip(),
        })

    # --- questions + options 병합 ---
    opt_by_q = {}
    for o in rows_o:
        qid = (o.get("question_id") or "").strip()
        if not qid:
            continue
        opt_by_q.setdefault(qid, []).append({
            "value": (o.get("value") or "").strip(),
            "label": (o.get("label") or "").strip(),
        })

    questions = []
    for q in rows_q:
        qid = (q.get("id") or "").strip()
        if not qid:
            continue
        questions.append({
            "id": qid,
            "text": (q.get("text") or "").strip(),
            "options": opt_by_q.get(qid, [])
        })

    # --- scores: dict[answer_key] -> {type: score} ---
    scores = {}
    for s in rows_s:
        key = (s.get("answer_key") or "").strip()
        typ = (s.get("type") or "").strip()
        val_raw = (s.get("score") or "0").strip()
        if not key or not typ:
            continue
        try:
            val = int(float(val_raw))
        except:
            val = 0
        scores.setdefault(key, {})[typ] = val

    # --- whisky_types: dict[type] = description ---
    whisky_types = {}
    for t in rows_t:
        typ = (t.get("type") or "").strip()
        desc = (t.get("description") or "").strip()
        if typ:
            whisky_types[typ] = desc

    _cache.update({
        "ts": time.time(),
        "whiskies": whiskies,
        "questions": questions,
        "scores": scores,
        "types": whisky_types,
    })

def _ensure_cache():
    now = time.time()
    if _cache["ts"] == 0 or (now - _cache["ts"]) > CACHE_TTL:
        _refresh_cache()

# ====== API ======
@app.route("/api/whiskies")
def api_whiskies():
    _ensure_cache()
    return jsonify(_cache["whiskies"])

@app.route("/api/questions")
def api_questions():
    _ensure_cache()
    return jsonify(_cache["questions"])

@app.route("/api/scores")
def api_scores():
    _ensure_cache()
    return jsonify(_cache["scores"])

@app.route("/api/whiskytypes")
def api_types():
    _ensure_cache()
    return jsonify(_cache["types"])

# 간단한 상태 확인용
@app.route("/healthz")
def healthz():
    return jsonify({"ok": True, "cached_at": _cache["ts"], "ttl": CACHE_TTL})

# 정적 index.html 제공
@app.route("/")
def serve_index():
    # static/index.html이 있어야 합니다.
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))  # Render는 PORT를 환경변수로 넘겨줌
    app.run(host="0.0.0.0", port=port)
