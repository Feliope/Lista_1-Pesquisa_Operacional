from mip import Model, maximize, CONTINUOUS, MAXIMIZE
import matplotlib.pyplot as plt
import numpy as np

# Criando o modelo
model = Model(sense=MAXIMIZE)

# Definindo as variáveis de decisão
x = model.add_var(var_type=CONTINUOUS)  # Camisas masculinas
y = model.add_var(var_type=CONTINUOUS)  # Blusas femininas

# Definindo a função objetivo (maximizar lucro total)
model.objective = maximize(8 * x + 12 * y)

# Adicionando as restrições de tempo dos departamentos
model += 20 * x + 60 * y <= 60000      # Restrição de corte
model += 70 * x + 60 * y <= 84000      # Restrição de costura
model += 12 * x + 4 * y <= 12000       # Restrição de embalagem

# Resolvendo o modelo
model.optimize()

# Extraindo os valores das variáveis
x_opt = x.x
y_opt = y.x
lucro_maximo = model.objective_value

print(f"Quantidade ótima de camisas: {x_opt}")
print(f"Quantidade ótima de blusas: {y_opt}")
print(f"Lucro máximo: ${lucro_maximo:.2f}")

# Plotando o gráfico da região viável e solução ótima

# Funções das restrições
def restricao_corte(x):
    return (60000 - 20 * x) / 60

def restricao_costura(x):
    return (84000 - 70 * x) / 60

def restricao_embalagem(x):
    return (12000 - 12 * x) / 4

# Intervalo de valores para o eixo x (camisas)
x_vals = np.linspace(0, 1000, 400)
y_vals1 = restricao_corte(x_vals)
y_vals2 = restricao_costura(x_vals)
y_vals3 = restricao_embalagem(x_vals)

# Plotando as restrições
plt.figure(figsize=(10, 8))
plt.plot(x_vals, y_vals1, label="20x + 60y = 60000 (Corte)", color="blue")
plt.plot(x_vals, y_vals2, label="70x + 60y = 84000 (Costura)", color="purple")
plt.plot(x_vals, y_vals3, label="12x + 4y = 12000 (Embalagem)", color="red")

# Região viável (restrições)
plt.fill_between(x_vals, np.minimum(np.minimum(y_vals1, y_vals2), y_vals3), 0, color='gray', alpha=0.2)

# Ponto ótimo
plt.plot(x_opt, y_opt, 'ro', label="Solução Ótima (x, y)")

# Configurações do gráfico
plt.xlim(0, 1000)
plt.ylim(0, 1000)
plt.xlabel("Quantidade de Camisas")
plt.ylabel("Quantidade de Blusas")
plt.title("Região Viável e Solução Ótima para Maximizar o Lucro")
plt.legend()
plt.grid(True)
plt.show()