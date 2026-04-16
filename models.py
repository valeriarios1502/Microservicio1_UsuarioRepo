from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    email = Column(String(100), unique=True)
    pais = Column(String(50))
    fecha_registro = Column(DateTime, default=datetime.now)
    activo = Column(Boolean, default=True)

    listas = relationship("Lista", back_populates="usuario", cascade="all, delete")
    peliculas_vistas = relationship("PeliculaVista", back_populates="usuario", cascade="all, delete")

class Lista(Base):
    __tablename__ = "listas"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    nombre = Column(String(100)) 
    fecha_creacion = Column(DateTime, default=datetime.now)

    usuario = relationship("Usuario", back_populates="listas")
    peliculas = relationship("ListaPelicula", back_populates="lista", cascade="all, delete")

class ListaPelicula(Base):
    __tablename__ = "lista_peliculas"
    id = Column(Integer, primary_key=True, index=True)
    lista_id = Column(Integer, ForeignKey("listas.id", ondelete="CASCADE"))
    pelicula_id = Column(Integer) 
    fecha_agregada = Column(DateTime, default=datetime.now)

    lista = relationship("Lista", back_populates="peliculas")

class PeliculaVista(Base):
    __tablename__ = "peliculas_vistas"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    pelicula_id = Column(Integer) 
    fecha_vista = Column(DateTime, default=datetime.now)

    usuario = relationship("Usuario", back_populates="peliculas_vistas")