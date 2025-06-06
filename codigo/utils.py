import re
import unicodedata

substituicoes = {
    "Armaaao Dos Baaozios": "Armação dos Búzios",
    "Armaaao Dos Baozios": "Armação dos Búzios",
    "Armacao Dos Buzios": "Armação dos Búzios",
    "Conceiaao De Macabaao": "Conceição de Macabu",
    "Conceiaao De Macabao": "Conceição de Macabu",
    "Conceicao De Macabu": "Conceição de Macabu",
    "Itaboraa": "Itaboraí",
    "Itaboraaa": "Itaboraí",
    "Itaguaa": "Itaguaí",
    "Itaguaaa": "Itaguaí",
    "Itaguai": "Itaguaí",
    "Laje Do Muriaa": "Laje do Muriaé",
    "Laje Do Muriaaa": "Laje do Muriaé",
    "Laje Do Muriae": "Laje do Muriaé",
    "Macaa": "Macaé",
    "Macaaa": "Macaé",
    "Maga": "Magé",
    "Magaa": "Magé",
    "Marica": "Maricá",
    "Maricaa": "Maricá",
    "Nitera3I": "Niterói",
    "Niteraa3I": "Niterói",
    "Niteroi": "Niterói",
    "Nova Iguaaau": "Nova Iguaçu",
    "Nova Iguaau": "Nova Iguaçu",
    "Nova Iguacu": "Nova Iguaçu",
    "Paraaaba Do Sul": "Paraíba do Sul",
    "Paraaba Do Sul": "Paraíba do Sul",
    "Paraiba Do Sul": "Paraíba do Sul",
    "Petra3Polis": "Petrópolis",
    "Petraa3Polis": "Petrópolis",
    "Petropolis": "Petrópolis",
    "Piraa": "Piraí",
    "Piraaa": "Piraí",
    "Porciaaoncula": "Porciúncula",
    "Porciaoncula": "Porciúncula",
    "Porciuncula": "Porciúncula",
    "Quissama": "Quissamã",
    "Quissamaa": "Quissamã",
    "Saao Fidaalis": "São Fidélis",
    "Sao Fidalis": "São Fidélis",
    "Sao Fidelis": "São Fidélis",
    "Saao Francisco De Itabapoana": "São Francisco de Itabapoana",
    "Sao Francisco De Itabapoana": "São Francisco de Itabapoana",
    "Saao Gonaaalo": "São Gonçalo",
    "Sao Gonaalo": "São Gonçalo",
    "Sao Goncalo": "São Gonçalo",
    "Saao Joaao Da Barra": "São João da Barra",
    "Sao Joao Da Barra": "São João da Barra",
    "Saao Joaao De Meriti": "São João de Meriti",
    "Sao Joao De Meriti": "São João de Meriti",
    "Saao Josaa Do Vale Do Rio Preto": "São José do Vale do Rio Preto",
    "Sao Josa Do Vale Do Rio Preto": "São José do Vale do Rio Preto",
    "Sao Jose Do Vale Do Rio Preto": "São José do Vale do Rio Preto",
    "Saao Pedro Da Aldeia": "São Pedro da Aldeia",
    "Sao Pedro Da Aldeia": "São Pedro da Aldeia",
    "Saao Sebastiaao Do Alto": "São Sebastião do Alto",
    "Sao Sebastiao Do Alto": "São Sebastião do Alto",
    "Seropaadica": "Seropédica",
    "Seropadica": "Seropédica",
    "Seropedica": "Seropédica",
    "Tangua": "Tanguá",
    "Tanguaa": "Tanguá",
    "Teresaa3Polis": "Teresópolis",
    "Teresa3Polis": "Teresópolis",
    "Teresopolis": "Teresópolis",
    "Valenaa": "Valença",
    "Valenaaa": "Valença",
    "Valenca": "Valença",
    "Nilaa3Polis": "Nilópolis",
    "Nila3Polis": "Nilópolis",
    "Nilopolis": "Nilópolis",

    # compostos
    "Mag�;Guapimirim": "Magé;Guapimirim",
    "Itabora��;Tangu��": "Itaboraí;Tanguá",
    "Maca�;Quissam�;Carapebus": "Macaé;Quissamã;Carapebus",
    "Cabo Frio;Arraial do Cabo": "Cabo Frio;Arraial do Cabo",
    "Santo Ant�nio de P�dua;Aperib�": "Santo Antônio de Pádua;Aperibé",
    "Natividade;Varre-Sai": "Natividade;Varre-Sai",
    "Itaperuna;S�o Jos� de Ub�;Cardoso Moreira;Italva": "Itaperuna;São José de Ubá;Cardoso Moreira;Italva",
    "Campos dos Goytacazes;S�o Francisco de Itabapoana": "Campos dos Goytacazes;São Francisco de Itabapoana",
    "Pira��;Pinheiral": "Piraí;Pinheiral",
    "Comendador Levy Gasparian;Areal;Tr�s Rios": "Comendador Levy Gasparian;Areal;Três Rios",
    "Miguel Pereira;Paty dos Alferes": "Miguel Pereira;Paty dos Alferes",
    "Cordeiro;Macuco": "Cordeiro;Macuco",
    "Porto Real;Quatis": "Porto Real;Quatis"
}


def limpar_nome_municipio(texto):
    if not isinstance(texto, str):
        return texto

    texto = texto.strip()

    # PRIMEIRO: tentar corrigir agrupamentos completos
    if texto in substituicoes:
        return substituicoes[texto]

    # SENÃO: dividir e corrigir um a um
    partes = texto.split(";")
    partes_corrigidas = []

    for parte in partes:
        parte = parte.strip()
        if parte in substituicoes:
            corrigido = substituicoes[parte]
        else:
            temp = re.sub(r'\d+', '', parte)
            temp = unicodedata.normalize('NFKD', temp)
            temp = temp.encode('ASCII', 'ignore').decode('utf-8')
            temp = re.sub(r'(.)\1{2,}', r'\1\1', temp)
            corrigido = temp.strip().title()

        partes_corrigidas.append(corrigido)

    return ";".join(partes_corrigidas)
