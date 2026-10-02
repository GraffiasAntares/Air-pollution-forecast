# Air Pollution Forecast

Веб-приложение для прогнозирования среднего индекса качества воздуха (AQI) в городе Красноярск. Проект выполнен в рамках курсовой работы (СФУ).

## О проекте

Приложение строит прогноз **среднего AQI для города Красноярск** с помощью модели машинного обучения **Random Forest** (случайный лес). Результаты отображаются в веб-интерфейсе.

## Возможности

- Прогноз среднего значения AQI по Красноярску
- Веб-интерфейс для просмотра результатов
- Запуск локально или в Docker

## Технологии

- **ML-модель:** Random Forest (scikit-learn)
- **Backend:** Python (зависимости в `requirements.txt`)
- **Frontend:** Node.js (зависимости в `package.json`)
- **Контейнеризация:** Docker

## Структура проекта

```
Air-pollution-forecast/
├── app/                # исходный код приложения
├── Dockerfile          # сборка Docker-образа
├── package.json        # зависимости Node.js
├── package-lock.json
├── requirements.txt    # зависимости Python
└── .gitignore
```

## Данные и модель

| Параметр | Значение |
|---|---|
| Город | Красноярск |
| Целевая переменная | средний AQI |
| Модель | Random Forest (RandomForestRegressor) |
| Источник данных | meteosource.com |
| Признаки | month, day, temperature, wind_speed |
| Горизонт прогноза | 7 дней |

### Про индекс AQI

AQI (Air Quality Index) приводит концентрации загрязняющих веществ к единой шкале: чем выше значение, тем хуже качество воздуха.

| AQI | Уровень |
|---|---|
| 0–40 | Чистый воздух |
| 41–70 | Умеренное загрязнение |
| 71–100 | Повышенное загрязнение |
| 101+ | Опасное загрязнение |

## Установка и запуск

### 1. Клонирование

```bash
git clone https://github.com/GraffiasAntares/Air-pollution-forecast.git
cd Air-pollution-forecast
```

### 2. Переменные окружения

Создайте файл `.env` в корне проекта:

```env
 METEOSOURCE_KEY=ваш_ключ
```

Файл `.env` добавлен в `.gitignore` и не попадает в репозиторий.

### 3. Локальный запуск

```bash
# Python-зависимости
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Node-зависимости
npm install

# запуск
<команда запуска, например: python app/main.py>
```

Приложение будет доступно по адресу `http://localhost:8000`.

### 4. Запуск в Docker

```bash
docker build -t air-pollution-forecast .
docker run -p 8000:8000 --env-file .env air-pollution-forecast
```
