from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(title="Test Scraper App")

# Verificar que el directorio existe
template_dir = os.path.join(os.getcwd(), "templates")
print(f"Template directory: {template_dir}")
print(f"Directory exists: {os.path.exists(template_dir)}")

# Configurar templates
templates = Jinja2Templates(directory=template_dir)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal simplificada"""
    try:
        return templates.TemplateResponse("test.html", {
            "request": request,
            "message": "Hola Mundo",
            "success": True
        })
    except Exception as e:
        return HTMLResponse(f"<h1>Error: {str(e)}</h1>", status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8004)