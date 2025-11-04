from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.session import get_db
from models.models import Proceso
from services.recors_service import (
    cargar_inicial,
    barrido_mejora,
    reporte_final
)

app = FastAPI(title="Prueba Técnica CRUD + SOLID + API", version="1.0.0")


#             ENDPOINTS PRINCIPALES (API)

@app.get("/")
def read_root():
    """Verifica si la API está funcionando."""
    return {"message": "API funcionando 🚀"}


@app.post("/cargar-inicial/{user_id}")
def cargar_datos(user_id: str, db: Session = Depends(get_db)):
    """
    Hace 100 llamadas al API externa y guarda los resultados en la base de datos.
    """
    resultados = cargar_inicial(db, user_id)
    return {
        "total_insertados": len(resultados),
        "primeros_5": [r.category for r in resultados[:5]]
    }


@app.get("/procesos")
def listar_procesos(db: Session = Depends(get_db)):
    """
    Lista todos los registros guardados en la base de datos.
    """
    procesos = db.query(Proceso).all()
    return [
        {"id": p.id, "value": p.value, "category": p.category}
        for p in procesos
    ]


@app.post("/mejorar/{user_id}")
def mejorar_registros(user_id: str, db: Session = Depends(get_db)):
    """
    Identifica registros 'bad' y reintenta hasta mejorar todos a 'medium' o 'good'.
    Retorna resumen de barridos e informe final.
    """
    resultado = barrido_mejora(db, user_id)
    resumen = reporte_final(db)
    return {
        "resultado_mejora": resultado,
        "reporte_final": resumen
    }



#                    CRUD MANUAL

@app.get("/procesos/{id}")
def obtener_proceso(id: int, db: Session = Depends(get_db)):
    """
    Obtiene un proceso por su ID y muestra sus datos.
    Ejemplo de respuesta:
    {
        "id": 15,
        "value": 78,
        "category": "medium"
    }
    """
    proceso = db.query(Proceso).filter(Proceso.id == id).first()
    if not proceso:
        raise HTTPException(status_code=404, detail=f"Proceso con ID {id} no encontrado")

    return {
        "id": proceso.id,
        "value": proceso.value,
        "category": proceso.category
    }


@app.post("/procesos")
def crear_proceso(
    value: int = Query(..., ge=0, le=100, description="Valor entre 0 y 100"),
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo proceso manualmente.
    La categoría se asigna automáticamente:
    - 0–60: bad
    - 61–85: medium
    - 86–100: good
    """
    if 0 <= value <= 60:
        category = "bad"
    elif 61 <= value <= 85:
        category = "medium"
    else:
        category = "good"

    nuevo = Proceso(value=value, category=category)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {
        "mensaje": "Proceso creado exitosamente",
        "proceso": {
            "id": nuevo.id,
            "value": nuevo.value,
            "category": nuevo.category
        }
    }


@app.put("/procesos/{id}")
def actualizar_proceso(
    id: int,
    value: int = Query(..., ge=0, le=100, description="Valor entre 0 y 100"),
    db: Session = Depends(get_db)
):
    """
    Actualiza el valor y la categoría de un proceso existente.
    La categoría se calcula automáticamente según el valor.
    """
    proceso = db.query(Proceso).filter(Proceso.id == id).first()
    if not proceso:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")

    # Determinar categoría automáticamente
    if 0 <= value <= 60:
        category = "bad"
    elif 61 <= value <= 85:
        category = "medium"
    else:
        category = "good"

    proceso.value = value
    proceso.category = category
    db.commit()
    db.refresh(proceso)

    return {
        "mensaje": f"Proceso {id} actualizado correctamente",
        "nuevo_valor": proceso.value,
        "nueva_categoria": proceso.category
    }


@app.delete("/procesos/{id}")
def eliminar_proceso(id: int, db: Session = Depends(get_db)):
    """
    Elimina un proceso de la base de datos.
    """
    proceso = db.query(Proceso).filter(Proceso.id == id).first()
    if not proceso:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    db.delete(proceso)
    db.commit()
    return {"mensaje": f"Proceso con ID {id} eliminado correctamente"}