import json
import os
import subprocess
import uuid


def encontrar_arquivos(diretorio, extensao):
    arquivos = []

    for raiz, diretorios, arquivos_nome in os.walk(diretorio):
        for arquivo_nome in arquivos_nome:
            if arquivo_nome.endswith(extensao):
                arquivos.append(os.path.join(raiz, arquivo_nome))

    return arquivos


def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

    return linhas


def gravar_arquivo(conteudo):
    path = "dados/preprocessamento/method"
    os.makedirs(path, exist_ok=True)

    cd_uuid = uuid.uuid4()
    caminho_arquivo = f"{path}/{cd_uuid}.json"

    with open(caminho_arquivo, "w") as arquivo:
        json.dump(conteudo, arquivo, indent=4)


def main():
    arquivos_cpp = encontrar_arquivos(
        diretorio="dados/insumo",
        extensao="cpp",
    )

    count = 1

    for arquivo in arquivos_cpp:
        data = subprocess.run(
            'ctags --output-format=json --format=2 --fields=+line ' + arquivo,
            shell=True,
            capture_output=True,
            text=True,
        ).stdout

        objs = []

        conteudo_arquivo = ler_arquivo(arquivo)

        for function in data.split('\n'):
            if function == '':
                continue

            function = json.loads(function)

            if function['kind'] != 'function':
                continue

            if 'scopeKind' not in function:
                continue

            if function['scopeKind'] != 'class':
                continue

            start_in_line = function['line']
            end_in_line = function['end']

            conteudo_function = conteudo_arquivo[start_in_line - 1:end_in_line]

            objs.append({
                'class': function['scope'],
                'method': function['name'],
                'start_in_line': start_in_line,
                'end_in_line': end_in_line,
                'conteudo': ''.join(conteudo_function),
            })

        objs = sorted(objs, key=lambda x: x['startInLine'])

        print(f"Arquivo {count}")
        count = count + 1

        gravar_arquivo({
            "arquivo": arquivo,
            "methods": objs,
        })

    print('END')
    exit(0)


if __name__ == '__main__':
    main()
