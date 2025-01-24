from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import tensorflow as tf
import numpy as np
import os

app = FastAPI()

# Model Path
<<<<<<< HEAD
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../model/movies_sea-028-val0.4281.h5"))

# Load Model
model = tf.keras.models.load_model(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
=======
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "movies_sea-028-val0.4281.h5"))

# Load Model
model = None
if os.path.exists(MODEL_PATH):
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully!")
else:
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
>>>>>>> 2ca2103e3b38f8aec2877dff959e413e5a37db17

# HTML Templates Setup
templates = Jinja2Templates(directory=os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates")))

# Genre and Rating Mapping
genre_mapping = {
    "애니메이션": 0, "액션": 1, "드라마": 2, "멜로/로맨스": 3, "범죄": 4, "공포(호러)": 5, "코미디": 6,
    "스릴러": 7, "다큐멘터리": 8, "미스터리": 9, "판타지": 10, "가족": 11, "전쟁": 12, "SF": 13, "공연": 14,
    "어드벤처": 15, "기타": 16, "뮤지컬": 17, "사극": 18, "성인물(에로)": 19, "서부극(웨스턴)": 20
}

rating_mapping = {
    "전체관람가": 0, "12세관람가": 1, "15세관람가": 2, "청소년관람불가": 3, "성인물": 4
}

<<<<<<< HEAD
=======
# Season Mapping
>>>>>>> 2ca2103e3b38f8aec2877dff959e413e5a37db17
season_mapping = {
    1: "봄",
    2: "여름",
    3: "가을",
    4: "겨울"
}

<<<<<<< HEAD
=======
@app.get("/favicon.ico", response_class=HTMLResponse)
async def favicon():
    return HTMLResponse(content="", status_code=204)

>>>>>>> 2ca2103e3b38f8aec2877dff959e413e5a37db17
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    genre: str = Form(...),
    total_screens: int = Form(...),
    audience_count: int = Form(...),
    rating: str = Form(...),
):
<<<<<<< HEAD
    # Encode Inputs
    genre_encoded = genre_mapping.get(genre, 0)
    rating_encoded = rating_mapping.get(rating, 0)
=======

    # Encode Inputs
    genre_encoded = genre_mapping.get(genre, -1)
    rating_encoded = rating_mapping.get(rating, -1)

    if genre_encoded == -1 or rating_encoded == -1:
        return templates.TemplateResponse("result.html", {
            "request": request,
            "genre": genre,
            "total_screens": total_screens,
            "audience_count": audience_count,
            "rating": rating,
            "season": "예측 실패",
            "season_name": "입력값 오류"
        })
>>>>>>> 2ca2103e3b38f8aec2877dff959e413e5a37db17

    # Prepare Input
    features = np.array([[genre_encoded, total_screens, audience_count, rating_encoded]], dtype=np.float32)

    # Predict
<<<<<<< HEAD
    prediction = model.predict(features) if model else None
    predicted_season = np.argmax(prediction, axis=1)[0] + 1 if prediction is not None else 0
    season_name = season_mapping.get(predicted_season, "예측 불가")
=======
    prediction = model.predict(features)
    if prediction is None or len(prediction) == 0:
        return templates.TemplateResponse("result.html", {
            "request": request,
            "genre": genre,
            "total_screens": total_screens,
            "audience_count": audience_count,
            "rating": rating,
            "season": "예측 실패",
            "season_name": "모델 오류"
        })

    predicted_season = np.argmax(prediction, axis=1)[0] + 1  # Add 1 to match 1:봄, 2:여름, 3:가을, 4:겨울
    season_name = season_mapping.get(predicted_season, "예측 실패")
>>>>>>> 2ca2103e3b38f8aec2877dff959e413e5a37db17

    # Render Result
    return templates.TemplateResponse("result.html", {
        "request": request,
        "genre": genre,
        "total_screens": total_screens,
        "audience_count": audience_count,
        "rating": rating,
        "season": predicted_season,
        "season_name": season_name
    })

@app.get("/health", response_class=HTMLResponse)
async def health():
    return "FastAPI server is running!"
