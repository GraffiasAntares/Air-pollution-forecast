import logging, json
import uvicorn
from uuid import uuid4
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os, requests
from fastapi.templating import Jinja2Templates

from auth.models import UserRegistration, UserLogin, Message
from auth.database import get_connection, release_connection
from starlette.middleware.sessions import SessionMiddleware
import joblib
from dotenv import load_dotenv

load_dotenv("SECRET.env")

METEOSOURCE_KEY = os.getenv("METEOSOURCE_KEY")


app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Словарь для хранения сессионных токенов
session_store = {}

app.add_middleware(SessionMiddleware, secret_key="secret-key")

# Подключение статических файлов
current_dir = os.path.dirname(__file__)
static_dir = os.path.join(current_dir, "../front/static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates_dir = os.path.join(current_dir, "../front/templates")
templates = Jinja2Templates(directory=templates_dir)

# Загрузка модели
model_path = os.path.join(current_dir, "model_AQI.pkl")
model = joblib.load(model_path)

# Получение данных о погоде
weather_pred = requests.get(f'https://www.meteosource.com/api/v1/free/point?lat=56.01839N&lon=92.86717E&sections=daily&timezone=Asia%2FKrasnoyarsk&language=en&units=metric&key={METEOSOURCE_KEY}').json()

@app.post("/register")
async def register_user(user_data: UserRegistration):
    connection = get_connection()
    try:
        cur = connection.cursor()
        password = user_data.password  
        cur.execute(
            f"""INSERT INTO users (username, email, password, role)
              VALUES ('{user_data.username}', '{user_data.email}', '{password}', 'user') RETURNING id"""
        )
        connection.commit()
        user_id = cur.fetchone()[0]
        cur.close()
        return {"message": "User registered successfully", "user_id": user_id}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        release_connection(connection)

@app.post("/login")
async def login_user(user_data: UserLogin, request: Request):
    connection = get_connection()
    try:
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM users WHERE email = '{user_data.email}'")
        user = cur.fetchone()
        cur.close()

        if not user or user[3] != user_data.password:
            raise HTTPException(status_code=401, detail="Invalid credentials")

         # Генерация токена сессии
        session_token = str(uuid4())

        # Установка куки асинхронно
        request.session["session_token"] = session_token
        request.session["id"] = user[0]
        request.session["username"] = user[1]
        request.session["email"] = user[2]
        request.session["role"] = user[4]

        response_data = {"message": "Login successful", "role": user[4]}
        print("Response Data:", json.dumps(response_data, indent=4))
        return JSONResponse(content={"message": "Login successful", "role": user[4]})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        release_connection(connection)

@app.post("/send/")
async def register_user(message: Message, request: Request):
    connection = get_connection()
    id = request.session.get("id")
    print(id, message)
    try:
        cur = connection.cursor() 
        cur.execute(
            f"""INSERT INTO messages (user_id, message) VALUES ({id}, '{message.message}')"""
        )
        connection.commit()
        cur.close()
        return {"message": "Message sent"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        release_connection(connection)

@app.get("/protected-route")
async def protected_route(request: Request):
    if request.session.get("session_token") is not None:
        username = request.session.get("username")
        email = request.session.get("email")
        return {"message": f"Hello {username}, {email}"}
    return {"message": "Unauthorized user"}

def AQI_notification(month, day, temperature, wind_speed):
    pred = round(model.predict([[month, day, temperature, wind_speed]])[0])
    if pred > 100:
        return {'message': 'Опасное загрязнение воздуха', 'mean AQI': pred}
    elif pred <= 100 and pred > 70:
        return {'message': 'Повышенное загрязнение воздуха', 'mean AQI': pred}
    elif pred <= 70 and pred > 40:
        return {'message': 'Умеренное загрязнение воздуха', 'mean AQI': pred}
    elif pred <= 40:
        return {'message': 'Чистый воздух', 'mean AQI': pred}

def AQI_forecast():
    sub_dict = {'data': []}
    for forecast in weather_pred['daily']['data']:
        day = forecast['day']
        temp = forecast['all_day']['temperature']
        wind = forecast['all_day']['wind']['speed']
        # notification = AQI_notification(temp, wind)
        notification = AQI_notification(int(day[5:7]),int(day[-2:]),temp,wind)
        notification['date'] = day.replace('-', '.')[8:] + '.' + day.replace('-', '.')[5:7]
        sub_dict['data'].append(notification)
    return sub_dict

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/get_value")
async def get_value():
    return JSONResponse(content={"data": AQI_forecast()})

@app.get("/authorization/", response_class=HTMLResponse)
async def page0(request: Request):
    if request.session.get("session_token") is not None:
        return HTMLResponse(content="""
                <script>
                    window.location.href = '/profile';
                </script>
            """, status_code=403, headers={"Cache-Control": "no-cache"})
    return templates.TemplateResponse("page0.html", {"request": request})

@app.get("/registration/", response_class=HTMLResponse)
async def page01(request: Request):
    return templates.TemplateResponse("page01.html", {"request": request})

@app.get("/unlogin/", response_class=HTMLResponse)
async def page01(request: Request):
    request.session.clear()
    return HTMLResponse(content="""
                <script>
                    window.location.href = '/authorization/';
                </script>
            """, status_code=403, headers={"Cache-Control": "no-cache"})

@app.get("/profile/", response_class=HTMLResponse)
async def page0(request: Request):
     if request.session.get("session_token") is not None:
        username = request.session.get("username")
        email = request.session.get("email")
        return templates.TemplateResponse("profile.html", {"request": request, "username":username, "email":email})
     return {"message": "Unauthorized user"}

@app.get("/guide/", response_class=HTMLResponse)
async def page2(request: Request):
    return templates.TemplateResponse("page2.html", {"request": request})

@app.get("/description", response_class=HTMLResponse)
async def page3(request: Request):
    return templates.TemplateResponse("page3.html", {"request": request})

@app.get("/contacts/", response_class=HTMLResponse)
async def page4(request: Request):
    if request.session.get("session_token") is not None:
        return templates.TemplateResponse("page4_auth.html", {"request": request})
    return templates.TemplateResponse("page4.html", {"request": request})

if __name__ == '__main__':
    scss_path = os.path.join(os.path.dirname(__file__), '../front/static/scss')
    css_path = os.path.join(os.path.dirname(__file__), '../front/static/css')
    
    # subprocess.Popen(["sass", f"{scss_path}:{css_path}", "--watch"])
    uvicorn.run(app, host="0.0.0.0", port=8001)
    
    
    

