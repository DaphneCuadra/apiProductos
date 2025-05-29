# 🛍️ API de Productos - FastAPI

Este proyecto corresponde a una API RESTful desarrollada con **FastAPI** para la gestión de productos, conectada a una base de datos Oracle. Ideal para integrarse en un sistema web.

---

## 📁 1. Crear carpeta del proyecto

Antes de ejecutar los comandos, debes crear una carpeta en tu escritorio (o donde desees trabajar el proyecto). Abre tu terminal y ejecuta:

```bash
cd Desktop/
mkdir Productos
cd Productos/
```

---

## 🧪 2. Clonar el repositorio

Una vez dentro de la carpeta `Productos`, clona el repositorio del proyecto:

```bash
git clone https://github.com/DaphneCuadra/apiProductos.git
cd apiProductos/
```

---

## ⚙️ 3. Instalación de dependencias

Instala las siguientes dependencias necesarias para ejecutar la API:

```bash
pip install fastapi
pip install uvicorn
pip install oracledb
pip install python-multipart
```

> Asegúrate de tener **Python 3.8+** y **pip** correctamente configurados.

---

## 🚀 4. Levantar el servidor

Para iniciar la API en modo desarrollo con recarga automática, ejecuta:

```bash
uvicorn app.main:app --reload --port 8080
```

La API estará disponible en: [http://localhost:8080](http://localhost:8080)

---

## 🧑‍💻 5. Abrir el proyecto en VS Code

Si usas Visual Studio Code, puedes abrir la carpeta del proyecto ejecutando:

```bash
code .
```

---

## 📝 Notas

- Esta API puede conectarse a una base de datos Oracle, por lo tanto asegúrate de tener correctamente configurado el `TNS` o la conexión directa (`hostname`, `port`, `SID/Service_name`) en el archivo de configuración.
- El endpoint de documentación automática está disponible en: [http://localhost:8080/docs](http://localhost:8080/docs)

---

## 👨‍💻 Desarrollado por

- Daphne Cuadra  
- Geraldine Inostroza  
- Cristóbal Rivero
