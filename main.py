import cv2
import numpy


def redim(img, largura):
	alt = int(img.shape[0]/img.shape[1]*largura)
	img = cv2.resize(img, (largura, alt), interpolation =cv2.INTER_AREA)
	return img

cameraFrontalURL: str = 'http://192.168.0.104:8080/video'
# cameraLateralDireitaURL: str = 'http://192.168.0.104:8081/video'
# cameraLateralEsquerdaURL: str = 'http://192.168.0.104:8082/video'
# cameraTraseiraURL: str = 'http://192.168.0.104:8083/video'
arduinoURL: str = ""

capFrontal = cv2.VideoCapture()
capFrontal.open(cameraFrontalURL)

# capLateralDireita = cv2.VideoCapture()
# capLateralDireita.open(cameraLateralDireitaURL)
#
# capLateralEsquerda = cv2.VideoCapture()
# capLateralEsquerda.open(cameraLateralEsquerdaURL)
#
# capTraseira = cv2.VideoCapture()
# capTraseira.open(cameraTraseiraURL)

#Criação do detector de faces
df = cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml')
quantidadePessoasCameraFrontal = 0

while True:

	(sucessoFrontal, frameFrontal) = capFrontal.read()
	# (sucessoLateralDireita, frameLateralDireita) = capLateralDireita.read()
	# (sucessoLateralEsquerda, frameLateralEsquerda) = capLateralEsquerda.read()
	# (sucessoTraseira, frameTraseira) = capTraseira.read()

	if sucessoFrontal:
		frameFrontal = redim(frameFrontal, 320)
		frameFrontalCinza = cv2.cvtColor(frameFrontal, cv2.COLOR_BGR2GRAY)
		faces = df.detectMultiScale(frameFrontalCinza, scaleFactor=1.1, minNeighbors=8, minSize=(25, 25))
		frameFrontalTemp = frameFrontal.copy()
		for (x, y, l, a) in faces:
			cv2.rectangle(frameFrontalTemp, (x, y), (x + l, y + a), (0, 255, 255), 2)
		if type(faces) is numpy.ndarray:
			if quantidadePessoasCameraFrontal != faces.shape[0]:
				quantidadePessoasCameraFrontal = faces.shape[0]
				print(quantidadePessoasCameraFrontal)
		cv2.imshow('Camera frontal', redim(frameFrontalTemp, 640))

	# if sucessoLateralDireita:
	# 	cv2.imshow("frameLateralDireita", frameLateralDireita)
	#
	# if sucessoLateralEsquerda:
	# 	cv2.imshow("frameLateralEsquerda", frameLateralEsquerda)
	#
	# if sucessoTraseira:
	# 	cv2.imshow("frameTraseira", frameTraseira)

	key = cv2.waitKey(1)

	if key == 27:
		break

capFrontal.release()
# capLateralDireita.release()
# capLateralEsquerda.release()
# capTraseira.release()

cv2.destroyAllWindows()