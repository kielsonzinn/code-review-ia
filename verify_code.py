import json
import os


def ler_arquivos_pasta(pasta):
    for arquivo in os.listdir(pasta):

        caminho_arquivo = os.path.join(pasta, arquivo)

        with open(caminho_arquivo, 'r') as file:

            conteudo = json.load(file)
            methods = conteudo.get('methods', [])

            lista_corretos = []
            lista_incorretos = []

            for metodo in methods:

                parametro = metodo.get('conteudo')
                resposta = input(f"Parâmetro: {parametro}. Digite 1 para correto ou 0 para incorreto: ")

                if resposta == '1':

                    lista_corretos.append(parametro)

                elif resposta == '0':

                    lista_incorretos.append(parametro)

                else:

                    print("Resposta inválida. Ignorando parâmetro.")

            gravar_arquivo_analisado(arquivo, lista_corretos, lista_incorretos)

            correto, incorreto = atualizar_contagem_analise(lista_corretos, lista_incorretos)
            resposta = input(f"QT_CORRETO: {correto}\nQT_INCORRETO: {incorreto}\nDeseja continuar (s/n)? ")
            
            if resposta.lower() != 's':
                return


def gravar_arquivo_analisado(arquivo, lista_corretos, lista_incorretos):
    nome_arquivo_analisado_correto = "correto_" + os.path.splitext(arquivo)[0] + ".json"
    nome_arquivo_analisado_incorreto = "correto_" + os.path.splitext(arquivo)[0] + ".json"

    pasta_analisado = "dados/preprocessamento/final"
    caminho_arquivo_analisado_correto = os.path.join(pasta_analisado, nome_arquivo_analisado_correto)
    caminho_arquivo_analisado_incorreto = os.path.join(pasta_analisado, nome_arquivo_analisado_incorreto)

    with open(caminho_arquivo_analisado_correto, 'w') as file:
        json.dump(lista_corretos, file)

    with open(caminho_arquivo_analisado_incorreto, 'w') as file:
        json.dump(lista_incorretos, file)


def atualizar_contagem_analise(lista_corretos, lista_incorretos):
    pasta_analisado = "dados/preprocessamento"
    caminho_data_json = os.path.join(pasta_analisado, "data.json")

    with open(caminho_data_json, 'r+') as file:
        data = json.load(file)
        corretos = len(lista_corretos) + data['qt_method_correto']
        incorretos = len(lista_incorretos) + data['qt_method_incorreto']
        data['qt_method_correto'] = corretos
        data['qt_method_incorreto'] = incorretos
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

    return corretos, incorretos


def main():
    ler_arquivos_pasta("dados/preprocessamento/method")


if __name__ == "__main__":
    main()

# TODO DEIXAR CADA LINHA QUE TEM LOG EM VERMELHO
# TODO MOVER O ARQUIVO ANALISADO PARA OUTRA PASTA
