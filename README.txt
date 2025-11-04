Descripción General

Este proyecto implementa una API REST con FastAPI que Consume una API externa (https://4advance.co/testapi/get.php) para obtener datos de resultados (value, category).

*Almacena los resultados en una base de datos MySQL usando SQLAlchemy ORM.

*Aplica principios SOLID mediante separación de responsabilidades en módulos (controllers, db, models, services).

*Permite mejorar los registros “bad” haciendo llamadas sucesivas al API hasta alcanzar categoría medium o good.

*Ofrece endpoints CRUD completos para gestionar los registros manualmente.

La estructura del proyecto:

│
├── main.py                     # Punto de entrada principal (API)
│
├── controllers/                # (Opcional) Controladores de rutas si se expandiera
├── db/
│   ├── session.py              # Conexión y configuración de la BD
│
├── models/
│   ├── models.py               # Definición del modelo Proceso
│
├── services/
│   ├── recors_service.py       # Lógica de negocio: llamadas API, mejoras, reportes
│
├── venv/                       # Entorno virtual (no subir a GitHub)
│
└── README.md                   # Documentación del proyecto

 Requisitos Previos

Asegurarse de tener instalado:

*Python 3.9+

*MySQL Server (por ejemplo, con XAMPP o WAMP)

*pip (gestor de paquetes de Python)

Instalación y Configuración

1. Clonar este repositorio

2.Crear y activar el entorno virtual:
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate

3.Instalar las dependencias:

pip install fastapi uvicorn sqlalchemy pymysql requests

4.Configurar la conexión a MySQL

USERNAME = "root"
PASSWORD = ""
HOST = "localhost"
PORT = "3306"
DATABASE = "resultados"

5.Ejecutar la aplicación:

uvicorn main:app --reload

6.Abrir la documentación interactiva en Swagger:

Endpoints Principales

Método	Endpoint	                Descripción
GET	    /	                        Verifica si la API funciona
POST	/cargar-inicial/{user_id}	Carga 100 resultados desde la API externa
GET	    /procesos	                Lista todos los registros guardados
GET	    /procesos/{id}              Obtiene un proceso por su ID
POST	/procesos	                Crea un proceso manualmente (auto-categoriza según el valor)
PUT	    /procesos/{id}	            Actualiza el valor y categoría de un proceso
DELETE	/procesos/{id}	            Elimina un proceso de la BD
POST	/mejorar/{user_id}	        Repite llamadas al API para mejorar los registros bad
GET	    /reporte (opcional)         Devuelve estadísticas globales

Lógica de Categorización

La categoría se asigna automáticamente según el value:

Rango de Value	Categoría
0 – 60	bad
61 – 85	medium
86 – 100	good

🧾 Autor

Nombre: Daniel Santiago Avila Ramirez 
Lenguaje: Python 3.13.9
Framework: FastAPI
Base de Datos: MySQL (XAMPP)
