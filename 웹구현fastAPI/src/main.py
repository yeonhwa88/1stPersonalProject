from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import tensorflow as tf
import numpy as np
import os

# FastAPI 애플리케이션 생성
app = FastAPI()

# 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 위치
templates_path = os.path.join(current_dir, "../templates")  # templates 폴더 경로
model_path = os.path.join(current_dir, "../model/movies_sea-028-val0.4281.h5")  # 모델 파일 경로

# 템플릿 경로 확인 및 설정
if not os.path.exists(templates_path):
    print(f"Templates directory not found: {templates_path}")
    raise FileNotFoundError(f"Templates directory not found: {templates_path}")
templates = Jinja2Templates(directory=templates_path)

# 모델 경로 확인 및 로드
if not os.path.exists(model_path):
    print(f"Model file not found: {model_path}")
    raise FileNotFoundError(f"Model file not found: {model_path}")
try:
    model = tf.keras.models.load_model(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Failed to load the model: {e}")
    raise RuntimeError(f"Failed to load the model: {e}")

# 장르와 등급 매핑
genre_mapping = {
    "애니메이션": 0, "액션": 1, "드라마": 2, "멜로/로맨스": 3, "범죄": 4, "공포(호러)": 5, "코미디": 6,
    "스릴러": 7, "다큐멘터리": 8, "미스터리": 9, "판타지": 10, "가족": 11, "전쟁": 12, "SF": 13, "공연": 14,
    "어드벤처": 15, "기타": 16, "뮤지컬": 17, "사극": 18, "성인물(에로)": 19, "서부극(웨스턴)": 20
}

rating_mapping = {
    "전체관람가": 0, "12세관람가": 1, "15세관람가": 2, "청소년관람불가": 3, "성인물": 4
}

season_mapping = {
    1: "봄",
    2: "여름",
    3: "가을",
    4: "겨울"
}

# 루트 경로
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 예측 경로
@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    genre: str = Form(...),
    total_screens: int = Form(...),
    audience_count: int = Form(...),
    rating: str = Form(...),
):
    # 입력값 매핑
    genre_encoded = genre_mapping.get(genre, 0)
    rating_encoded = rating_mapping.get(rating, 0)

    # 모델 입력 데이터 준비
    features = np.array([[genre_encoded, total_screens, audience_count, rating_encoded]], dtype=np.float32)

    # 예측 수행
    try:
        prediction = model.predict(features) if model else None
        predicted_season = np.argmax(prediction, axis=1)[0] + 1 if prediction is not None else 0
        season_name = season_mapping.get(predicted_season, "예측 불가")
    except Exception as e:
        print(f"Prediction failed: {e}")
        season_name = "예측 실패"
        predicted_season = 0

    # 결과 반환
    return templates.TemplateResponse("result.html", {
        "request": request,
        "genre": genre,
        "total_screens": total_screens,
        "audience_count": audience_count,
        "rating": rating,
        "season": predicted_season,
        "season_name": season_name
    })

# 상태 확인 경로
@app.get("/health", response_class=HTMLResponse)
async def health():
    return "FastAPI server is running!"
