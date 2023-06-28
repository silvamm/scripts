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

    ies_ids_unicos = set()
    for k, v in setup.items():
        for linha in v:
            ies_ids_unicos.add(linha['Código IES'])

    ies_ids = list(ies_ids_unicos)
    ies_ids.sort()
    return setup, ies_ids

def criar_inserts_registro_unificado(id_ies_mandatoria, linhas):
    inserts = ''
    for linha in linhas:
        #id da ies mandatoria
        if(linha['Código IES'] == id_ies_mandatoria):
            inserts += f'''\tINSERT INTO course (area_id, description, full_description, history_description, abbreviation, degree)             
                        SELECT cod_cent as area_id, des_curs, des_cur2, des_cur3, abr_curs, tipo_cur FROM oracle.course as legado 
                        WHERE legado.cod_curs = {linha["Código"]} and legado.cod_empr = {id_ies_mandatoria} RETURNING id INTO id_unificado;\n'''
            
            break

    return inserts

def criar_inserts_legacy_course(linhas):
    inserts = ''
    for linha in linhas:
        inserts += f'\tINSERT INTO legacy_course (legacy_course_id, institution_id, course_id) values ({linha["Código"]},{linha["Código IES"]},id_unificado);\n'

    return inserts

def criar_inserts_course_instituion(linhas):

    ies_sem_duplicacao = set()
    for linha in linhas:
        ies_sem_duplicacao.add(linha["Código IES"])

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
    setup, ies_ids = criar_setup(dados_planilha)   
    
    inserts = ''
    for descricao, linhas in setup.items():

        inserts += f'\n-- {descricao}\n'

        for id in ies_ids:    
            insert_registro_unificado = criar_inserts_registro_unificado(id, linhas)
            if(insert_registro_unificado):
                break

        if not (insert_registro_unificado):
            inserts += '-- Sem registro encontrado na IES mandatoria\n'
            continue

        inserts += insert_registro_unificado
        inserts += criar_inserts_legacy_course(linhas)
        inserts += criar_inserts_course_instituion(linhas)
    
    criar_script(inserts)

if __name__ == "__main__":
    main()