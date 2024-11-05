from mip import Model, xsum, MAXIMIZE

# Parâmetros
custo_petroleo = [19, 24, 20, 27]  # Custo por barril de cada tipo de petróleo
max_disponibilidade = [3500, 2200, 4200, 1800]  # Máxima disponibilidade de cada petróleo
preco_gasolina = [35, 28, 22]  # Preço de venda por barril das gasolinas superazul, azul e amarela

# Inicializar o modelo
model = Model(sense=MAXIMIZE)

# Variáveis de decisão: quantidade de cada petróleo para cada tipo de gasolina
x = [[model.add_var(name=f'x_{i}_{j}') for j in range(3)] for i in range(4)]

# Função objetivo: maximizar lucro
model.objective = xsum(preco_gasolina[j] * xsum(x[i][j] for i in range(4)) -
                       custo_petroleo[i] * x[i][j] for i in range(4) for j in range(3))

# Restrições de disponibilidade de petróleo
for i in range(4):
    model += xsum(x[i][j] for j in range(3)) <= max_disponibilidade[i], f"Disponibilidade_Petroleo_{i+1}"

# Restrições de composição para cada gasolina
# Superazul
model += x[0][0] <= 0.3 * xsum(x[i][0] for i in range(4)), "Restricao_Superazul_Petroleo1"
model += x[1][0] >= 0.4 * xsum(x[i][0] for i in range(4)), "Restricao_Superazul_Petroleo2"
model += x[2][0] <= 0.5 * xsum(x[i][0] for i in range(4)), "Restricao_Superazul_Petroleo3"

# Azul
model += x[0][1] <= 0.3 * xsum(x[i][1] for i in range(4)), "Restricao_Azul_Petroleo1"
model += x[1][1] >= 0.1 * xsum(x[i][1] for i in range(4)), "Restricao_Azul_Petroleo2"

# Amarela
model += x[0][2] <= 0.7 * xsum(x[i][2] for i in range(4)), "Restricao_Amarela_Petroleo1"

# Resolver o modelo
model.optimize()

# Exibir resultados
if model.num_solutions:
    print("==== Solução Ótima Encontrada ====")
    for j, gasolina in enumerate(["Superazul", "Azul", "Amarela"]):
        print(f"\nGasolina {gasolina}:")
        for i, petroleo in enumerate(["Petróleo 1", "Petróleo 2", "Petróleo 3", "Petróleo 4"]):
            quantidade = x[i][j].x
            print(f"  {petroleo}: {quantidade:.2f} barris")
    
    print("\n==== Lucro Máximo ====")
    print(f"Lucro Máximo: R$ {model.objective_value:.2f}")
else:
    print("Nenhuma solução encontrada.")
