import statistics
import cv2
import numpy as np
import json

from models.Camera import Camera
from models.Transporte import Transporte
from models.Vagao import Vagao

def run() -> None:

    with open("data.json", "r") as read_file:
        transporte = Transporte(json.loads(read_file.read()))

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

    df = cv2.HOGDescriptor()
    df.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    while True:

        for vagao in transporte.listaVagoes:
            camerasQtn = list()
            for camera in vagao.listaCameras:
                (sucesso, frame) = camera.captura.read()

                # Verifica se conseguiu fazer captura
                if sucesso:
                    frame = cv2.resize(frame, (640, 480))
                    frameCinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    # Realiza a contagem na imagem
                    pessoas, weigths = df.detectMultiScale(frameCinza, winStride=(4, 4), padding=(8, 8), scale=1.05)

                    for (x, y, l, a) in pessoas:
                        # display the detected boxes in the colour picture
                        cv2.rectangle(frame, (x, y), (x + l, y + a), (0, 255, 255), 2)

                    # Display the resulting frame
                    cv2.imshow('frame', frame)

                    # Verifica se conseguiu capturar algo
                    if type(pessoas) is np.ndarray:
                        camera.quantidadePessoas = pessoas.shape[0]
                        camerasQtn.append(camera.quantidadePessoas)

            # Calcula mediana
            if len(camerasQtn) > 0:
                vagao.quantidadePessoas = statistics.median(camerasQtn)
                print(f"Mediana: {camera.quantidadePessoas}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release
    for vagao in transporte.listaVagoes:
        for camera in vagao.listaCameras:
            camera.captura.release()

    cv2.destroyAllWindows()
    cv2.waitKey(1)

if __name__ == '__main__':
    run()

