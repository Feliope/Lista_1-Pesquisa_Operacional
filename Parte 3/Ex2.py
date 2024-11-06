from mip import Model, xsum, maximize, BINARY

# Define o modelo
m = Model(sense=maximize)

# Variáveis de decisão (1 se a caixa é incluída, 0 se não é)
x1 = m.add_var(var_type=BINARY, name="Alimento")
x2 = m.add_var(var_type=BINARY, name="Água")
x3 = m.add_var(var_type=BINARY, name="Munição")
x4 = m.add_var(var_type=BINARY, name="Remédios")

# Função objetivo (maximizar importância)
m.objective = xsum([1*x1, 2*x2, 4*x3, 4*x4])

# Restrições
m += x1 + x2 + x3 + x4 <= 7  # Limite de peso do helicóptero
m += x1 >= 6                 # Mínimo necessário de alimentos
m += x2 >= 4                 # Mínimo necessário de água
m += x3 >= 2                 # Mínimo necessário de munição
m += x4 >= 2                 # Mínimo necessário de remédios

# Resolver o modelo
m.optimize()

# Exibir resultados
print("Quantidade de cada item a ser transportado no helicóptero:")
for v in m.vars:
    print(f"{v.name}: {v.x}")

# Gráfico de barras dos itens transportados
import matplotlib.pyplot as plt

# Dados para o gráfico
labels = ['Alimento', 'Água', 'Munição', 'Remédios']
quantidades = [x1.x, x2.x, x3.x, x4.x]

plt.bar(labels, quantidades, color=['green', 'blue', 'red', 'purple'])
plt.xlabel("Itens de Socorro")
plt.ylabel("Quantidade")
plt.title("Quantidade de Itens a Serem Transportados")
plt.show()
