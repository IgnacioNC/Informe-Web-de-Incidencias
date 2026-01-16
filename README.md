# Informe web de incidencias – FastAPI + Jinja2

Aplicación web desarrollada con FastAPI y Jinja2 que genera un informe dinámico de incidencias, permitiendo filtrar los datos y visualizar estadísticas mediante gráficos.

![Captura general de la Web](capturas/cap_general.png)

## 🚀 Tecnologías utilizadas

- Python
- FastAPI
- Jinja2
- Chart.js
- HTML / CSS

## 📄 Funcionalidad

La aplicación ofrece un informe accesible desde la ruta `/informe` que incluye:

- Filtros por categoría, gravedad mínima y estado.
- Resumen estadístico de incidencias.
- Tabla detallada de incidencias filtradas.
- Gráficos interactivos con Chart.js.

## 📋 Tabla de incidencias

![Captura de los filtros](capturas/cap_tabla.png)

## 🔎 Filtros disponibles

- **Categoría**: red, hardware o software.
- **Gravedad mínima**: valor entre 1 y 5.
- **Estado**: pendiente, en curso o completada.

![Captura de los filtros](capturas/cap_filtros.png)

Los filtros se aplican mediante parámetros en la URL.

![Captura de la url](capturas/cap_url.png)

## 📊 Gráficos

- Gráfico de barras con incidencias por categoría.
- Gráfico circular con incidencias por estado (mejora añadida).

![Captura de los graficos](capturas/cap_graficos.png)

## 🗂️ Estructura del proyecto

```text
.
├── main.py
├── templates/
│   ├── base.html
│   └── informe.html
├── capturas/
└── README.md
```

## ▶️ Ejecución

Ejecutar el servidor de desarrollo:

```bash
uvicorn main:app --reload
```

Acceder al informe desde el navegador:

http://127.0.0.1:8000/informe
