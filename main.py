import statistics
import cv2
import numpy as np
import json
import requests

from models.Camera import Camera
from models.Transporte import Transporte
from models.Vagao import Vagao

def run() -> None:

    print("Iniciou....")

    # TODO: apagar depois de pronto
    mensagemDefault = ""

    # Configuracao do yolo
    net = cv2.dnn.readNet("yolo/yolov.weights", "yolo/yolov.cfg")

    with open("data.json", "r") as read_file:
        transporte = Transporte(json.loads(read_file.read()))

    # Carrega rotulos do modelo
    classes = []
    with open("yolo/coco.names", "r") as coco_file:
        classes = [line.strip() for line in coco_file.readlines()]

    # Define possiveis saidas do modelo
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Abre as cameras
    vagoes = list()
    for vagao in transporte.listaVagoes:
        vagao = Vagao(vagao)
        cameras = list()
        for camera in vagao.listaCameras:
            camera = Camera(camera)
            camera.captura = cv2.VideoCapture()
            camera.captura.open(camera.url)
            cameras.append(camera)
        vagao.listaCameras = cameras
        vagoes.append(vagao)
    transporte.listaVagoes = vagoes

    while True:

        transporteQtn = 0
        for vagao in transporte.listaVagoes:
            camerasQtn = list()
            for camera in vagao.listaCameras:

                # Realiza/Verifica a leitura
                (sucesso, img) = camera.captura.read()
                

                # Verifica se conseguiu fazer captura
                if sucesso:

                    # Infos do frame
                    img = cv2.resize(img, None, fx=0.4, fy=0.4)
                    height, width, channels = img.shape

                    # Pre processamento do video
                    blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)

                    # Detecta as saidas do video pelas configs de saida do YOLO
                    net.setInput(blob)
                    outs = net.forward(output_layers)

                    # Declara variaveis
                    class_ids = []
                    confidences = []
                    boxes = []
                    for out in outs:
                        for detection in out:
                            scores = detection[5:]
                            class_id = np.argmax(scores)
                            confidence = scores[class_id]

                            if confidence > 0.5:

                                # Objeto detectado
                                center_x = int(detection[0] * width)
                                center_y = int(detection[1] * height)
                                w = int(detection[2] * width)
                                h = int(detection[3] * height)

                                # Marca objeto
                                x = int(center_x - w / 2)
                                y = int(center_y - h / 2)

                                # Persiste marcacoes e objetos
                                boxes.append([x, y, w, h])
                                confidences.append(float(confidence))
                                class_ids.append(class_id)

                    pessoas = 0

                    # Non-maximum Suppresion
                    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
                    font = cv2.FONT_HERSHEY_PLAIN
                    colors = np.random.uniform(0, 255, size=(len(classes), 3))
                    for i in range(len(boxes)):
                        if i in indexes:
                            x, y, w, h = boxes[i]

                            #Verifica se existe o rotulo
                            label = str(classes[class_ids[i]])

                            # Caso seja uma pessoa detectada
                            if label.__eq__("person"):
                                color = colors[class_ids[i]]
                                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                                cv2.putText(img, label, (x, y + 30), font, 2, color, 3)
                                # Adiciona pessoa na temp
                                pessoas = pessoas + 1

                    # TODO: Remover no futuro, apenas para desenvolvimento
                    cv2.imshow("Image", cv2.resize(img, (800, 600)))

                    # Adiciona no objeto
                    camera.quantidadePessoas = pessoas
                    camerasQtn.append(camera.quantidadePessoas)


            # Calcula mediana
            if len(camerasQtn) > 0:
                vagao.quantidadePessoas = statistics.median(camerasQtn)
                transporteQtn = transporteQtn + vagao.quantidadePessoas

        if transporteQtn > transporte.limite:
            # TODO: apagar depois de pronto
            if mensagemDefault != "Ultrapassou o limite":
                mensagemDefault = "Ultrapassou o limite"
                print(mensagemDefault)
                requests.patch(url= transporte.urlApi + '/' + transporte.placaVeiculo + '/', data={
                   "estaLotado": True,
                   "qtnPassageirosAtual": transporteQtn,
                   "limite": transporte.limite
                })
                requests.get(url= transporte.urlArduino + "on")

        else:
            # TODO: apagar depois de pronto
            if mensagemDefault != "Dentro do limite":
                mensagemDefault = "Dentro do limite"
                print(mensagemDefault)
                requests.patch(url=transporte.urlApi + '/' + transporte.placaVeiculo + '/', data={
                    "estaLotado": False,
                    "qtnPassageirosAtual": transporteQtn,
                    "limite": transporte.limite
                })
                requests.get(url= transporte.urlArduino + "off")

        if cv2.waitKey(60) & 0xFF == ord('q'):
            break

    # Release
    for vagao in transporte.listaVagoes:
        for camera in vagao.listaCameras:
            camera.captura.release()

    cv2.destroyAllWindows()
    cv2.waitKey(1)

if __name__ == '__main__':
    run()


