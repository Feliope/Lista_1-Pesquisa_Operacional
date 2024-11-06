from mip import Model, xsum, maximize, CONTINUOUS

# Dados do problema
areas_disponiveis = [1500, 1700, 900, 600]  # área disponível em cada cidade
producao_esperada = [
    [17, 14, 10, 9],   # Cidade 1
    [15, 16, 12, 13],  # Cidade 2
    [13, 12, 14, 11],  # Cidade 3
    [10, 11, 8, 12]    # Cidade 4
]
renda_anual = [
    [9, 12, 20, 18],   # Cidade 1
    [10, 13, 24, 20],  # Cidade 2
    [11, 13, 28, 20],  # Cidade 3
    [12, 10, 18, 17]   # Cidade 4
]
producao_minima = [225000, 9000, 4800, 3500]  # produção mínima em m³

# Número de cidades e tipos de árvores
num_cidades = 4
num_arvores = 4

# Modelo de otimização
m = Model(sense=maximize)

# Variáveis de decisão: hectares plantados
x = [[m.add_var(var_type=CONTINUOUS) for j in range(num_arvores)] for i in range(num_cidades)]

# Função objetivo: maximizar a renda anual total
m.objective = xsum(renda_anual[i][j] * x[i][j] for i in range(num_cidades) for j in range(num_arvores))

# Restrições de área disponível para cada cidade
for i in range(num_cidades):
    m += xsum(x[i][j] for j in range(num_arvores)) <= areas_disponiveis[i]

# Restrições de produção mínima para cada tipo de árvore
for j in range(num_arvores):
    m += xsum(producao_esperada[i][j] * x[i][j] for i in range(num_cidades)) >= producao_minima[j]

# Resolver o modelo
status = m.optimize()

# Verificar se a solução é viável
if status == "OPTIMAL" or status == "FEASIBLE":
    print("Quantidade de hectares plantados em cada cidade para cada tipo de árvore:")
    for i in range(num_cidades):
        for j in range(num_arvores):
            # Verificar se a variável possui um valor antes de acessar
            if x[i][j].x is not None:
                print(f"Cidade {i+1}, Árvore {j+1}: {x[i][j].x:.2f} hectares")
            else:
                print(f"Cidade {i+1}, Árvore {j+1}: 0.00 hectares (não foi plantado)")
    print(f"Renda Anual Total: {m.objective_value:.2f}")

else:
    print("O modelo é inviável ou não pôde encontrar uma solução.")
