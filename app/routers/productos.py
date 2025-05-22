from fastapi import APIRouter, HTTPException, UploadFile, File, status
import os
from app.database import get_conexion
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

# Endpoint para obtener todos los productos
@router.get("/", status_code=status.HTTP_200_OK)
def obtener_productos():
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
            SELECT id_producto, nombre, descripcion, imagen, precio, stock, 
                   id_marca, id_inventario, id_categoria  
            FROM producto
        """)
        productos = []
        for row in cursor:
            productos.append({
                "id_producto": row[0],
                "nombre": row[1],
                "descripcion": row[2],
                "imagen": row[3],
                "precio": row[4],
                "stock": row[5],
                "id_marca": row[6],
                "id_inventario": row[7],
                "id_categoria": row[8],
            })
        cursor.close()
        cone.close()
        return productos
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )
    
@router.get("/marcas", status_code=status.HTTP_200_OK)
def obtener_marcas():
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
            SELECT id_marca, descripcion 
            FROM marca
        """)
        productos = []
        for row in cursor:
            productos.append({
                "id_marca": row[0],
                "descripcion": row[1],
            })
        cursor.close()
        cone.close()
        return productos
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )
@router.get("/categorias", status_code=status.HTTP_200_OK)
def obtener_categorias():
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
            SELECT id_categoria, descripcion 
            FROM categoria
        """)
        productos = []
        for row in cursor:
            productos.append({
                "id_categoria": row[0],
                "descripcion": row[1],
            })
        cursor.close()
        cone.close()
        return productos
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )

@router.get("/inventario", status_code=status.HTTP_200_OK)
def obtener_inventario():
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
            SELECT id_inventario, cantidad_disponible,descripcion,id_sucursal 
            FROM inventario
        """)
        productos = []
        for row in cursor:
            productos.append({
                "id_inventario": row[0],
                "cantidad_disponible": row[1],
                "descripcion": row[2],
                "id_sucursal": row[3],
            })
        cursor.close()
        cone.close()
        return productos
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )
# Endpoint para subir imágenes
@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_image(file: UploadFile = File(...)):
    try:
        # Validar tipo de archivo (opcional)
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
        ext = file.filename.split('.')[-1].lower()
        if ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de archivo no permitido"
            )

        # Generar nombre único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        # Guardar archivo
        with open(filepath, "wb") as buffer:
            buffer.write(await file.read())
        
        return {
            "message": "Archivo subido correctamente",
            "filePath": f"/{UPLOAD_DIR}/{filename}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Endpoint para obtener un producto específico
@router.get("/{id_producto}", status_code=status.HTTP_200_OK)
def obtener_producto(id_producto: int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
            SELECT id_producto, nombre, descripcion, imagen, precio, stock,
                   id_marca, id_inventario, id_categoria 
            FROM producto 
            WHERE id_producto = :id_producto
        """, {"id_producto": id_producto})
        
        producto = cursor.fetchone()
        cursor.close()
        cone.close()
        
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
            
        return {
            "id_producto": producto[0],
            "nombre": producto[1],
            "descripcion": producto[2],
            "imagen": producto[3],
            "precio": producto[4],
            "stock": producto[5],
            "id_marca": producto[6],
            "id_inventario": producto[7],
            "id_categoria": producto[8]
        }
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )

# Endpoint para crear un nuevo producto
@router.post("/")
def agregar_producto(id_producto: int,nombre: str,
    descripcion: str,
    imagen: str,
    precio: int,
    stock: int,
    id_marca: int,
    id_inventario: int,
    id_categoria: int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
            INSERT INTO producto
            VALUES(:id_producto, :nombre, :descripcion,:imagen,:precio,:stock,:id_marca,:id_inventario,:id_categoria)
        """,{"id_producto":id_producto, "nombre":nombre, "descripcion": descripcion,"imagen":imagen,"precio":precio,"stock":stock,"id_marca":id_marca,"id_inventario":id_inventario,"id_categoria":id_categoria})
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Producto agregado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

# Endpoint para actualizar un producto completo
class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    imagen: Optional[str] = None
    precio: Optional[int] = None
    stock: Optional[int] = None
    id_marca: Optional[int] = None
    id_inventario: Optional[int] = None
    id_categoria: Optional[int] = None

@router.put("/{id_producto}", status_code=status.HTTP_200_OK)
def actualizar_producto(
    id_producto: int,
    producto: ProductoUpdate
):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        
        # Verificar si el producto existe
        cursor.execute("SELECT 1 FROM producto WHERE id_producto = :id", {"id": id_producto})
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        
        # Construir la consulta dinámicamente
        update_fields = {}
        for field, value in producto.dict().items():
            if value is not None:
                update_fields[field] = value
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        
        set_clause = ", ".join([f"{k} = :{k}" for k in update_fields.keys()])
        query = f"""
            UPDATE producto
            SET {set_clause}
            WHERE id_producto = :id_producto
        """
        
        params = update_fields
        params["id_producto"] = id_producto
        
        cursor.execute(query, params)
        
        cone.commit()
        return {"message": "Producto actualizado con éxito"}
        
    except HTTPException:
        raise
    except Exception as ex:
        cone.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )
    finally:
        cursor.close()
        cone.close()

