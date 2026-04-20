from pdv_library import PDVSystem
# Prints como forma de carregamento do sistema
print("Iniciando o sistema PDV...")
print("Carregando biblioteca...")
print("Biblioteca carregada com sucesso!")
print("Bem-vindo ao Sistema PDV!")
# Menus
def mostrar_menu():
    print("\n===== MENU PDV =====")
    print("1. Produtos")
    print("2. Vendedores")
    print("3. Clientes")
    print("4. Listar Cadastros")
    print("5. Carrinho de Compras")
    print("6. Relatório de Vendas")
    print("7. Sair")

def menu_produtos(pdv):
    while True:
        print("\n--- Menu Produtos ---")
        print("1. Adicionar/Atualizar Produto")
        print("2. Remover Produto")
        print("3. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            codigo = input("Código do produto: ")
            nome = input("Nome do produto: ")
            valor = float(input("Valor do produto (R$): "))
            estoque = int(input("Quantidade em estoque: "))
            pdv.cadastrar_produto(codigo, nome, valor, estoque)
            print("Produto cadastrado/atualizado com sucesso!")
        
        elif escolha == '2':
            codigo = input("Código do produto a remover: ")
            if pdv.remover_produto(codigo):
                print("Produto removido com sucesso.")
            else:
                print("Produto não encontrado.")
        
        elif escolha == '3':
            break
        
        else:
            print("Opção inválida. Tente novamente.")

def menu_vendedores(pdv):
    while True:
        print("\n--- Menu Vendedores ---")
        print("1. Adicionar/Atualizar Vendedor")
        print("2. Remover Vendedor")
        print("3. Voltar")
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            codigo = input("Código do vendedor: ")
            nome = input("Nome do vendedor: ")
            pdv.cadastrar_vendedor(codigo, nome)
            print("Vendedor cadastrado/atualizado com sucesso!")

        elif escolha == '2':
            codigo = input("Código do vendedor a remover: ")
            if pdv.remover_vendedor(codigo):
                print("Vendedor removido com sucesso.")
            else:
                print("Vendedor não encontrado.")
        elif escolha == '3':
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_clientes(pdv):
    while True:
        print("\n--- Menu Clientes ---")
        print("1. Adicionar/Atualizar Cliente")
        print("2. Remover Cliente")
        print("3. Voltar")
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            codigo = input("Código do cliente: ")
            nome = input("Nome do cliente: ")
            pdv.cadastrar_cliente(codigo, nome)
            print("Cliente cadastrado/atualizado com sucesso!")

        elif escolha == '2':
            codigo = input("Código do cliente a remover: ")
            if pdv.remover_cliente(codigo):
                print("Cliente removido com sucesso.")
            else:
                print("Cliente não encontrado.")
        
        elif escolha == '3':
            break
        
        else:
            print("Opção inválida. Tente novamente.")
# Natan
def menu_carrinho(pdv):
    while True:
        print("\n--- Carrinho de Compras ---")
        print("1. Adicionar Item")
        print("2. Remover Item")
        print("3. Finalizar Compra")
        print("4. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            codigo = input("Código do produto: ")
            nome = "" 
            quantidade = int(input("Quantidade a adicionar: "))
            resultado = pdv.adicionar_item_carrinho(codigo, nome, quantidade)
            print(resultado)
            if "adicionado" in resultado:
                if codigo in pdv.produtos:
                    print(f"Estoque disponível: {pdv.produtos[codigo]['estoque']}")
        
        elif opcao == '2':
            codigo = input("Código do produto a remover: ")
            nome = "" 
            quantidade = int(input("Quantidade a remover: "))
            resultado = pdv.remover_item_carrinho(codigo, nome, quantidade)
            print(resultado)
        
        elif opcao == '3':
            cod_cliente = input("Código do cliente: ")
            nome_cliente = input("Nome do cliente: ")
            cod_vendedor = input("Código do vendedor: ")
            nome_vendedor = input("Nome do vendedor: ")
            
            mensagem, recibo, status = pdv.finalizar_compra(cod_cliente, nome_cliente, cod_vendedor, nome_vendedor)
            print(f"\n{mensagem}")
            if status == "finalizado":
                print("\n--- Recibo de Compra ---")
                print(f"Data: {recibo['data']}")
                print(f"Cliente: {recibo['cliente']}")
                print(f"Vendedor: {recibo['vendedor']}")
                for cod, item in recibo['itens']:
                    print(f"Produto: {item['nome']} | Quantidade: {item['quantidade']} | Unitário: R${item['valor']:.2f} | Subtotal: R${item['valor'] * item['quantidade']:.2f}")
                print(f"\nTotal: R${recibo['total']:.2f}")
                print(f"Imposto (25%): R${recibo['imposto']:.2f}")
                print(f"Comissão (5%): R${recibo['comissao']:.2f}")
                print(f"Lucro: R${recibo['lucro']:.2f}")
            break

        elif opcao == '4':
            break
        
        else:
            print("Opção inválida. Tente novamente.")

# Parte da Tela do Login
def menu_inicial():
    print("\n===== LOGIN PDV =====")
    print("1. Pagina do Vendedor")
    print("2. Pagina do Cliente")
    print("3. Sair")
    escolha = input("Escolha uma opção: ")
    return escolha
# Parte da Tela por Parte do Vendedor
def menu_vendedor_principal(pdv):
    while True:
        print("\n===== MENU VENDEDOR =====")
        print("1. Gerenciar Produtos")
        print("2. Gerenciar Vendedores")
        print("3. Gerenciar Clientes")
        print("4. Listar Cadastros")
        print("5. Relatório de Vendas")
        print("6. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            menu_produtos(pdv)
        elif escolha == '2':
            menu_vendedores(pdv)
        elif escolha == '3':
            menu_clientes(pdv)
        elif escolha == '4':
            print(pdv.listar_produtos())
            print(pdv.listar_vendedores())
            print(pdv.listar_clientes())
        elif escolha == '5':
            relatorio, status = pdv.exibir_relatorio()
            print(relatorio)
        elif escolha == '6':
            break
        else:
            print("Opção inválida. Tente novamente.")
# Tela por Parte do Cliente
def menu_cliente_principal(pdv):
    while True:
        print("\n===== MENU CLIENTE =====")
        print("1. Ver Produtos")
        print("2. Carrinho de Compras")
        print("3. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            print(pdv.listar_produtos())
        elif escolha == '2':
            menu_carrinho(pdv)
        elif escolha == '3':
            break
        else:
            print("Opção inválida. Tente novamente.")
# Controle
if __name__ == "__main__":
    pdv_system = PDVSystem()
    while True:
        escolha = menu_inicial()

        if escolha == '1':
            menu_vendedor_principal(pdv_system)
        elif escolha == '2':
            menu_cliente_principal(pdv_system)
        elif escolha == '3':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")