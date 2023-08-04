from flask import Flask, jsonify, request, render_template
from psycopg2 import extras
from conexion_BD import connection
from werkzeug.utils import secure_filename
import datetime
import os
from os import path
import re

app = Flask(__name__)

"""
desde aqui comienza los endpoinst de cliente
"""
@app.route("/customers", methods=["POST"])
def customers(): #esta funcion se encarga de agregar un cliente osea endponist 1
    new_cliente = request.get_json()
    nombre = new_cliente["name"]
    whatsapp = new_cliente["whatsapp"]
    cedula = new_cliente["cedula"]
    email = new_cliente["email"]  
    if not re.match(r"^[0-9]+$", str(cedula)):
       
        return jsonify({"error": "La cédula solo puede contener dígitos numéricos."}), 400

    # Validar que la cédula sea única y tenga un formato válido
    con = connection()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM Cliente WHERE cedula = %s", (cedula,))
    count= 0


    if count > 0:
        cur.close()
        con.close()
        return jsonify({"error": "La cédula ya existe en la base de datos."}), 400

    if not re.match(r"^\d{8}$", cedula):
        cur.close()
        con.close()
        return jsonify({"error": "La cédula debe tener 8 dígitos numéricos."}), 400

    if not re.match(r"^[0-9]+$", str(cedula)):
        cur.close()
        con.close()
        return jsonify({"error": "La cédula solo puede contener dígitos numéricos."}), 400

    # Validar que el correo electrónico tenga un formato válido
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        cur.close()
        con.close()
        return jsonify({"error": "El correo electrónico no es válido."}), 400

    # Insertar el nuevo cliente en la base de datos
    cur.execute(
        "INSERT INTO Cliente (cedula, nombre, whatsapp, email) VALUES (%s, %s, %s, %s)",
        (cedula, nombre, whatsapp, email),
    )
    con.commit()

    cur.close()
    con.close()

    return jsonify({"message": "El cliente ha sido creado exitosamente."}), 201





@app.route("/customers", methods=["GET"])
def lis_customers():#esta se encraga de traer toda la tabla de clientes osea endpoints
    con = connection()
    cur = con.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute("SELECT * FROM Cliente")
    clie = cur.fetchall()

    cur.close()
    con.close()
    return jsonify(clie)


@app.route("/customers/<cedula>", methods=["PUT"])
def update_customers(cedula):#esta se encarga de actualizar los datos de un cliente osea endpoints 3
    con = connection()
    cur = con.cursor(cursor_factory=extras.RealDictCursor)
    #extraigo los datos del endpoints
    new_cliente = request.get_json()
    nombre = new_cliente["name"]
    whatsapp = new_cliente["whatsapp"]
    email = new_cliente["email"]
    #valida la el correo
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        cur.close()
        con.close()
        return jsonify({"error": "El correo electrónico no es válido."}), 400

    cur.execute(
        "UPDATE Cliente SET nombre = %s, whatsapp = %s, email = %s where cedula= %s RETURNING * ",
        (nombre, whatsapp, email, cedula),
    )
    new_cliente = cur.fetchone()

    con.commit()

    cur.close()
    con.close()

    if new_cliente is None:
        return jsonify({"message": "Customers not found"})

    return "UPDATE"

"""
Desde aqui comienza los endpoinst de pedidos
"""
@app.route("/orders", methods=["POST"])
def orders():#esta endpoints se encarga de insertar el pedido
    prec_hamb = 5
    #extraigo los datos que me estan pasando por el endpoints osea el json
    new_order = request.get_json()
    cant_hambur = new_order["quanty"]
    modo_pago = new_order["paymet_method"]
    observacion = new_order["remark"]
    ciudad = new_order["city"]
    municipio = new_order["municipality"]
    cedula = new_order["cedula"]

    #estas son validaciones para verificar los datos del json y no puedan perjudicar la BD
    if modo_pago not in ["efectivo", "tarjeta","pago movil"]:
        return jsonify({"error": "El método de pago no es válido."}), 400

    if not re.match(r"^[a-zA-Z0-9\s]*$", observacion):
        return jsonify({"error": "La observación solo puede contener letras, números y espacios."}), 400
    
    if not re.match(r"^[a-zA-Z0-9\s]*$", ciudad):
        return jsonify({"error": "La ciudad solo puede contener letras, números y espacios"}), 400
  
    if not re.match(r"^[a-zA-Z0-9\s]*$", municipio):
        return jsonify({"error": "El municipio solo puede contener letras, números y espacios"}), 400

   
    if not re.match(r"^[0-9]+$", str(cedula)):
        return jsonify({"error": "La cédula solo puede contener dígitos numéricos."}), 400

    con = connection()
    cur = con.cursor(cursor_factory=extras.RealDictCursor)

    if municipio != "maneiro" or municipio != "Maneiro":
        monto_delivery = 2.00
    else:
        monto_delivery = 0.00

    total = (int(cant_hambur) * prec_hamb) + monto_delivery

    fe_ho_actu = datetime.datetime.now()
    fecha_hora = datetime.datetime.strftime(fe_ho_actu, "%Y-%m-%d %H:%M:%S")
    print(fecha_hora)
    cur.execute(
        "INSERT INTO Pedido (cant_hambur,modo_pago,observacion,ciudad,municipio,monto_delivery,total_pagar,fecha_hora,ced_cliente ) VAlUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *",
        (
            cant_hambur,
            modo_pago,
            observacion,
            ciudad,
            municipio,
            monto_delivery,
            total,
            fecha_hora,
            cedula,
        ),
    )

    order = cur.fetchone()
    con.commit()
    cur.close()
    con.close()
    return jsonify(order)

