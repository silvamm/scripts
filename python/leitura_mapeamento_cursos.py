import pandas as pd

def ler_csv(nome_arquivo):
    data = pd.read_csv(nome_arquivo, header= 1)
    data = data.query('Situação == "ATIVO"')

    return data

def criar_setup(dados_planilha):
    setup = {}

    for i, linha in dados_planilha.iterrows():

        descricao = linha['Descrição']
        if not descricao in setup:
            setup[descricao] = [linha]
        else:
            setup[descricao].append(linha)

    return setup

def criar_inserts_registro_unificado(cadastros_legado):

    cadastro = min(cadastros_legado, key=lambda cadastro: cadastro['Código IES'])
    
    return f'''\tINSERT INTO course (area_id, description, full_description, history_description, abbreviation, degree)             
                    SELECT cod_cent as area_id, des_curs, des_cur2, des_cur3, abr_curs, tipo_cur FROM oracle.course as legado 
                    WHERE legado.cod_curs = {cadastro['Código']} and legado.cod_empr = {cadastro['Código IES']} RETURNING id INTO id_unificado;\n'''

def criar_inserts_legacy_course(cadastros_legado):
    inserts = ''
    for cadastro in cadastros_legado:
        inserts += f'\tINSERT INTO legacy_course (legacy_course_id, institution_id, course_id) values ({cadastro["Código"]},{cadastro["Código IES"]},id_unificado);\n'

    return inserts

def criar_inserts_course_instituion(cadastros_legado):

    ies_sem_duplicacao = set()
    for cadastro in cadastros_legado:
        ies_sem_duplicacao.add(cadastro["Código IES"])

    inserts = ''
    for i in ies_sem_duplicacao:
        inserts += f'\tINSERT INTO course_institution (course_id, institution_id) VALUES (id_unificado,{i});\n'

    return inserts

def criar_script(inserts):
    script = 'CREATE OR REPLACE FUNCTION unificar_cursos()\n\tRETURNS void\n\tLANGUAGE plpgsql\nAS\n$$\nDECLARE\n\tid_unificado integer;\nBEGIN'
    script += inserts
    script += 'END;\n$$'

    with open('script.sql', 'w') as script_destino:
        script_destino.write(script)

def main():
    dados_planilha = ler_csv('mapeamento-cursos.csv')
    setup = criar_setup(dados_planilha)   
    
    inserts = ''
    for nome_curso, cadastros_legado in setup.items():

        inserts += f'\n-- {nome_curso}\n'
        inserts += criar_inserts_registro_unificado(cadastros_legado)
        inserts += "\n"
        inserts += criar_inserts_legacy_course(cadastros_legado)
        inserts += "\n"
        inserts += criar_inserts_course_instituion(cadastros_legado)
    
    criar_script(inserts)

if __name__ == "__main__":
    main()