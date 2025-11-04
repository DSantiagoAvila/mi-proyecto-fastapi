from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.session import get_db
from models.models import Proceso
from services.recors_service import cargar_inicial, barrido_mejora, obtener_resultado_api

app = FastAPI()

@app.get("/recors")
def listar_registros(db: Session = Depends(get_db)):
    return db.query(Proceso).all()

@app.post("/recors/init")
def carga_inicial(
    user_id: str = Query(..., description="ID del usuario requerido"),
    db: Session = Depends(get_db)
):
    return cargar_inicial(db, user_id)

@app.post("/recors/barrido")
def ejecutar_barrido(
    user_id: str = Query(..., description="ID del usuario requerido"),
    db: Session = Depends(get_db)
):
    return barrido_mejora(db, user_id)

@app.put("/recors/{id}")
def actualizar_registro(id: int, value: int, category: str, db: Session = Depends(get_db)):
    registro = db.query(Proceso).filter(Proceso.id == id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    registro.value = value
    registro.category = category
    db.commit()
    db.refresh(registro)
    return registro

@app.delete("/recors/{id}")
def eliminar_registro(id: int, db: Session = Depends(get_db)):
    registro = db.query(Proceso).filter(Proceso.id == id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    db.delete(registro)
    db.commit()
    return {"mensaje": "Registro eliminado"}

@app.post("/recors/mejorar-continuamente")
def mejorar_continuamente(
    user_id: str = Query(..., description="ID del usuario requerido"),
    max_intentos: int = Query(default=10, description="Número máximo de intentos"),
    db: Session = Depends(get_db)
):
    """Busca y actualiza registros 'bad' con nuevos intentos"""
    intentos = 0
    total_actualizados = 0
    
    while intentos < max_intentos:
        registros_actualizados = 0
        registros_bad = db.query(Proceso).filter(Proceso.category == "bad").all()
        
        if not registros_bad:
            break
            
        for registro in registros_bad:
            nuevo_resultado = obtener_resultado_api(user_id)
            if nuevo_resultado and nuevo_resultado["category"] in ("medium", "good"):
                registro.value = nuevo_resultado["value"]
                registro.category = nuevo_resultado["category"]
                db.commit()
                db.refresh(registro)
                registros_actualizados += 1
                total_actualizados += 1
        
        if registros_actualizados == 0:
            break
            
        intentos += 1
    
    # Obtener estadísticas finales
    registros_bad_restantes = db.query(Proceso).filter(Proceso.category == "bad").count()
    
    return {
        "mensaje": f"Se actualizaron {total_actualizados} registros en {intentos} intentos",
        "registros_bad_restantes": registros_bad_restantes,
        "intentos_realizados": intentos,
        "se_detuvo_por": "No hay más registros bad" if registros_bad_restantes == 0 else 
                         "Se alcanzó el máximo de intentos" if intentos >= max_intentos else 
                         "No se pudieron mejorar más registros"
    }

@app.get("/recors/estadisticas")
def obtener_estadisticas(db: Session = Depends(get_db)):
    """Obtiene estadísticas de registros por categoría"""
    stats = db.query(
        Proceso.category,
        func.count(Proceso.id).label("count")
    ).group_by(Proceso.category).all()
    
    return {
        "total": db.query(func.count(Proceso.id)).scalar(),
        "por_categoria": {cat: count for cat, count in stats}
    }
