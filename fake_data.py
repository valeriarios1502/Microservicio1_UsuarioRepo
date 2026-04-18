from faker import Faker
from database import SessionLocal
from models import Usuario, Lista, ListaPelicula, PeliculaVista
import random
import pymysql
import sys
import os
from sqlalchemy import text

fake = Faker('es')

def get_peliculas_ids():
    conn = pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM movies")
    ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return ids

def crear_fake_data():
    db = SessionLocal()
    PELICULA_ID_MIN = 1
    PELICULA_ID_MAX = 20015
    peliculas_ids = get_peliculas_ids()
    print(f"Películas cargadas: {len(peliculas_ids)}", flush=True)

    # Usuarios
    usuarios_ids = []
    for i in range(20000):
        usuario = Usuario(
            nombre=fake.name(),
            email=fake.unique.email(),
            pais=fake.country()
        )
        db.add(usuario)
        db.flush()
        usuarios_ids.append(usuario.id)
        if i % 500 == 0:
            db.commit()
            print(f"Usuarios: {i}/20000", flush=True)
    db.commit()
    print("Usuarios creados", flush=True)

    # Listas
    listas_ids = []
    for i, usuario_id in enumerate(usuarios_ids):
        cantidad = random.randint(1, 3)
        for _ in range(cantidad):
            lista = Lista(
                usuario_id=usuario_id,
                nombre=random.choice([
                    "Favoritas", "Watchlist", "Drama",
                    "Comedia", "Accion", "recomendadas"
                ])
            )
            db.add(lista)
            db.flush()
            listas_ids.append(lista.id)
        if i % 500 == 0:
            db.commit()
            print(f"Listas: {i}/{len(usuarios_ids)}", flush=True)
    db.commit()
    print("Listas creadas", flush=True)

    # Películas en listas
    for i, lista_id in enumerate(listas_ids):
        cantidad = random.randint(1, 3)
        peliculas = random.sample(peliculas_ids, cantidad)
        for pelicula_id in peliculas:
            item = ListaPelicula(
                lista_id=lista_id,
                pelicula_id=pelicula_id
            )
            db.add(item)
        if i % 500 == 0:
            db.commit()
            print(f"Películas en listas: {i}/{len(listas_ids)}", flush=True)
    db.commit()
    print("Películas agregadas a listas", flush=True)

    # Películas vistas
    for i, usuario_id in enumerate(usuarios_ids):
        cantidad = random.randint(5, 30)
        peliculas = random.sample(range(PELICULA_ID_MIN, PELICULA_ID_MAX + 1), cantidad)
        for pelicula_id in peliculas:
            vista = PeliculaVista(
                usuario_id=usuario_id,
                pelicula_id=pelicula_id
            )
            db.add(vista)
        if i % 500 == 0:
            db.commit()
            print(f"Películas vistas: {i}/{len(usuarios_ids)}", flush=True)
    db.commit()
    print("Películas vistas creadas", flush=True)

    db.close()
    print("Fake data completada!", flush=True)

if __name__ == "__main__":
    try:
        crear_fake_data()
    except Exception as e:
        print(f"ERROR: {e}", flush=True)
        import traceback
        traceback.print_exc()
