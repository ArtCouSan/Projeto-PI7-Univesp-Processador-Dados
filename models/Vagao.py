from models.Camera import Camera


class Vagao:

    def __init__(self, listaCameras: list[Camera], quantidadePessoas: int):
        self.__listaCameras = listaCameras
        self.__quantidadePessoas = quantidadePessoas

    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])

    @property
    def listaCameras(self):
        return self.__listaCameras

    @listaCameras.setter
    def listaCameras(self, nova_listaCameras: list[Camera]):
        self.__listaCameras = nova_listaCameras

    @property
    def quantidadePessoas(self):
        return self.__quantidadePessoas

    @quantidadePessoas.setter
    def quantidadePessoas(self, nova_quantidadePessoas: int):
        self.__quantidadePessoas = nova_quantidadePessoas


