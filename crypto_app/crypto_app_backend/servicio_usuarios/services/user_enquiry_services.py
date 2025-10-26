# servicio_usuarios/services/consultas_usuario_services.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from servicio_usuarios.models.modelo_usuario import Usuario
from servicio_usuarios.models.modelo_criptomonedas import Criptomoneda
from servicio_usuarios.models.modelo_moneda_fiat import MonedaFiat
from servicio_usuarios.models.modelo_consultas_usuario import ConsultasUsuario

def registrarConsultaUsuario(db: Session, id_usuario: int, id_cripto: int, id_moneda: int):

    try:
        
        usuario = db.query(Usuario).get(id_usuario)
        cripto = db.query(Criptomoneda).get(id_cripto)
        moneda = db.query(MonedaFiat).get(id_moneda)

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        if not cripto:
            raise HTTPException(status_code=404, detail="Criptomoneda no encontrada")
        if not moneda:
            raise HTTPException(status_code=404, detail="Moneda Fiat no encontrada")

        
        nueva_consulta = ConsultasUsuario(
            id_usuario=id_usuario,
            id_cripto=id_cripto,
            id_moneda=id_moneda
        )

        db.add(nueva_consulta)
        db.commit()
        db.refresh(nueva_consulta)

        return {"mensaje": "Consulta de usuario registrada con éxito."}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al registrar la consulta: {str(e)}")