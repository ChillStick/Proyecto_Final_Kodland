# Importar
from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
from ultralytics import YOLO
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Cargar el modelo YOLO
model = YOLO('yolov8n.pt')  # Cambia por el modelo YOLO que prefieras

def result_calculate(size, lights, device):
    # Variables que permiten calcular el consumo energético de los aparatos
    home_coef = 100
    light_coef = 0.04
    devices_coef = 5   
    return size * home_coef + lights * light_coef + device * devices_coef 


def result_cuestculate(number1, number2, number3, number4, option1, option2, option3, option4):
    # Variables que permiten calcular el consumo energético de los aparatos  
    value1 = 0
    value2 = 0
    value3 = 0
    value4 = 0

    if option1 == "Sí":
        value1 = 0
    else:
        value1 = 10
    if option2 == "Sí":
        value2 = 10
    else:
        value2 = 0
    if option3 == "Sí":
        value3 = 0
    else:
        value3 = 10
    if option4 == "Sí":
        value4 = 10
    else:
        value4 = 0
    return (number1 * number3 * number4 + number2) / (value2 - value1 + value4 - value3)



# La primera página
@app.route('/')
def index():
    return render_template('index.html')
# Segunda página
@app.route('/<size>')
def lights(size):
    return render_template(
                            'lights.html', 
                            size=size
                           )

# La tercera página
@app.route('/<size>/<lights>')
def electronics(size, lights):
    return render_template(
                            'electronics.html',                           
                            size = size,
                            lights = lights
                           )

# Cálculo
@app.route('/<size>/<lights>/<device>')
def end(size, lights, device):
    return render_template('end.html', 
                            result=result_calculate(int(size),
                                                    int(lights), 
                                                    int(device)
                                                    )
                        )
# El formulario
@app.route('/form')
def form():
    return render_template('form.html')

# El cuestionario
@app.route('/cuest')
def cuest():
    return render_template('cuest.html')

# Busqueda
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Subir la imagen
        if 'image' not in request.files:
            return "No file uploaded", 400
        
        file = request.files['image']
        if file.filename == '':
            return "No file selected", 400

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Realizar detección con YOLO
        img = cv2.imread(filepath)
        results = model(img)

        # Dibujar las detecciones
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = int(box.cls[0])

                # Dibujar el rectángulo y la etiqueta
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    img, f"Class {cls} ({conf:.2f})", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
                )

        # Guardar la imagen procesada
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"output_{file.filename}")
        cv2.imwrite(output_path, img)

        return render_template('search.html', uploaded_image=file.filename, detected_image=f"output_{file.filename}")
    
    return render_template('search.html')

#Resultados del formulario
@app.route('/submit', methods=['POST'])
def submit_form():
    # Declarar variables para la recogida de datos
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']
    date = request.form['date']
    reason = request.form['reason']
    with open('form.txt', 'a',) as f:
        f.write(name + '/')
    with open('form.txt', 'a',) as f:
        f.write(email + '/')
    with open('form.txt', 'a',) as f:
        f.write(address + '/')
    with open('form.txt', 'a',) as f:
        f.write(date + '/')
    with open('form.txt', 'a',) as f:
        f.write(reason)
        f.write("\n")

    # Puedes guardar tus datos o enviarlos por correo electrónico
    return render_template('form_result.html', 
                           # Coloque aquí las variables
                           name=name,
                           email=email,
                           address=address,
                           date=date,
                           reason=reason,
                           )


@app.route('/result', methods=['POST'])
def submit_cuest():
    # Declarar variables para la recogida de datos
    number1 = request.form['number1']
    number2 = request.form['number2']
    number3 = request.form['number3']
    number4 = request.form['number4']
    option1 = request.form['option1']
    option2 = request.form['option2']
    option3 = request.form['option3']
    option4 = request.form['option4']
    more = request.form['more']
    with open('cuest.txt', 'a',) as f:
        f.write(number1 + '/')
    with open('cuest.txt', 'a',) as f:
        f.write(number2 + '/')
    with open('cuest.txt', 'a',) as f:
        f.write(number3 + '/')
    with open('cuest.txt', 'a',) as f:
        f.write(number4 + '/')
    with open('cuest.txt', 'a',) as f:
        f.write(option1 + '/')
    with open('cuest.txt', 'a',) as f:
        f.write(option2 + '/')
    with open('cuest.txt', 'a',) as f:
        f.write(option3 + '/')
    with open('cuest.txt', 'a',) as f:
        f.write(option4 + '/')
    with open('cuest.txt', 'a',) as f:
        f.write(more + '/')
        f.write("\n")
    
    return render_template('cuest_result.html', 
                            # Coloque aquí las variables
                            number1=number1,
                            number2=number2,
                            number3=number3,
                            number4=number4,
                            option1=(option1),
                            option2=(option2),
                            option3=(option3),
                            option4=(option4),
                            more=more,
                            finish=result_cuestculate(int(number1),
                                                    int(number2), 
                                                    int(number3),
                                                    int(number4),
                                                    (option1),
                                                    (option2),
                                                    (option3),
                                                    (option4),
                                                    )
                           )

app.run(debug=True)
