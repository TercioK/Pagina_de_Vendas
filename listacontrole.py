from datetime import datetime
pegar_data_agora = datetime.now()
formatar_br_horario = pegar_data_agora.strftime("%d.%m.%Y")
formatar_br_horario_hora = pegar_data_agora.strftime("%d/%m/%Y %H:%M:%S")

# Criar a parte de Logs - Qualquer alteração vai ser documentada em TXT
def criar_logs(status, sobre):
    try:
        with open(f"Logs_{formatar_br_horario}.txt", "a") as arquivo:
            arquivo.write(f"---[LOGS - ({formatar_br_horario_hora})]---\n")

            if (status == "adicionar"):
                arquivo.write(f"[Alteração] - Foi feito uma alteração em {sobre}, adicionou na lista!\n")
            elif (status == "remover"):
                arquivo.write(f"[Removido] - Foi feito uma alteração em {sobre}, removeu na lista!\n")
            elif (status == "finalizou"):
                arquivo.write(f"[Finalizado] - O Cliente {sobre} finalizou a compra!\n")
    except FileNotFoundError:
        print(f"ERRO: Arquivo chamado *Logs_{formatar_br_horario}.txt* não foi encontrado! Tente criar um arquivo com esse nome, ou executar o codigo novamente.")

# Quando o codigo for executado pela primeira vez, o Python criar o arquivo pela primeira vez
def listatxt_produtos():
    try:
        with open("lista_produtos.txt", "r") as criar:
            pass
    except FileNotFoundError:
        with open("lista_produtos.txt", "w") as criar:
            criar.write("ID | NOME | PREÇO | QUANTIDADE\n")

# As coisas pra adicionar na lista
def lista_add_produtos(codigo_id, nome, valor, estoque_quant):
    try:
        with open("lista_produtos.txt", "a") as produtos:
            # Melhor Adicionar tudo em um Write so, pra facilitar a leitura! - 
            produtos.write(f"{codigo_id}, {nome}, {valor}, {estoque_quant}")
    except FileNotFoundError:
        print("ERRO: O arquivo com nome *lista_produtos.txt* não foi encontrado! Criando outro, espere...")
        listatxt_produtos()

# A parte que adiciona e atualiza as coisas da lista em Txt
def lista_atualizar_produtos(codigo_id, nome, valor, estoque_quant):
    try:
        with open("lista_produtos.txt", "r") as produtos:
            linhas = produtos.readlines()

        produtoencontrado = False
        with open("lista_produtos.txt", "w") as produtos:
            for linhaprodutos in linhas:
                # Vai ignorar a parte de ID e tals
                if ("ID | NOME | PREÇO | QUANTIDADE" in linhaprodutos):
                    produtos.write(linhaprodutos)
                    continue
                partes = linhaprodutos.strip().split(",")
                # Essa parte so vai continuar se tiver pelo menos uma linha depois
                if (len(partes) > 0):
                    id_atual = partes[0].strip()
                    if (id_atual == str(codigo_id)):
                        produtos.write(f"{codigo_id}, {nome}, {valor}, {estoque_quant}\n")
                        produtoencontrado = True
                    else:
                        produtos.write(linhaprodutos)
            if not produtoencontrado:
                # Melhor Adicionar tudo em um Write so, pra facilitar a leitura!
                produtos.write(f"{codigo_id}, {nome}, {valor}, {estoque_quant}\n")
        if produtoencontrado:
            # Parte dos Logs
            criar_logs("adicionar", f"ProdutoID: {codigo_id} foi atualizado para {nome}")
        else:
            criar_logs("adicionar", f"ProdutoID: {codigo_id} foi adicionado como novo na lista com nome: {nome}")
    except FileNotFoundError:
        print("ERRO: O arquivo *lista_produtos.txt* não foi encontrado! Criando outro...")
        listatxt_produtos()

# A parte que vai remover as coisas da lista em Txt
def lista_deletar_produtos(codigo_id):
    try:
        with open("lista_produtos.txt", "r") as produtos:
            linhas = produtos.readlines()
        foiencontrado = False
        with open("lista_produtos.txt", "w") as produtos:
            for linhasprodutos in linhas:
                if ("ID | NOME | PREÇO | QUANTIDADE" in linhasprodutos):
                    produtos.write(linhasprodutos)
                    continue
                partes = linhasprodutos.strip().split(",")
                # Essa parte so vai continuar se tiver pelo menos uma linha depois tambem
                if (len(partes) > 0):
                    id_atual = partes[0].strip()
                    if (id_atual == str(codigo_id)):
                        foiencontrado = True
                        continue
                    else:
                        produtos.write(linhasprodutos)
                if foiencontrado:
                    criar_logs("remover", f"O Produto com ID: {codigo_id} foi encontrado, e foi removido da lista em TXT!")
                else:
                    print(f"Não foi possivel remover nada da lista com ID: {codigo_id}! Tente novamente mais tarde...")
    except FileNotFoundError:
        print("ERRO: O arquivo *lista_produtos.txt* não foi encontrado! Criando outro...")
        listatxt_produtos()