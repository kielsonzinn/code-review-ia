import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def carregar_dados(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        dados = json.load(arquivo)
    return dados


def qt_ocorrencia(testing, lista_de_strings):
    ocorrencias = 0

    for string in lista_de_strings:
        if string == testing:
            ocorrencias += 1

    return ocorrencias


def verify_testing(vectorizer, modelo, dados):
    vetor_novo_dado = vectorizer.transform(dados)
    previsao_novo_dado = modelo.predict(vetor_novo_dado)

    qt_ocorrencia_correto = qt_ocorrencia('Correto', previsao_novo_dado)
    qt_ocorrencia_incorreto = qt_ocorrencia('Incorreto', previsao_novo_dado)
    total = len(dados)
    percentual_acerto = qt_ocorrencia_correto * 100 / total
    percentual_erro = qt_ocorrencia_incorreto * 100 / total

    print(f"Quantidade dados: {total}")
    print(f"Acertou: {qt_ocorrencia_correto}")
    print(f"Errou: {qt_ocorrencia_incorreto}")
    print(f"Acertou em percentual: {percentual_acerto}")
    print(f"Errou em percentual: {percentual_erro}")


def verify_correct_testing(vectorizer, modelo):
    print(f'### Teste com logs corretos ###')
    verify_testing(vectorizer, modelo, carregar_dados('dados/correct_testing.json'))


def verify_incorrect_testing(vectorizer, modelo):
    print(f'### Teste com logs incorretos ###')
    verify_testing(vectorizer, modelo, carregar_dados('dados/incorrect_testing.json'))


def main():
    arquivo_corretos = 'dados/correct.json'
    arquivo_incorretos = 'dados/incorrect.json'

    dados_corretos = carregar_dados(arquivo_corretos)
    dados_incorretos = carregar_dados(arquivo_incorretos)

    dados_corretos = dados_corretos[:8000]
    dados_incorretos = dados_incorretos[:1000]

    dados = dados_corretos + dados_incorretos
    labels = ['Correto'] * len(dados_corretos) + ['Incorreto'] * len(dados_incorretos)

    vectorizer = TfidfVectorizer()
    vetor_dados = vectorizer.fit_transform(dados)

    x_treino, x_teste, y_treino, y_teste = train_test_split(vetor_dados, labels, test_size=0.2, random_state=42)

    modelo = LogisticRegression()
    modelo.fit(x_treino, y_treino)

    previsoes = modelo.predict(x_teste)
    acuracia = accuracy_score(y_teste, previsoes)

    qt_dados_corretos = len(dados_corretos)
    qt_dados_incorretos = len(dados_incorretos)

    print('### CRIACAO DO MODELO ###')
    print(f'Quantidade dados corretos: {qt_dados_corretos}')
    print(f'Quantidade dados incorretos: {qt_dados_incorretos}')
    print(f'Acurácia do modelo: {acuracia}\n')

    verify_correct_testing(vectorizer, modelo)
    print('')
    verify_incorrect_testing(vectorizer, modelo)


if __name__ == '__main__':
    main()
