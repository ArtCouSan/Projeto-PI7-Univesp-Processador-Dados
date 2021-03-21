class Camera:

    def __init__(self, url: str, captura: any, quantidadePessoas: int):
        self.__url = url
        self.__captura = captura
        self.__quantidadePessoas = quantidadePessoas

    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, nova_url):
        self.__url = nova_url

    @property
    def captura(self):
        return self.__captura

    @captura.setter
    def captura(self, nova_captura):
        self.__captura = nova_captura

    @property
    def quantidadePessoas(self):
        return self.__quantidadePessoas

    @quantidadePessoas.setter
    def quantidadePessoas(self, nova_quantidadePessoas: int):
        self.__quantidadePessoas = nova_quantidadePessoas