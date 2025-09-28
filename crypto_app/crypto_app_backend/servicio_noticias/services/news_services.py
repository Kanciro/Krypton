# services/news_services.py

import requests
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

# Asegúrate de que todos los imports sean correctos
from servicio_usuarios.models.modelo_noticias import Noticia
from servicio_usuarios.models.modelo_fuente import Fuente
from servicio_usuarios.models.modelo_categoria_noticias import CategoriaNoticias
from servicio_usuarios.models.modelo_criptomonedas import Criptomoneda
from servicio_usuarios.database.db import get_db

# ---
# Funciones de utilidad para obtener/crear fuentes y categorías (las que ya tenías)
# ...

def get_or_create_fuente(db: Session, nombre_fuente: str) -> Fuente:
    """Obtiene una fuente por nombre o la crea si no existe."""
    fuente = db.query(Fuente).filter(func.lower(Fuente.fuente) == func.lower(nombre_fuente)).first()
    if not fuente:
        fuente = Fuente(fuente=nombre_fuente)
        db.add(fuente)
        db.commit()
        db.refresh(fuente)
    return fuente

def get_or_create_categoria(db: Session, nombre_categoria: str) -> CategoriaNoticias:
    """Obtiene una categoría por nombre o la crea si no existe."""
    categoria = db.query(CategoriaNoticias).filter(func.lower(CategoriaNoticias.categoria) == func.lower(nombre_categoria)).first()
    if not categoria:
        categoria = CategoriaNoticias(categoria=nombre_categoria)
        db.add(categoria)
        db.commit()
        db.refresh(categoria)
    return categoria

# Nueva función para encontrar el ID de la criptomoneda a partir del título
def find_crypto_id_by_title(db: Session, title: str) -> int | None:
    """
    Busca una criptomoneda en el título de la noticia.
    Devuelve el id_cripto si la encuentra, de lo contrario None.
    """
    # Consulta todas las criptomonedas en la base de datos
    cryptos = db.query(Criptomoneda.id_cripto, Criptomoneda.nombre).all()
    
    # Crea una lista de palabras clave (nombres de criptomonedas en minúsculas)
    crypto_names_lower = {name.lower(): crypto_id for crypto_id, name in cryptos}
    
    # Comprueba si alguna palabra clave está en el título de la noticia
    for name, crypto_id in crypto_names_lower.items():
        if name in title.lower():
            return crypto_id
            
    return None

# ---
# Función principal para obtener e insertar noticias (modificada)

def fetch_and_insert_news(db: Session, lang: str = 'ES'):
    """
    Obtiene noticias de CryptoCompare e las inserta en la base de datos.
    """
    url = "https://min-api.cryptocompare.com/data/v2/news/"
    params = {"lang": lang}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        articles = data.get('Data', [])
        
        # El endpoint de FastAPI ya inyecta la sesión, no necesitas crearla aquí.
        # Por lo tanto, el siguiente bloque de código debe ser removido:
        # db = next(get_db())
        
        for article in articles:
            api_id = article.get('id', '')
            titulo = article.get('title', '')
            url_noticia = article.get('url', '')
            contenido = article.get('body', '')
            source_name = article.get('source_info', {}).get('name', 'Desconocido')
            
            # Asignar una categoría por defecto
            categoria_name = "Noticias de Criptomonedas"
            
            # Prevenir la inserción de duplicados
            existing_news = db.query(Noticia).filter(Noticia.api_id == api_id).first()
            if existing_news:
                print(f"Noticia con ID {api_id} ya existe. Saltando...")
                continue
            
            # Obtener/Crear la fuente y la categoría
            fuente_obj = get_or_create_fuente(db, source_name)
            categoria_obj = get_or_create_categoria(db, categoria_name)
            
            # --- ¡Lógica clave! ---
            # Encontrar el ID de la criptomoneda a partir del título de la noticia
            crypto_id = find_crypto_id_by_title(db, titulo)
            
            # Crear e insertar la nueva noticia
            new_news = Noticia(
                api_id=api_id,
                titulo=titulo,
                url=url_noticia,
                contenido=contenido,
                fecha_creacion=datetime.utcnow(),
                id_fuente=fuente_obj.id_fuente,
                id_categoria=categoria_obj.id_categoria,
                id_cripto=crypto_id 
            )
            
            db.add(new_news)
            print(f"Noticia insertada: {titulo}")
            
        db.commit()
        print("Todas las noticias han sido procesadas.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de CryptoCompare: {e}")
        db.rollback()
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        db.rollback()
    finally:
        # FastAPI se encarga de cerrar la sesión, no es necesario que lo hagas aquí
        pass