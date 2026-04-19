from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

app = FastAPI(title="Scraper de Tabla de Posiciones")

# Configurar archivos estáticos y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def scrape_football_data(url: str):
    """Función para hacer scraping de datos de fútbol"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Error al acceder a la URL: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Buscar todas las tablas
    tables = soup.find_all('table')

    if len(tables) < 2:
        raise HTTPException(status_code=400, detail="No se encontraron las tablas esperadas en la página")

    # Tabla 1: equipos, Tabla 2: estadísticas
    team_rows = tables[0].find_all('tr')[1:]  # Saltar header
    stat_rows = tables[1].find_all('tr')[1:]  # Saltar header

    data = []
    for i, (team_row, stat_row) in enumerate(zip(team_rows, stat_rows)):
        # Extraer nombre del equipo
        team_cell = team_row.find_all('td')[0].get_text().strip()
        pos = ''.join(filter(str.isdigit, team_cell[:2]))
        team = team_cell[2:]

        # Extraer estadísticas
        stat_cells = stat_row.find_all('td')
        stats = [cell.get_text().strip() for cell in stat_cells]

        if len(stats) >= 8:
            full_row = [pos, team] + stats
            data.append(full_row)

    if not data:
        raise HTTPException(status_code=400, detail="No se pudieron extraer datos válidos")

    # Crear DataFrame
    columns = ["Pos", "Equipo", "PJ", "G", "E", "P", "GF", "GC", "DIF", "PTS"]
    df = pd.DataFrame(data, columns=columns)

    # Limpiar datos numéricos
    cols_num = ["PJ", "G", "E", "P", "GF", "GC", "DIF", "PTS"]
    for col in cols_num:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Ordenar por puntos
    df = df.sort_values(by="PTS", ascending=False)

    return df

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal con formulario y datos"""
    data = None
    message = None
    success = False
    url = None

    # Verificar si existe el archivo CSV
    if os.path.exists("liga.csv"):
        try:
            df = pd.read_csv("liga.csv")
            data = df.to_dict('records')
            message = f"Datos cargados: {len(data)} equipos"
            success = True
        except Exception as e:
            message = f"Error al cargar datos existentes: {str(e)}"
            success = False

    return templates.TemplateResponse("index.html", {
        "request": request,
        "data": data,
        "message": message,
        "success": success,
        "url": url
    })

@app.post("/scrape", response_class=HTMLResponse)
async def scrape(request: Request, url: str = Form(...)):
    """Realizar scraping de la URL proporcionada"""
    data = None
    message = None
    success = False

    try:
        # Realizar scraping
        df = scrape_football_data(url)

        # Guardar CSV
        df.to_csv("liga.csv", index=False)

        # Convertir a formato para template
        data = df.to_dict('records')

        message = f"Scraping exitoso: {len(data)} equipos encontrados y guardados"
        success = True

    except HTTPException as e:
        message = e.detail
        success = False
    except Exception as e:
        message = f"Error inesperado: {str(e)}"
        success = False

    return templates.TemplateResponse("index.html", {
        "request": request,
        "data": data,
        "message": message,
        "success": success,
        "url": url
    })

@app.get("/download")
async def download_csv():
    """Descargar el archivo CSV"""
    if not os.path.exists("liga.csv"):
        raise HTTPException(status_code=404, detail="Archivo CSV no encontrado")

    return FileResponse(
        path="liga.csv",
        filename="liga.csv",
        media_type='text/csv',
        headers={"Content-Disposition": "attachment; filename=liga.csv"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8007)