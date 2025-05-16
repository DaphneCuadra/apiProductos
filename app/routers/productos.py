from fastapi import APIRouter, HTTPException
from app.database import get_conexion

#vamos a crear la variable para las rutas:
router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

#endpoints: GET, GET, POST, PUT, DELETE, PATCH
@router.get("/")
def obtener_productos():
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("SELECT id_producto, nombre, descripcion, precio, stock, marca, id_marca, id_inventario, id_categoria  FROM producto")
        productos = []
        for  id_producto, nombre, descripcion, precio, stock, marca, id_marca, id_inventario, id_categoria in cursor:
            productos.append({
                "id_producto": id_producto,
                "nombre": nombre,
                "descripcion": descripcion
                "precio": precio
                "stock": stock
                "marca": marca
                "id_marca": id_marca
                "id_inventario": id_inventario
                "id_categoria": id_categoria
            })
        cursor.close()
        cone.close()
        return productos
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/{id_buscar}")
def obtener_producto(id_producto: int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("SELECT  id_producto, nombre, descripcion, precio, stock, marca, id_marca, id_inventario, id_categoria FROM producto WHERE id_producto = :id_producto"
                       ,{"id_producto": id_buscar})
        producto = cursor.fetchone()
        cursor.close()
        cone.close()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return {
            "id_producto": id_buscar,
            "nombre": producto[0],
            "descripcion": producto[1],
            "precio": producto[2],
            "stock": producto[3],
            "marca": producto[4],
            "id_marca": producto[5],
            "id_inventario": producto[6],
            "id_categoria": producto[7]
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/")
def agregar_producto(id_producto:int, nombre:str, descripcion:str, precio:int, stock:int, marca:str, id_marca:int, id_inventario:int, id_categoria:int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
            INSERT INTO producto
            VALUES(:id_producto, :nombre, :descripcion, :precio, :stock, :marca, :id_marca, :id_inventario, :id_categoria)
        """,{"id_producto":id_producto, "nombre":nombre, "descripcion": descripcion, "precio":precio, "stock":stock, "marca":marca, "id_marca":id_marca, "id_inventario":id_inventario, "id_categoria":id_categoria})
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Producto agregado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

Terminar Tabla!!!
@router.put("/{id_actualizar}")
def actualizar_producto(id_actualizar:int, nombre:str, descripcion:str, precio:int, stock:int, marca:str, id_marca:int, id_inventario:int, id_categoria:int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
                UPDATE producto
                SET nombre = :nombre, email = :email
                WHERE id_producto = :id_producto
        """, {"nombre":nombre, "descripcion": descripcion, "precio":precio, "stock":stock, "marca":marca, "id_marca":id_marca, "id_inventario":id_inventario, "id_categoria":id_categoria, "id_producto":id_actualizar})
        if cursor.rowcount==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Producto actualizado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.delete("/{rut_eliminar}")
def eliminar_producto(rut_eliminar: int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("DELETE FROM alumno WHERE rut = :rut"
                       ,{"rut": rut_eliminar})
        if cursor.rowcount==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Usuario eliminado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


from typing import Optional

@router.patch("/{rut_actualizar}")
def actualizar_parcial(rut_actualizar:int, nombre:Optional[str]=None, email:Optional[str]=None):
    try:
        if not nombre and not email:
            raise HTTPException(status_code=400, detail="Debe enviar al menos 1 dato")
        cone = get_conexion()
        cursor = cone.cursor()

        campos = []
        valores = {"rut": rut_actualizar}
        if nombre:
            campos.append("nombre = :nombre")
            valores["nombre"] = nombre
        if email:
            campos.append("email = :email")
            valores["email"] = email

        cursor.execute(f"UPDATE alumno SET {', '.join(campos)} WHERE rut = :rut"
                       ,valores)
        if cursor.rowcount==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        cone.commit()
        cursor.close()
        cone.close()        
        return {"mensaje": "Usuario actualizado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))