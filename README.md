# Requisitos

- python >= 3.9
- ctags

# Pre processamento

- Execute o extract.py passando 2 argumentos
    - --PATH_TRAINING
      - Esse corresponde ao path da pasta que contem codigo c++ para treinamento do modelo
    - --PATH_TESTING
      - Esse corresponde ao path da pasta que contem codigo c++ para teste do modelo
- Esse extract.py, ira ler cada arquivo ".h" e ".cpp", usando uma ferramenta para separar o codigo por method, na sequência ira verificar cada linha que corresponde a uma linha de log, separando essas linhas como corretas e incorretas, gerando assim 4 arquivos json
  - dados/correct.json
    - Contem os logs no formato correto para treinamento
  - dados/incorrect.json
      - Contem os logs no formato incorreto para treinamento
  - dados/correct_testing.json
    - Contem os logs no formato correto para teste
  - dados/incorrect_testing.json
    - Contem os logs no formato incorreto para teste
- Todo esse processo gera dados para treinar o modelo, ja pre processados

# Treinamento

- Execute o review.py que ira ler o correct.json e incorrect.json, com isso ira treinar o modelo, usando 80% dos dados, os outros 20% ira usar para testar o percentual de acerto do modelo
- Na sequência, para ter um percentual mais visivel de acerto, ira ler o correct_testing.json e incorrect_testing.json e usar o modelo para verificar o codigo de teste, e dessa forma chegar a um percentual de acerto

# Dados

- Caso 01
```
### CRIACAO DO MODELO ###
Quantidade dados corretos: 9084
Quantidade dados incorretos: 1187
Acurácia do modelo: 0.9148418491484185

### Teste com logs corretos ###
Quantidade dados: 2344
Acertou: 1053
Errou: 1291
Acertou em percentual: 44.92320819112628
Errou em percentual: 55.07679180887372

### Teste com logs incorretos ###
Quantidade dados: 83
Acertou: 52
Errou: 31
Acertou em percentual: 62.65060240963855
Errou em percentual: 37.34939759036145
```

- Caso 02
```
### CRIACAO DO MODELO ###
Quantidade dados corretos: 1000
Quantidade dados incorretos: 1000
Acurácia do modelo: 0.9575

### Teste com logs corretos ###
Quantidade dados: 2344
Acertou: 346
Errou: 1998
Acertou em percentual: 14.761092150170649
Errou em percentual: 85.23890784982935

### Teste com logs incorretos ###
Quantidade dados: 83
Acertou: 7
Errou: 76
Acertou em percentual: 8.433734939759036
Errou em percentual: 91.56626506024097
```

Caso 03
```
### CRIACAO DO MODELO ###
Quantidade dados corretos: 2000
Quantidade dados incorretos: 1000
Acurácia do modelo: 0.9133333333333333

### Teste com logs corretos ###
Quantidade dados: 2344
Acertou: 1807
Errou: 537
Acertou em percentual: 77.09044368600682
Errou em percentual: 22.909556313993175

### Teste com logs incorretos ###
Quantidade dados: 83
Acertou: 58
Errou: 25
Acertou em percentual: 69.87951807228916
Errou em percentual: 30.120481927710845
```

Caso 04
```
### CRIACAO DO MODELO ###
Quantidade dados corretos: 8000
Quantidade dados incorretos: 1000
Acurácia do modelo: 0.9122222222222223

### Teste com logs corretos ###
Quantidade dados: 2344
Acertou: 2013
Errou: 331
Acertou em percentual: 85.87883959044369
Errou em percentual: 14.121160409556314

### Teste com logs incorretos ###
Quantidade dados: 83
Acertou: 74
Errou: 9
Acertou em percentual: 89.1566265060241
Errou em percentual: 10.843373493975903
```

# O que foi usado?

Modelo de regressão logística e a técnica de extração de recursos TF-IDF (Term Frequency-Inverse Document Frequency) em texto.

# Explicando melhor

1. Modelo de regressão logística:
   A regressão logística é um algoritmo de aprendizado de máquina usado principalmente para tarefas de classificação binária, onde o objetivo é prever uma classe-alvo entre duas possíveis. No entanto, também pode ser estendido para tarefas de classificação multiclasse.

   O modelo de regressão logística utiliza a função logística (também conhecida como sigmoid) para realizar a classificação. A função sigmoid mapeia o resultado de uma combinação linear de características para um valor entre 0 e 1, representando a probabilidade de pertencer à classe positiva. Se a probabilidade calculada for maior que um determinado limite, geralmente 0,5, o exemplo é classificado como pertencente à classe positiva; caso contrário, é classificado como pertencente à classe negativa.

   Durante o treinamento, o modelo de regressão logística ajusta os pesos das características para maximizar a verossimilhança dos dados observados. Esse processo é geralmente realizado usando técnicas de otimização, como a descida de gradiente.

2. Técnica de extração de recursos TF-IDF:
   A técnica TF-IDF (Term Frequency-Inverse Document Frequency) é uma abordagem amplamente utilizada para converter texto numa representação numérica que pode ser usada em algoritmos de aprendizado de máquina. É particularmente útil para lidar com grandes volumes de texto, como documentos ou coleções de palavras.

   O TF-IDF considera a frequência de um termo num documento e em toda a coleção de documentos. Ele calcula um peso para cada termo que considera tanto a frequência do termo no documento específico (TF) quanto a raridade do termo em toda a coleção de documentos (IDF).

   A pontuação TF-IDF de um termo aumenta proporcionalmente à sua frequência no documento e diminui à medida que ocorre em mais documentos da coleção. Isso ajuda a identificar termos frequentes num documento específico, mas raros na coleção, fornecendo uma indicação da importância do termo para aquele documento em particular.

   Ao aplicar a técnica TF-IDF, os documentos de texto são transformados numa matriz numérica, onde cada linha representa um documento e cada coluna representa um termo do vocabulário. Os valores na matriz representam as pontuações TF-IDF de cada termo no respectivo documento.
