import requests
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.models import Proceso
from time import sleep

API_URL = "https://4advance.co/testapi/get.php?user_id="


#  FUNCIONES DE APOYO (Capa de servicio con separación lógica)

def obtener_resultado_api(user_id: str):
    """
    Llama al API externa y devuelve el resultado en formato dict.
    Retorna None si ocurre un error.
    """
    try:
        full_url = f"{API_URL}{user_id}"
        print(f"🌐 Llamando a: {full_url}")  # depuración
        with requests.Session() as session:
            session.trust_env = False
            response = session.get(full_url, timeout=5, proxies={"http": None, "https": None})
            response.raise_for_status()
            data = response.json()
            print(f"✅ Respuesta API: {data}")
            return data
    except requests.RequestException as e:
        print(f"❌ Error al llamar al API: {e}")
        return None


def insertar_resultado(db: Session, user_id: str):
    """
    Llama al API y guarda el resultado en la base de datos.
    Retorna el nuevo registro o None si hubo error.
    """
    data = obtener_resultado_api(user_id)
    if data is None:
        return None

    nuevo = Proceso(value=data["value"], category=data["category"])
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


#  CARGA INICIAL (100 llamadas al API)


def cargar_inicial(db: Session, user_id: str, cantidad: int = 100):
    """
    Hace N llamadas iniciales al API y guarda los resultados.
    Retorna la lista de registros insertados.
    """
    registros = []
    for i in range(cantidad):
        resultado = insertar_resultado(db, user_id)
        if resultado:
            registros.append(resultado)
        else:
            print(f"⚠️  Error en llamada #{i+1}, se omitió registro.")
        sleep(0.2)  # evita ráfagas al API
    print(f"✅ Carga inicial completada ({len(registros)} registros).")
    return registros


#  BARRIDOS DE MEJORA (identificar 'bad' y reintentar)

def barrido_mejora(db: Session, user_id: str, max_barridos: int = 50, max_estancados: int = 5):
    """
    Repite llamadas al API para mejorar los registros 'bad'.
    Si en varios barridos consecutivos no se logra mejora, detiene el proceso.
    Retorna estadísticas del proceso.
    """
    total_intentos = 0
    total_mejorados = 0
    barrido = 0
    sin_mejora_consecutivos = 0

    while barrido < max_barridos:
        malos = db.query(Proceso).filter(Proceso.category == "bad").all()
        restantes = len(malos)

        # Si ya no hay registros "bad", termina
        if restantes == 0:
            print(f"✅ No quedan registros 'bad'. Barridos totales: {barrido}")
            break

        barrido += 1
        mejorados = 0
        print(f"\n🔄 Barrido {barrido}: {restantes} registros 'bad' encontrados.")

        for record in malos:
            total_intentos += 1
            nuevo = obtener_resultado_api(user_id)
            if not nuevo:
                continue

            nueva_categoria = nuevo.get("category")
            nuevo_valor = nuevo.get("value")

            # Solo actualiza si mejora (medium o good)
            if nueva_categoria in ("medium", "good"):
                record.category = nueva_categoria
                record.value = nuevo_valor
                mejorados += 1
                total_mejorados += 1
                db.commit()

            sleep(0.2)  # evita saturar el API

        if mejorados > 0:
            print(f"✅ Barrido {barrido}: {mejorados} registros mejorados.")
            sin_mejora_consecutivos = 0
        else:
            sin_mejora_consecutivos += 1
            print(f"⚠️ Barrido {barrido}: sin mejoras ({sin_mejora_consecutivos}/{max_estancados}).")

        # Si se acumulan varios sin mejora, se detiene
        if sin_mejora_consecutivos >= max_estancados:
            print("⛔ Proceso detenido: demasiados barridos sin mejoras.")
            break

    restantes_final = db.query(Proceso).filter(Proceso.category == "bad").count()
    print(f"\n📊 Barridos realizados: {barrido} | Mejorados: {total_mejorados} | Restantes: {restantes_final}")

    return {
        "barridos_realizados": barrido,
        "intentos_totales": total_intentos,
        "registros_mejorados": total_mejorados,
        "bad_restantes": restantes_final
    }


#  REPORTE FINAL (conteo por categoría)

def reporte_final(db: Session):
    """
    Genera un resumen de categorías y totales.
    Retorna dict listo para usar en JSON o consola.
    """
    total = db.query(func.count(Proceso.id)).scalar()
    categorias = db.query(Proceso.category, func.count()).group_by(Proceso.category).all()

    print("\n=== 📊 REPORTE FINAL ===")
    print(f"Total registros: {total}")
    for cat, count in categorias:
        print(f" - {cat}: {count}")

    return {
        "total_registros": total,
        "categorias": {cat: count for cat, count in categorias}
    }
