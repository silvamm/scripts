import pandas as pd

def ler_csv(nome_arquivo):
    data = pd.read_csv(nome_arquivo, header= 1)
    data = data.query('Situação == "ATIVO"')

    return data

def criar_inserts_registro_unificado(resultado, id_ies_mandatoria, chave):
    inserts = ''
    resultado[chave]

    for k, v in resultado.items():
        if not (k == chave):
            continue
        inserts += f'-- {i}\n'
        for tuple in v:
            #id da ies mandatoria
            if(tuple[1] == id_ies_mandatoria):
                inserts += f'''INSERT INTO course (area_id, description, full_description, history_description, abbreviation, degree)             
                            SELECT cod_cent as area_id, des_curs, des_cur2, des_cur3, abr_curs, tipo_cur FROM oracle.course as legado 
                            WHERE legado.cod_curs = {tuple[0]} and legado.cod_empr = {id_ies_mandatoria} RETURNING id INTO id_unificado;\n'''
                
                break
    return inserts

def criar_inserts_legacy_course(resultado, chave):
    inserts = ''

    for k, v in resultado.items():
        inserts += '\n'
        for tuple in v:
            inserts += f'insert into legacy_course (legacy_course_id, institution_id, course_id) values ({tuple[0]},{tuple[1]},id_unificado);\n'

    return inserts

def criar_script(inserts):
    with open('script.sql', 'w') as script_destino:
        script_destino.write(inserts)


def criar_setup(dados_planilha):
    resultado = ''

    for num_linha, linha in dados_planilha.iterrows():

        descricao = linha['Descrição']
        id_curso_id_ies = (linha['Código'], linha['Código IES'], linha)
        if not descricao in resultado:
            resultado[descricao] = [id_curso_id_ies]
        else:
            resultado[descricao].append(id_curso_id_ies)

    return resultado

dados_planilha = ler_csv('mapeamento-cursos.csv')
setup = criar_setup(dados_planilha)   
inserts = ''
for k, v in setup:     
    inserts += f'-- {k}\n'

    

    

    #inserts_course_instituion += f' -- {i}\n'
    #inserts_course_instituion += f'insert into course_institution (course_id, institution_id) values (id_unificado,{tuple[1]});\n'
#inserts_course_institution = ''
#for i in resultado[]
#print(inserts)
#insert = 'insert into legacy_course (legacy_course_id, institution_id, course_id) values (,'', id_unificado);'

