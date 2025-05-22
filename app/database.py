import oracledb

def get_conexion():
    conexion = oracledb.connect(
        user="bd_clavitos",
        password="bd_clavitos",
        dsn= "localhost:1521/XE",
        #dsn="localhost:1521/orcl.duoc.com.cl"
    )
    return conexion