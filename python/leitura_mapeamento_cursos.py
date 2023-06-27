import pandas as pd

def ler_csv(nome_arquivo):
    data = pd.read_csv(nome_arquivo, header= 1)
    data = data.query('Situação == "ATIVO"')

    return data

def criar_setup(dados_planilha):
    resultado = {}

    for num_linha, linha in dados_planilha.iterrows():

        descricao = linha['Descrição']
        id_curso_id_ies = (linha['Código'], linha['Código IES'], linha)
        if not descricao in resultado:
            resultado[descricao] = [id_curso_id_ies]
        else:
            resultado[descricao].append(id_curso_id_ies)

    return resultado

def criar_inserts_registro_unificado(id_ies_mandatoria, lista_tuplas):
    inserts = ''
    for tuple in lista_tuplas:
        #id da ies mandatoria
        if(tuple[1] == id_ies_mandatoria):
            inserts += f'''INSERT INTO course (area_id, description, full_description, history_description, abbreviation, degree)             
                        SELECT cod_cent as area_id, des_curs, des_cur2, des_cur3, abr_curs, tipo_cur FROM oracle.course as legado 
                        WHERE legado.cod_curs = {tuple[0]} and legado.cod_empr = {id_ies_mandatoria} RETURNING id INTO id_unificado;\n'''
            
            break
    return inserts

def criar_inserts_legacy_course(lista_tuplas):
    inserts = ''
    for tuple in lista_tuplas:
        inserts += f'INSERT INTO legacy_course (legacy_course_id, institution_id, course_id) values ({tuple[0]},{tuple[1]},id_unificado);\n'

    return inserts

def criar_inserts_course_instituion(lista_tuplas):

    ies_sem_duplicacao = set()
    for tuple in lista_tuplas:
        ies_sem_duplicacao.add(tuple[1])

    inserts = ''
    for i in ies_sem_duplicacao:
        inserts += f'INSERT INTO course_institution (course_id, institution_id) VALUES (id_unificado,{i});\n'

    return inserts


def criar_script(inserts):
    with open('script.sql', 'w') as script_destino:
        script_destino.write(inserts)



def main():
    dados_planilha = ler_csv('mapeamento-cursos.csv')
    setup = criar_setup(dados_planilha)   

    inserts = ''
    for k, v in setup.items():

        if not k in ['ADMINISTRAÇÃO (BACHARELADO)','ARQUITETURA E URBANISMO (BACHARELADO)']:     
            continue

        inserts += f'\n-- {k}\n'

        insert_registro_unificado = criar_inserts_registro_unificado(1, v)

        if not (insert_registro_unificado):
            inserts += '-- Sem registro encontrado na IES mandatoria\n'
            continue

        inserts += insert_registro_unificado
        inserts += criar_inserts_legacy_course(v)
        inserts += criar_inserts_course_instituion(v)

    criar_script(inserts)
    
if __name__ == "__main__":
    main()


    

    

    #inserts_course_instituion += f' -- {i}\n'
    #inserts_course_instituion += f'insert into course_institution (course_id, institution_id) values (id_unificado,{tuple[1]});\n'
#inserts_course_institution = ''
#for i in resultado[]
#print(inserts)
#insert = 'insert into legacy_course (legacy_course_id, institution_id, course_id) values (,'', id_unificado);'

