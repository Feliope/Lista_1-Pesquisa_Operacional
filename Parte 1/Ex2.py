from mip import Model, xsum,  maximize

# Parâmetros
custo_petroleo = [19, 24, 20, 27]  # Custo por barril de cada tipo de petróleo
max_disponibilidade = [3500, 2200, 4200, 1800]  # Máxima disponibilidade de cada petróleo
preco_gasolina = [35, 28, 22]  # Preço de venda por barril das gasolinas superazul, azul e amarela

model = Model()

x = [[model.add_var(name=f"x_{i}_{j}", lb=0) for j in range(3)] for i in range(4)]

receita = xsum(x[i][j] * preco_gasolina[j] for i in range(4) for j in range(3))
custo = xsum(x[i][j] * custo_petroleo[i] for i in range(4) for j in range(3))

model.objective = maximize(receita - custo)

for i in range(4):
    model += xsum(x[i][j] for j in range(3)) <= max_disponibilidade[i]

# Super Azul
total_super_azul = xsum(x[i][0] for i in range(4))

model += x[0][0] <= 0.3 * total_super_azul
model += x[1][0] >= 0.4 * total_super_azul
model += x[2][0] <= 0.5 * total_super_azul

# Azul
total_azul = xsum(x[i][1] for i in range(4))

model += x[0][1] <= 0.3 * total_azul
model += x[1][1] >= 0.1 * total_azul

# Amarelo
total_amarelo = xsum(x[i][2] for i in range(4))

model += x[0][2] <= 0.7 * xsum(x[i][2] for i in range(4))

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
