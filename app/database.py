import oracledb

def get_conexion():
    conexion = oracledb.connect(
        user="admin",
        password="admin",
        dsn="localhost:1521/orcl.duoc.com.cl"
    )
    return conexion