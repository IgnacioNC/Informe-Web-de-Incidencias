from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

INCIDENCIAS = [
    {"id": 1, "categoria": "Red", "estado": "pendiente", "gravedad": 3, "comentario": "Problemas de conectividad"},
    {"id": 2, "categoria": "Hardware", "estado": "en_curso", "gravedad": 5, "comentario": "Fallo en servidor"},
    {"id": 3, "categoria": "Software", "estado": "Pendiente", "gravedad": 2, "comentario": "Error en aplicación"},
    {"id": 4, "categoria": "Software", "estado": "completada", "gravedad": 4, "comentario": "Actualización de drivers"},
    {"id": 5, "categoria": "Hardware", "estado": "completada", "gravedad": 5, "comentario": "Reemplazo de disco duro"},
]

# Al entrar en la raiz ("/") carga base.html
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "contenido": "<p>Ve a <a href='/informe'>/informe</a> para ver el informe.</p>",
        },
    )


@app.get("/informe", response_class=HTMLResponse)
async def informe(
    request: Request,   
    categoria: Optional[str] = Query(None, description="Filtrar por categoria"),  #query params
    min_gravedad: int = Query(1, ge=1, le=5, description="Gravedad minima"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
):
    
    # Filtro para recibir el parametro categoria y en caso contrario asignar ""
    # No se puede usar None porque no puede usar strip() ni lower(), por lo que luego se cambia a None si es ""
    categoria_normalizada = (categoria or "").strip().lower()
    if not categoria_normalizada:
        categoria_normalizada = None

    incidencias_filtradas = []
    for incidencia in INCIDENCIAS:
        # Si hay categoria y no coincide, se salta
        if categoria_normalizada and incidencia["categoria"].strip().lower() != categoria_normalizada:
            continue
        if incidencia["gravedad"] < min_gravedad:
            continue
        if estado and incidencia["estado"] != estado:
            continue
        incidencias_filtradas.append(incidencia)

    total_incidencias = len(incidencias_filtradas)
    resueltas = sum(1 for incidencia in incidencias_filtradas if incidencia["estado"] == "Completada")
    porcentaje_resueltas = (resueltas / total_incidencias * 100) if total_incidencias > 0 else 0

    # Variables que se usan en informe
    resumen = {
        "num_incidencias": total_incidencias,
        "num_resueltas": resueltas,
        "porcentaje_resueltas": round(porcentaje_resueltas, 2),
    }

    categorias_posibles = ["Red", "Hardware", "Software"]
    labels = categorias_posibles
    values = [
        # Cuenta las incidencias por categoria
        sum(1 for incidencia in incidencias_filtradas if incidencia["categoria"] == c)
        for c in categorias_posibles
    ]

    # Enviar datos a la plantilla informe.html
    return templates.TemplateResponse(
        "informe.html",
        {
            "request": request,
            "incidencias": incidencias_filtradas,
            "resumen": resumen,
            "labels": labels,
            "values": values,
            "categoria": categoria_normalizada or "",
            "estado": estado or "",
            "min_gravedad": min_gravedad,
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
