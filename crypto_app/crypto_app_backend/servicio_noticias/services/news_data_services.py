from typing import List
from sqlalchemy.orm import Session
from servicio_usuarios.models.modelo_noticias import Noticia
from fastapi import HTTPException

def TraerNoticias(db: Session) -> List[Noticia]:
    """
    Obtiene todas las noticias desde la base de datos.
    """
    try:
        all_news = db.query(Noticia).all()
        if not all_news:
            raise HTTPException(status_code=404, detail="No se encontraron noticias.")
        return all_news
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las noticias: {str(e)}")
