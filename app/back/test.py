from fastapi import FastAPI
from starlette.templating import Jinja2Templates
import os

app = FastAPI()
current_dir = os.path.dirname(__file__)
templates_dir = os.path.join(current_dir, "templates")
templates = Jinja2Templates(directory=templates_dir)

print("Templates initialized successfully!")