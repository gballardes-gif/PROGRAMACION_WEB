from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# Registros almacenados en memoria (se pierden al reiniciar el servidor)
historial_notas = []
historial_nombres = []


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/ejercicio/<int:numero>")
def ir_a_ejercicio(numero):
    if numero == 1:
        return redirect(url_for("ejercicio1"))
    elif numero == 2:
        return redirect(url_for("ejercicio2"))
    else:
        abort(404)


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    resultado = None

    if request.method == "POST":
        try:
            nota1 = int(request.form["nota1"])
            nota2 = int(request.form["nota2"])
            nota3 = int(request.form["nota3"])
            asistencia = int(request.form["asistencia"])
        except ValueError:
            abort(400)

        for nota in (nota1, nota2, nota3):
            if nota < 10 or nota > 70:
                abort(400)
        if asistencia < 0 or asistencia > 100:
            abort(400)

        promedio = calcular_promedio(nota1, nota2, nota3)

        if promedio >= 40 and asistencia >= 75:
            estado = "APROBADO"
        else:
            estado = "REPROBADO"

        resultado = {"promedio": promedio, "estado": estado}
        historial_notas.append(resultado)

    return render_template("ejercicio1.html", resultado=resultado, historial=historial_notas)


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    resultado = None

    if request.method == "POST":
        nombre1 = request.form["nombre1"].strip()
        nombre2 = request.form["nombre2"].strip()
        nombre3 = request.form["nombre3"].strip()

        if nombre1 == "" or nombre2 == "" or nombre3 == "":
            abort(400)

        mas_largo = nombre_mas_largo(nombre1, nombre2, nombre3)

        resultado = {"nombre": mas_largo, "cantidad": len(mas_largo)}
        historial_nombres.append(resultado)

    return render_template("ejercicio2.html", resultado=resultado, historial=historial_nombres)


def calcular_promedio(n1, n2, n3):
    return round((n1 + n2 + n3) / 3)


def nombre_mas_largo(n1, n2, n3):
    mayor = n1
    if len(n2) > len(mayor):
        mayor = n2
    if len(n3) > len(mayor):
        mayor = n3
    return mayor


if __name__ == "__main__":
    app.run(debug=True)