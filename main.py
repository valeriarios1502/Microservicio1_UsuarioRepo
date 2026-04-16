from fastapi import FastAPI
from routes import router
from database import engine, Base
import time

app = FastAPI(title="MS1 - Usuarios")  

app.include_router(router)

# (opcional) creación de tablas
def create_tables():
    for i in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            print("Tablas creadas", flush=True)
            return
        except Exception as e:
            time.sleep(3)


create_tables()