import os

from django.core.files.storage import FileSystemStorage


def save(file):
    pasta = "core/static/img/"

    # Verificando se o caminho já existe
    if os.path.isdir(pasta):
        return configuracao_upload_foto(pasta, file)
    else:
        # Criando o caminho caso não exista
        os.mkdir(pasta)
        return configuracao_upload_foto(pasta, file)

def configuracao_upload_foto(pasta ,file):
    pasta += file.name
    fs = FileSystemStorage()
    filename = fs.save(pasta, file)
    upload_file = fs.url(filename)
    return upload_file



