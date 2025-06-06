from utils import limpar_nome_municipio
import pandas as pd
import numpy as np


try:
    print("Obtendo dados...")

    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    df_ocorrencia = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    # print(df_ocorrencia.head())

    for i in range(2):
        df_ocorrencia['munic'] = df_ocorrencia['munic'].apply(limpar_nome_municipio)

    # delimitando variáveis
    df_ocorrencia = df_ocorrencia[['munic', 'roubo_veiculo']]

    # totalizando
    df_roubo_veiculo = df_ocorrencia.groupby('munic').sum(['roubo_veiculo']).reset_index()
    # print(df_roubo_veiculo.to_string())


except Exception as e:
    print(f"Erro ao obter os dados: {e}")
    exit()

# iniciando analise
try:
    print('obtendo informações sobre padrão de roubo de veículos...')
    # array - performance computacional
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])
    # MEDIDAS DE TENDÊNCIA CENTRAL
    # media
    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    # mediana
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    # distancia
    distancia = abs((media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo)

    print("\nMEDIDAS DE TENDÊNCIA CENTRAL")
    print(30*"=")
    print(f"Média de roubos de veículos: {media_roubo_veiculo:.2f}")
    print(f"Mediana de roubos de veículos: {mediana_roubo_veiculo:.2f}")
    print(f"Distância entre média e mediana: {distancia:.3f}%")

    # MEDIDAS DE POSIÇÃO
    # Quatis
    q1 = np.quantile(array_roubo_veiculo, 0.25, method='weibull')
    q2 = np.quantile(array_roubo_veiculo, 0.50, method='weibull')
    q3 = np.quantile(array_roubo_veiculo, 0.75, method='weibull')

    print("\nMEDIDAS DE POSIÇÃO")
    print(30*"=")
    print(f"1º Quartil (Q1): {q1:.2f}")
    print(f"2º Quartil (Q2): {q2:.2f}")
    print(f"3º Quartil (Q3): {q3:.2f}")

    # ROUBAM MAIS E ROUBAM MENOS
    # Roubaram menos
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]
    # Roubaram mais
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]

    print("\nMunicipios com menores números de roubos de veículos")
    print(30*"=")
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))

    print("\nMunicipios com maiores números de roubos de veículos")
    print(30*"=")
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))

    # IDENTIFICAÇÃO DE OUTLIERS
    # IQR
    iqr = q3 - q1

    limite_superior = q3 + (1.5 * iqr)
    limite_inferior = q1 - (1.5 * iqr)

    print("\nLimites - Medidas de Posição")
    print(30*"=")
    print(f"Limite Inferior: {limite_inferior:.2f}")
    print(f"Limite Superior: {limite_superior:.2f}")

    # Descobrindo Outliers
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]

    # Outliers inferiores
    print("\nOutliers Inferiores")
    print(45*"=")
    if len(df_roubo_veiculo_outliers_inferiores) == 0:
        print("Nenhum outlier inferior encontrado.")
    else:
        print(df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True))

    # Outliers superiores
    print("\nOutliers Superiores")
    print(45*"=")
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print("Nenhum outlier superior encontrado.")
    else:
        print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))

except Exception as e:
    print(f"Erro ao obter os dados: {e}")
