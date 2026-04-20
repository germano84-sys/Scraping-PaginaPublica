# Scraper Web de Tabla de Posiciones - FastAPI

## Descripción
Aplicación web que realiza web scraping de tablas de posiciones de fútbol desde páginas web (como ESPN) y permite visualizar y descargar los datos en formato CSV.

## Características
- ✅ Interfaz web intuitiva con Bootstrap
- ✅ Formulario para ingresar URL de scraping
- ✅ Visualización de datos en tabla HTML
- ✅ Descarga automática de archivo CSV
- ✅ Manejo de errores y mensajes informativos
- ✅ Scraping optimizado con BeautifulSoup
![API SCRAPER INICIADA](./img/scraper/inicio_ejecutada.jpg)

## Tecnologías
- **FastAPI**: Framework web moderno y rápido
- **BeautifulSoup**: Para parsing HTML
- **Pandas**: Para manipulación de datos
- **Jinja2**: Templates HTML
- **Bootstrap**: Interfaz responsiva
- **Uvicorn**: Servidor ASGI

## Instalación

1. **Clonar o descargar el proyecto**
2. **Crear entorno virtual**:
   ```bash
   python -m venv .venv
   ```
3. **Activar entorno virtual**:
   ```bash
   # Windows
   .\.venv\Scripts\activate
   ```
4. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## Inicio Rápido
# 
**Opción 1: Script automático (Windows)**
```bash
# Doble clic en start.bat
start.bat
```

**Opción 2: Manual**
```bash
# Activar entorno virtual
.\.venv\Scripts\activate

# Ejecutar aplicación
python -m uvicorn main:app --host 127.0.0.1 --port 8007 --reload
```

**Abrir navegador**: `http://127.0.0.1:8007`

3. **Ingresar URL** de la página con tabla de posiciones (por defecto: ESPN Liga Española)

4. **Hacer clic en "Realizar Scraping"**

5. **Visualizar datos** en la tabla y **descargar CSV** si es necesario

## Estructura del Proyecto
```
scraping-paginapublica/
├── main.py                 # Aplicación FastAPI
├── requirements.txt        # Dependencias
├── liga.csv               # Datos scrapeados (generado)
├── templates/
│   └── index.html         # Template principal
├── static/                # Archivos estáticos (CSS, JS)
└── readme.md              # Este archivo
```

## API Endpoints

- `GET /`: Página principal con formulario y datos
- `POST /scrape`: Realizar scraping (recibe URL por formulario)
- `GET /download`: Descargar archivo CSV

## Funcionamiento

La aplicación detecta automáticamente las tablas en la página web y combina:
- **Tabla de equipos**: Nombres y posiciones
- **Tabla de estadísticas**: PJ, G, E, P, GF, GC, DIF, PTS

Los datos se limpian, ordenan por puntos y se muestran en una tabla responsiva.

## Manejo de Errores

- URLs inválidas
- Páginas sin tablas
- Estructuras HTML inesperadas
- Problemas de conexión

## Personalización

Puedes modificar `scrape_football_data()` en `main.py` para adaptar el scraping a otras páginas web con estructuras diferentes.

## Datos extraídos
- Equipo
- Partidos jugados
- Ganados, empatados, perdidos
- Goles a favor y en contra
- Diferencia de goles
- Puntos

## Ejecución
1. Crear entorno virtual:
   python -m venv venv

2. Activar entorno:
   venv\Scripts\activate

3. Instalar dependencias:
   pip install -r requirements.txt

4. Ejecutar:
   python main.py

## Resultado
Se genera un archivo `liga_ecuador.csv` con la tabla de posiciones.