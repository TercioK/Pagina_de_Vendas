#Página: import datetime.py
#Página de vendas (main.py)
#Arquivo principal (main.py)
#Arquivo da biblioteca (pdv_library.py)    
#Biblioteca do sistema PDV (pdv_library.py)
from listacontrole import criar_logs, listatxt_produtos, lista_atualizar_produtos, lista_deletar_produtos
import datetime
# Ao iniciar o programa, ele crie logo um arquivo
listatxt_produtos()
class PDVSystem:
    """
    Sistema de Ponto de Vendas (PDV) para gerenciar produtos,
    vendedores, clientes e vendas.
    """
    def __init__(self):
        self.produtos = {}
        self.vendedores = {}
        self.clientes = {}
        self.carrinho = {}
        self.vendas = []
        self.imposto = 0.25
        self.comissao_vendedor = 0.05

    def _formatar_cadastro(self, tipo_cadastro, dados):
        output = f"\n--- Lista de {tipo_cadastro} ---\n"
        if not dados:
            return f"Nenhum {tipo_cadastro.lower()} cadastrado."
        
        for codigo, info in dados.items():
            if tipo_cadastro == "Produtos":
                output += f"Código: {codigo} | Nome: {info['nome']} | Valor: R${info['valor']:.2f} | Estoque: {info['estoque']}\n"
            else:
                output += f"Código: {codigo} | Nome: {info['nome']}\n"
        return output
    # Controle entre Cadastrar e Remover
    def cadastrar_produto(self, codigo, nome, valor, estoque):
        self.produtos[codigo] = {'nome': nome, 'valor': valor, 'estoque': estoque}
        # Vai chamar a funçao que vai criar ou atualizar
        lista_atualizar_produtos(codigo, nome, valor, estoque)
    def remover_produto(self, codigo):
        if codigo in self.produtos:
            del self.produtos[codigo]
            # Aqui vai chamar a funçao que vai deletar, se caso estiver no txt
            lista_deletar_produtos(codigo)
            return True
        return False
    
    def listar_produtos(self):
        return self._formatar_cadastro("Produtos", self.produtos)

    def cadastrar_vendedor(self, codigo, nome):
        self.vendedores[codigo] = {'nome': nome, 'vendas_totais': 0, 'comissao_total': 0}

    def remover_vendedor(self, codigo):
        if codigo in self.vendedores:
            del self.vendedores[codigo]
            return True
        return False

    def listar_vendedores(self):
        return self._formatar_cadastro("Vendedores", self.vendedores)

    def cadastrar_cliente(self, codigo, nome):
        self.clientes[codigo] = {'nome': nome, 'compras_totais': 0}
    
    def remover_cliente(self, codigo):
        if codigo in self.clientes:
            del self.clientes[codigo]
            return True
        return False

    def listar_clientes(self):
        return self._formatar_cadastro("Clientes", self.clientes)

    def adicionar_item_carrinho(self, codigo_produto, nome_produto, quantidade):
        if codigo_produto not in self.produtos:
            return f"Erro: Produto com código {codigo_produto} não encontrado."
        
        produto = self.produtos[codigo_produto]
        if quantidade > produto['estoque']:
            return f"Erro: Apenas {produto['estoque']} unidades do produto '{produto['nome']}' em estoque."
        
        if codigo_produto in self.carrinho:
            self.carrinho[codigo_produto]['quantidade'] += quantidade
        else:
            self.carrinho[codigo_produto] = {'nome': produto['nome'], 'quantidade': quantidade, 'valor': produto['valor']}
        
        return f"{quantidade} unidades do produto '{produto['nome']}' adicionadas ao carrinho."

    def remover_item_carrinho(self, codigo_produto, nome_produto, quantidade):
        if codigo_produto not in self.carrinho:
            return "Erro: Produto não está no carrinho."

        item_carrinho = self.carrinho[codigo_produto]

        if quantidade >= item_carrinho['quantidade']:
            del self.carrinho[codigo_produto]
            return f"Produto '{nome_produto}' removido completamente do carrinho."
        else:
            item_carrinho['quantidade'] -= quantidade
            return f"{quantidade} unidades do produto '{nome_produto}' removidas do carrinho. Restam {item_carrinho['quantidade']}."
    
    def finalizar_compra(self, cod_cliente, nome_cliente, cod_vendedor, nome_vendedor):
        if not self.carrinho:
            return "Erro: O carrinho está vazio.", {}, "erro"

        if cod_cliente not in self.clientes:
            self.cadastrar_cliente(cod_cliente, nome_cliente)
        
        if cod_vendedor not in self.vendedores:
            self.cadastrar_vendedor(cod_vendedor, nome_vendedor)

        total = 0
        itens_venda = []
        for codigo, item in self.carrinho.items():
            subtotal = item['quantidade'] * item['valor']
            total += subtotal
            self.produtos[codigo]['estoque'] -= item['quantidade']
            itens_venda.append((codigo, item))

        imposto_total = total * self.imposto
        comissao = total * self.comissao_vendedor
        lucro = total - imposto_total - comissao

        recibo = {
            'data': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'cliente': nome_cliente,
            'vendedor': nome_vendedor,
            'itens': itens_venda,
            'total': total,
            'imposto': imposto_total,
            'comissao': comissao,
            'lucro': lucro
        }
        criar_logs("finalizou", nome_cliente)
        self.vendas.append(recibo)
        self.carrinho.clear()

        return "Compra finalizada com sucesso!", recibo, "finalizado"

    def exibir_relatorio(self):
        if not self.vendas:
            return "Nenhuma venda registrada ainda.", "erro"
        
        total_vendas = sum(venda['total'] for venda in self.vendas)
        total_impostos = sum(venda['imposto'] for venda in self.vendas)
        total_comissoes = sum(venda['comissao'] for venda in self.vendas)
        total_lucro = sum(venda['lucro'] for venda in self.vendas)
        
        relatorio = "\n--- Relatório de Vendas ---\n"
        relatorio += f"Total de Vendas: R${total_vendas:.2f}\n"
        relatorio += f"Total de Impostos: R${total_impostos:.2f}\n"
        relatorio += f"Total de Comissões: R${total_comissoes:.2f}\n"
        relatorio += f"Lucro Total: R${total_lucro:.2f}\n"
        relatorio += "---------------------------\n"
        
        return relatorio, "sucesso"