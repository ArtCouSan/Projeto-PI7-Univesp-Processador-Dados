from models.Vagao import Vagao


class Transporte:

    def __init__(self, listaCameras: list[Vagao], urlArduino: str, urlApi: str, limite: int, placaVeiculo: str):
        self.__listaCameras = listaCameras
        self.__urlArduino = urlArduino
        self.__limite = limite
        self.__placaVeiculo = placaVeiculo
        self.__urlApi = urlApi

    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])

    @property
    def listaVagoes(self):
        return self.__listaVagoes

    @listaVagoes.setter
    def listaVagoes(self, nova_listaVagoes: list[Vagao]):
        self.__listaVagoes = nova_listaVagoes

    @property
    def urlArduino(self):
        return self.__urlArduino

    @urlArduino.setter
    def urlArduino(self, nova_urlArduino: str):
        self.__urlArduino = nova_urlArduino

    @property
    def limite(self):
        return self.__limite

    @limite.setter
    def limite(self, nova_limite: int):
        self.__limite = nova_limite

    @property
    def placaVeiculo(self):
        return self.__placaVeiculo

    @placaVeiculo.setter
    def placaVeiculo(self, nova_placaVeiculo: str):
        self.__placaVeiculo = nova_placaVeiculo

    @property
    def urlApi(self):
        return self.__urlApi

    @urlApi.setter
    def urlApi(self, nova_urlApi: str):
        self.__urlApi = nova_urlApi