# Endpoint para eliminar un producto
@router.delete("/{id_producto}", status_code=status.HTTP_200_OK)
def eliminar_producto(id_producto: int):
    response_data = {"message": "Producto eliminado con éxito"}
    cone = None
    cursor = None
    
    try:
        # 1. Obtener conexión
        cone = get_conexion()
        cursor = cone.cursor()
        
        # 2. Obtener información del producto (incluyendo imagen)
        cursor.execute("""
            SELECT imagen FROM producto 
            WHERE id_producto = :id_producto
        """, {"id_producto": id_producto})
        
        producto = cursor.fetchone()
        
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
            
        imagen_path = producto[0]
        
        # 3. Eliminar el producto de la BD
        cursor.execute("""
            DELETE FROM producto 
            WHERE id_producto = :id_producto
        """, {"id_producto": id_producto})
        
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
            
        cone.commit()
        
        # 4. Eliminar la imagen si existe
        if imagen_path and imagen_path.strip():
            try:
                from pathlib import Path
                
                # Normalizar la ruta de la imagen (eliminar cualquier / inicial)
                imagen_path = imagen_path.lstrip('/')
                
                # Construir ruta completa al archivo
                filepath = os.path.abspath(os.path.join(UPLOAD_DIR, Path(imagen_path).name))
                
                # Validar seguridad: asegurar que el archivo está dentro del directorio permitido
                upload_dir_abs = os.path.abspath(UPLOAD_DIR)
                if not filepath.startswith(upload_dir_abs):
                    response_data["warning"] = "Ruta de imagen inválida (fuera del directorio permitido)"
                    return response_data
                
                # Eliminar el archivo si existe
                if os.path.exists(filepath):
                    os.remove(filepath)
                    response_data["deleted_image"] = filepath
                else:
                    # Intentar encontrar el archivo con diferentes variaciones de la ruta
                    possible_paths = [
                        os.path.abspath(imagen_path),
                        os.path.abspath(os.path.join(UPLOAD_DIR, imagen_path)),
                        os.path.abspath(os.path.join(UPLOAD_DIR, Path(imagen_path).name))
                    ]
                    
                    found = False
                    for path in possible_paths:
                        if os.path.exists(path) and path.startswith(upload_dir_abs):
                            os.remove(path)
                            response_data["deleted_image"] = path
                            found = True
                            break
                    
                    if not found:
                        response_data["warning"] = f"Archivo de imagen no encontrado en: {possible_paths}"
                    
            except Exception as ex:
                print(f"Error eliminando imagen: {str(ex)}")
                response_data["warning"] = f"El producto se eliminó, pero la imagen no pudo borrarse: {str(ex)}"
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as ex:
        if cone:
            cone.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )
    finally:
        if cursor:
            cursor.close()
        if cone:
            cone.close()
# Endpoint para actualización parcial de un producto
@router.patch("/{id_producto}", status_code=status.HTTP_200_OK)
def actualizar_parcial(
    id_producto: int,
    nombre: Optional[str] = None,
    descripcion: Optional[str] = None,
    precio: Optional[int] = None,
    stock: Optional[int] = None,
    id_marca: Optional[int] = None,
    id_inventario: Optional[int] = None,
    id_categoria: Optional[int] = None
):
    try:
        # Verificar que al menos un campo sea proporcionado
        if not any([nombre, descripcion, precio, stock, id_marca, id_inventario, id_categoria]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Debe enviar al menos un campo para actualizar"
            )
            
        cone = get_conexion()
        cursor = cone.cursor()

        campos = []
        valores = {"id_producto": id_producto}
        
        if nombre is not None:
            campos.append("nombre = :nombre")
            valores["nombre"] = nombre
        if descripcion is not None:
            campos.append("descripcion = :descripcion")
            valores["descripcion"] = descripcion
        if precio is not None:
            campos.append("precio = :precio")
            valores["precio"] = precio
        if stock is not None:
            campos.append("stock = :stock")
            valores["stock"] = stock
        if id_marca is not None:
            campos.append("id_marca = :id_marca")
            valores["id_marca"] = id_marca
        if id_inventario is not None:
            campos.append("id_inventario = :id_inventario")
            valores["id_inventario"] = id_inventario
        if id_categoria is not None:
            campos.append("id_categoria = :id_categoria")
            valores["id_categoria"] = id_categoria

        query = f"""
            UPDATE producto 
            SET {', '.join(campos)} 
            WHERE id_producto = :id_producto
        """
        
        cursor.execute(query, valores)
        
        if cursor.rowcount == 0:
            cursor.close()
            cone.close()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
            
        cone.commit()
        cursor.close()
        cone.close()
        return {"message": "Producto actualizado parcialmente con éxito"}
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )