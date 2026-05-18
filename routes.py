from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Usuario, Lista, ListaPelicula, PeliculaVista
from datetime import datetime
import requests
import os

router = APIRouter()

MS3_URL = os.getenv("MS3_URL")

@router.get("/usuarios")
def get_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return usuarios

@router.get("/usuarios/{id}")
def get_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/usuarios")
def crear_usuario(nombre: str, email: str, pais: str, db: Session = Depends(get_db)):
    usuario_nuevo = Usuario(nombre=nombre, email=email, pais=pais)
    db.add(usuario_nuevo)
    db.commit()
    db.refresh(usuario_nuevo)
    return usuario_nuevo

@router.put("/usuarios/{id}")
def actualizar_usuario(id: int, nombre: str, email: str, pais: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.nombre = nombre
    usuario.pais = pais
    db.commit()
    return usuario

@router.delete("/usuarios/{id}")
def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    #requests.delete(f"{MS3_URL}/grupos/usuario/{id}/salir-todos") #o el nombre q le ponga bruno al endpoint
    #aca sale error xq aun no esta el metodo ps, asi q no se puede eliminar
    db.delete(usuario)
    db.commit()
    return {"Usuario eliminado"}




@router.get("/listas")
def get_todas_listas(db: Session = Depends(get_db)):
    listas = db.query(Lista).all()
    return listas

@router.get("/listas/usuario/{usuario_id}")
def get_listas_de_usuaria(usuario_id: int, db: Session = Depends(get_db)):
    listas = db.query(Lista).filter(Lista.usuario_id == usuario_id).all()
    return listas

@router.post("/usuarios/{usuario_id}/listas")
def crear_lista(usuario_id: int, nombre: str, db: Session = Depends(get_db)):
    lista_nueva = Lista(usuario_id=usuario_id, nombre=nombre)
    db.add(lista_nueva)
    db.commit()
    db.refresh(lista_nueva)
    return lista_nueva

@router.delete("/listas/{id}")
def eliminar_lista(id: int, db: Session = Depends(get_db)):
    lista = db.query(Lista).filter(Lista.id == id).first()
    db.delete(lista)
    db.commit()
    return {"Lista eliminada"}




@router.get("/listas/{lista_id}/peliculas")
def get_peliculas_lista(lista_id: int, db: Session = Depends(get_db)):
    peliculas = db.query(ListaPelicula).filter(ListaPelicula.lista_id == lista_id).all()
    return peliculas

@router.post("/listas/{lista_id}/agregar_pelicula")
def añadir_pelicula(lista_id: int, pelicula_id: int, db: Session = Depends(get_db)):
    peliculas = ListaPelicula(lista_id=lista_id, pelicula_id=pelicula_id)
    db.add(peliculas)
    db.commit()
    db.refresh(peliculas)
    return peliculas

@router.delete("/listas/{lista_id}/{pelicula_id}")
def eleiminar_pelicula(lista_id: int, pelicula_id: int, db: Session = Depends(get_db)):
    lista = db.query(ListaPelicula).filter(ListaPelicula.lista_id == lista_id, ListaPelicula.pelicula_id == pelicula_id).first()
    db.delete(lista)
    db.commit()
    return {"Pelicula eliminada"}




@router.get("/usuarios/{usuario_id}/peliculas_vistas")
def get_peliculas_vistas(usuario_id: int, db: Session = Depends(get_db)):
    peliculas = db.query(PeliculaVista).filter(PeliculaVista.usuario_id == usuario_id).all()
    return peliculas

@router.post("/usuarios/{usuario_id}/vista/{pelicula_id}")
def marcar_vista(usuario_id: int, pelicula_id: int, db: Session = Depends(get_db)):
    vista = PeliculaVista(usuario_id=usuario_id, pelicula_id=pelicula_id)
    db.add(vista)
    db.commit()
    return {"mensaje": "Película marcada como vista"}

@router.get("/usuarios_registros")
def get_todos_los_registros(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    listas = db.query(Lista).all()
    listas_peliculas = db.query(ListaPelicula).all()
    peliculas_vistas = db.query(PeliculaVista).all()

    return {
        "usuarios": usuarios,
        "listas": listas,
        "listas_peliculas": listas_peliculas,
        "peliculas_vistas": peliculas_vistas
    }
