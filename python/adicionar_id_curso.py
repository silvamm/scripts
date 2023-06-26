conteudo_arquivo = ""

def adicionar_id_curso(texto) :
    
    texto = texto.replace(',ID_ADMINISTRAÇÃO (BACHARELADO),', ',1,')
    texto = texto.replace(',ID_ARQUITETURA E URBANISMO (BACHARELADO),', ',2,')
    texto = texto.replace(',ID_BIOMEDICINA (BACHARELADO),', ',3,')
    texto = texto.replace(',ID_CIÊNCIA DA COMPUTAÇÃO (BACHARELADO),', ',4,')
    texto = texto.replace(',ID_CIÊNCIAS BIOLÓGICAS (BACHARELADO),', ',5,')
    texto = texto.replace(',ID_CIÊNCIAS CONTÁBEIS (BACHARELADO),', ',6,')
    texto = texto.replace(',ID_DIREITO (BACHARELADO),', ',7,')
    texto = texto.replace(',ID_EDUCAÇÃO FÍSICA (BACHARELADO),', ',8,')
    texto = texto.replace(',ID_EDUCAÇÃO FÍSICA (LICENCIATURA),', ',9,')
    texto = texto.replace(',ID_ENGENHARIA DE PRODUÇÃO (BACHARELADO),', ',10,')
    texto = texto.replace(',ID_FARMÁCIA (BACHARELADO),', ',11,')
    texto = texto.replace(',ID_FISIOTERAPIA (BACHARELADO),', ',12,')
    texto = texto.replace(',ID_JORNALISMO (BACHARELADO),', ',13,')
    texto = texto.replace(',ID_PEDAGOGIA (LICENCIATURA),', ',14,')
    texto = texto.replace(',ID_PSICOLOGIA (BACHARELADO),', ',15,')
    texto = texto.replace(',ID_PUBLICIDADE E PROPAGANDA (BACHARELADO),', ',16,')
    texto = texto.replace(',ID_Engenharia da Computação,', ',17,')
    texto = texto.replace('|', '')
    return texto

with open('script_origem_dbeaver.txt','r') as script_origem:
    conteudo_arquivo = script_origem.read()

with open('script_destino.sql', 'w') as script_destino:
    conteudo_arquivo = adicionar_id_curso(conteudo_arquivo)
    script_destino.write(conteudo_arquivo)
    