"""
@app.route("/enviar-screenshot", methods=["GET"])
def enviar_screenshot():
    return render_template("payment-screenshot.html")
"""

# se crea la configuracion para guaradar las imagenes
app.config["UPLOAD_IMAG"] = "screenshot"  # la ruta donde se va a guardar la imagen

ALLOWED_EXTENSIONS = set(["png", "jpg"])  # las extensiones permitidas


def allowed_file(file):#esta funcion e encraga de la extension del archivo
    file = file.split(".")
    if file[1] in ALLOWED_EXTENSIONS:
        return True
    return False


@app.route("/orders/<id>/payment-screenshot", methods=["POST"])
def payment_screenshot(id):#esta se encarga de agregar el endpoinst
    file = request.files["screenshot"]#extraigo el json del enpoinst del archivo mandado por el endpoinst
    filename = secure_filename(file.filename)  # type: ignore

    if file and allowed_file(filename):#verifico que el archivo sea correcto 
        print("permitido")
        extension = path.splitext(filename)[1]#saco la extension osea jpg
        new_name = id + extension 
        file.save(os.path.join(app.config["UPLOAD_IMAG"], new_name))
        # ahora se guarda en la BD
        con = connection()
        cur = con.cursor(cursor_factory=extras.RealDictCursor)
        cur.execute(
            "UPDATE Pedido SET sreen_pago = %s where num_pedido= %s",
            (new_name, id),
        )

        con.commit()

        cur.close()
        con.close()
        return new_name
    else:
        return jsonify({"message": "No se logro guardar la imagen"})


@app.route("/orders/<id>/status", methods=["PATCH"])
def update_status(id):#esta es endpoints para modificar el status
    con = connection()#creo la varieble conexion
    cur = con.cursor(cursor_factory=extras.RealDictCursor)#creo las variables pára ejecutar las consultas

    new_status = request.get_json()#extraigo el json que esta llegando por el endpoints
    estado = new_status["status"]# variable pára asiganar el estado

    if estado not in ["in_progress", "pending","delivered"]:#validacion donde dice si el status no esta entre esas tres entonces dara invalido
        return jsonify({"error": "El Estado es invalido."}), 400

    cur.execute(
        "UPDATE Pedido SET status = %s where num_pedido= %s RETURNING *",
        (estado, id),
    )#ejecuto la consulta
    update_excelent = cur.fetchone()#traigo el dato de la consultas osea los datos

    con.commit()

    cur.close()
    con.close()

    if update_excelent is None:#verifica que si la variable update_excelent es none osea no se logro la actualizacion
        return jsonify({"message": "NO SE LOGRO ACTUALIZAR"})

    return jsonify({"message": "ACTUALIZACION EXITOSA"})


@app.route("/orders", methods=["GET"])
def List_fecha_status_ced():#funcion del filtrado endpoinst 7
    date = None
    status = None
    cedula = None
    #traigo los datos del endpoints
    date = request.args.get("date")
    status = request.args.get("status")
    cedula = request.args.get("cedula")
    print(len(str(cedula)))

    con = connection()
    cur = con.cursor(cursor_factory=extras.RealDictCursor)

 
       
    if cedula != None and status != None and date != None:#esta condicion dice que si las variables date,status,cedula no son none trae los datos de la consulta
                cur.execute(
            "SELECT * FROM Pedido WHERE fecha_hora like %s AND status=%s AND ced_cliente=%s",
            (date + "%", status, cedula),
        )
                list_orders = cur.fetchall()

    elif (date != None and cedula != None) and status == None:#aqui es lo mismo pero  solo con date y cedula por si el status llega none
                cur.execute(
            "SELECT * FROM Pedido WHERE fecha_hora like %s AND ced_cliente=%s",
            (date + "%", cedula),
        )
                list_orders = cur.fetchall()

    elif (cedula != None and status != None) and date == None:
                cur.execute(
            "SELECT * FROM Pedido WHERE ced_cliente=%s AND status=%s",
            (cedula, status),
        )
                list_orders = cur.fetchall()

    elif (date != None and status != None) and cedula == None:#aqui es lo mismo pero solo que con la cedula
                cur.execute(
            "SELECT * FROM Pedido WHERE fecha_hora like %s AND status=%s",
            (date + "%", status),
        )
                list_orders = cur.fetchall()

    else:#si resulta que los datos mandados por el endpóinst son none retorna todo los datos de la tabla
                cur.execute("SELECT * FROM Pedido")
                list_orders = cur.fetchall()

    cur.close()
    con.close()
    return jsonify(list_orders)
                
if __name__ == "__main__":
    app.run(debug=True, port=4000)
