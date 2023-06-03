import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


def main():
    # TODO LER DOS ARQUIVOS DE CORRETO E INCORRETO
    codigo_exemplos = [
        """
        int Myclass::soma( int n1, int n2 ) {
            qInfo() << 'Myclass::soma';
            ...
        }
        """,
        """
        int Myclass::divide( int n1, int n2 ) {
            qInfo() << 'Myclass::divide';
            ...
        }
        """,
        """
        int Myclass::soma( int n1, int n2 ) { 
            qInfo() << 'Myclass::nomeErrado'; 
            ... 
        }
        """,
        """
        int Myclass::divide( int n1, int n2 ) { 
            qInfo() << 'Myclass::erradoNome'; 
            ... 
        }
        """,
    ]

    # TODO CRIAR ESSAS CLASSES DE ACORDO COM OS ARQUIVOS, AONDE 0 INCORRETO, 1 CORRETO
    classes = np.array([1, 1, 0, 0])

    vectorizer = CountVectorizer()
    x = vectorizer.fit_transform(codigo_exemplos)

    model = LogisticRegression()
    model.fit(x, classes)

    novo_codigo = [
        """
        int Myclass::divide( int n1, int n2 ) { 
            qInfo() << 'Myclass::divide';
            ... 
        }
        """
    ]

    novo_codigo_vetorizado = vectorizer.transform(novo_codigo)

    # TODO VERIFICAR SE REALMENTE VAI CONSEGUIR IDENTIFICAR, HOJE TA IDENTIFICANDO SO SE FOR IGUAL AO QUE JA EXISTE,
    #  TALVEZ SO FALTE INSUMO DE DADOS
    predicao = model.predict(novo_codigo_vetorizado)

    if predicao[0] == 1:
        print("O trecho de código é considerado correto.")
    else:
        print("O trecho de código é considerado incorreto.")


if __name__ == '__main__':
    main()

# TODO LER OS DADOS DOS ARQUIVOS QUE TEM CORRETO E INCORRETO dados/preprocessamento/final E TREINAR O MODELO
# TODO DEPOIS DISSO LER OUTRA ARQUIVO DE TESTE E PARA CADA METHOD CHAMAR A FUNCAO E LOGAR SE ESTA CORRETO E INCORRETO
# TODO A CADA METHOD GRAVAR SE ACERTOU OU ERRO, E NO FINAL MOSTRAR O PERCENTUAL DE ACERTO
