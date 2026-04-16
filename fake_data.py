from faker import Faker
from database import SessionLocal
from models import Usuario, Lista, ListaPelicula, PeliculaVista
import random
import sys

fake = Faker('es')

def crear_fake_data():
    db = SessionLocal()

    PELICULA_ID_MIN = 1
    PELICULA_ID_MAX = 20015

    usuarios_ids = []
    for i in range(100):  
        usuario = Usuario(
            nombre=fake.name(),
            email=fake.unique.email(),
            pais=fake.country()
        )
        db.add(usuario)
        db.flush()
        usuarios_ids.append(usuario.id)
    db.commit()
    print("Usuarios creados", flush=True)

    listas_ids = []
    for usuario_id in usuarios_ids:
        cantidad = random.randint(1, 3)
        for _ in range(cantidad):
            lista = Lista(
                usuario_id=usuario_id,
                nombre=random.choice([
                    "Favoritas",
                    "Watchlist",
                    "Drama",
                    "Comedia",
                    "jijiju",
                    "recomendadas"
                ])
            )
            db.add(lista)
            db.flush()
            listas_ids.append(lista.id)
    db.commit()
    print("Listas creadas", flush=True)

    for lista_id in listas_ids:
        cantidad = random.randint(5, 15)
        peliculas = random.sample(range(PELICULA_ID_MIN, PELICULA_ID_MAX + 1), cantidad)
        for pelicula_id in peliculas:
            item = ListaPelicula(
                lista_id=lista_id,
                pelicula_id=pelicula_id
            )
            db.add(item)
    db.commit()
    print("Películas agregadas a listas", flush=True)

    for usuario_id in usuarios_ids:
        cantidad = random.randint(5, 30)
        peliculas = random.sample(range(PELICULA_ID_MIN, PELICULA_ID_MAX + 1), cantidad)
        for pelicula_id in peliculas:
            vista = PeliculaVista(
                usuario_id=usuario_id,
                pelicula_id=pelicula_id
            )
            db.add(vista)
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