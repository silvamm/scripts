require 'csv'
require 'money'

I18n.config.available_locales = :en
Money.locale_backend = :i18n
Money.rounding_mode = BigDecimal::ROUND_HALF_EVEN

$total_ifood = Money.from_amount(0, "BRL")

def csv_to_transactions(nome_arquivo)

    total = Money.from_amount(0, "BRL")
    itens_selecionados = 0

    CSV.foreach('C:\Users\mathe\Projetos\scripts\/' + nome_arquivo + '.csv',
         headers: ['Data da transacao', 'Estabelecimento', 'Tipo da transacao', 'Valor'], encoding:'iso-8859-1:utf-8', col_sep: ';' ).with_index do |row, i|
        
        nome_estabelecimento = row.field('Estabelecimento')

        next if nome_estabelecimento.nil?

        if nome_estabelecimento.downcase.include? "ifood" 
            
            valor = row.field('Valor')
            operador = valor[0]    
            valor = in_cents(valor)

            centavos = Money.from_cents(valor.to_i, "BRL")
        
            if operador == "+"
                puts "#{row.field('Data da transacao')} | #{nome_estabelecimento} | #{row.field('Valor')}"
                itens_selecionados += 1
                total = total + centavos   
            end
        end
    end
    $total_ifood = $total_ifood + total
    puts "Itens encontrados " + itens_selecionados.to_s
    puts "Resultado: " + total.format 
    total
end

def in_cents(valor)
    valor = valor[1..]    
    valor = valor.sub(",", "")
    valor = valor.sub(".", "")
    valor
end

def read_csv(meses, year)
    puts "#" * 100
    puts year.to_s
    for i in  meses do
        if i.negative?
            puts Date::MONTHNAMES[-i]
        else
            puts Date::MONTHNAMES[i]
        end
        nome_arquivo = 'Fatura' + i.to_s
        csv_to_transactions(nome_arquivo)
    end
    puts "#" * 100
end

meses2023 = [1,2,3,4,5]
meses2022 = [-12,-11,-10,-9,-8,-7,-5]

read_csv(meses2023, 2023)
read_csv(meses2022, 2022)

puts "Total de IFood em 12 meses é " + $total_ifood.format
puts "Média de " + ($total_ifood / 12).format


