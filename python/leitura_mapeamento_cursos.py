import pandas as pd

def ler_csv(nome_arquivo):
    data = pd.read_csv(nome_arquivo, header= 1)
    data = data.query('Situação == "ATIVO"')

    return data

def criar_setup(dados_planilha):
    resultado = {}

    for num_linha, linha in dados_planilha.iterrows():

        descricao = linha['Descrição']

        dados = {} 
        dados["Código Legado"] = linha['Código']
        dados["Código IES"] = linha['Código IES']
        dados["Info"] = linha
        
        if not descricao in resultado:
            resultado[descricao] = [dados]
        else:
            resultado[descricao].append(dados)

    return resultado

def criar_inserts_registro_unificado(id_ies_mandatoria, dados):
    inserts = ''
    for dado in dados:
        #id da ies mandatoria
        if(dado["Código IES"] == id_ies_mandatoria):
            inserts += f'''\tINSERT INTO course (area_id, description, full_description, history_description, abbreviation, degree)             
                        SELECT cod_cent as area_id, des_curs, des_cur2, des_cur3, abr_curs, tipo_cur FROM oracle.course as legado 
                        WHERE legado.cod_curs = {dado["Código Legado"]} and legado.cod_empr = {id_ies_mandatoria} RETURNING id INTO id_unificado;\n'''
            
            break

    return inserts

def criar_inserts_legacy_course(dados):
    inserts = ''
    for dado in dados:
        inserts += f'\tINSERT INTO legacy_course (legacy_course_id, institution_id, course_id) values ({dado["Código Legado"]},{dado["Código IES"]},id_unificado);\n'

    return inserts

def criar_inserts_course_instituion(dados):

    ies_sem_duplicacao = set()
    for dado in dados:
        ies_sem_duplicacao.add(dado["Código IES"])

    inserts = ''
    for i in ies_sem_duplicacao:
        inserts += f'\tINSERT INTO course_institution (course_id, institution_id) VALUES (id_unificado,{i});\n'

    return inserts

def criar_script(inserts):
    script = 'CREATE OR REPLACE FUNCTION unificar_cursos()\n\tRETURNS void\n\tLANGUAGE plpgsql\nAS\n$$\nDECLARE\n\tid_unificado integer;\nBEGIN'
    script += inserts
    script += 'END;\n$$'

    with open('script.sql', 'w') as script_destino:
        script_destino.write(inserts)

def main():
    dados_planilha = ler_csv('mapeamento-cursos.csv')
    setup = criar_setup(dados_planilha)   

    inserts = ''
    for k, v in setup.items():
        
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