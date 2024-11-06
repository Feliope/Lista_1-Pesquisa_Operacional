from mip import Model, xsum, MAXIMIZE, CONTINUOUS
import numpy as np
import matplotlib.pyplot as plt

# Criando o modelo
m = Model(sense=MAXIMIZE)

# Variáveis de decisão: quantidade de chapas (x) e barras (y)
x = m.add_var(name="x", var_type=CONTINUOUS)
y = m.add_var(name="y", var_type=CONTINUOUS)

# Função objetivo: maximizar o lucro Z = 40x + 35y
m.objective = 40 * x + 35 * y

# Restrições:
# Capacidade de produção: (x / 800) + (y / 600) <= 1
m += (x / 800) + (y / 600) <= 1

# Demanda máxima
m += x <= 550  # Restrição de chapas
m += y <= 580  # Restrição de barras

# Restrições de não-negatividade
m += x >= 0
m += y >= 0

# Resolver o modelo
m.optimize()

# Obtendo os valores ótimos de x e y
optimal_x = x.x
optimal_y = y.x
optimal_profit = m.objective_value

print(f"Produção ótima de chapas: {optimal_x}")
print(f"Produção ótima de barras: {optimal_y}")
print(f"Lucro máximo: {optimal_profit}")


# Definindo os limites das variáveis
x_max, y_max = 800, 600

# Valores das restrições como funções de x
def capacity_constraint(x):
    return 600 - (3/4) * x

# Valores de x para definir as restrições no gráfico
x_vals = np.linspace(0, x_max, 400)

y_capacidade_total = (y_max - (y_max / x_max) * x_vals)
y_demanda_barras = np.full_like(x_vals, 580)  # Demanda Barra
y_capacidade_barras = np.full_like(x_vals, y_max)  # Capacidade Barra

# Plotando as linhas de restrição
plt.figure(figsize=(10, 8))

# Restrição de capacidade
plt.plot(x_vals, capacity_constraint(x_vals), label=r"$\frac{x}{800} + \frac{y}{600} \leq 1$", color='blue')
# Restrição de demanda para chapas
plt.axvline(x=550, label=r"$x \leq 550$", color='green', linestyle="--")
# Restrição de demanda para barras
plt.axhline(y=580, label=r"$y \leq 580$", color='red', linestyle="--")

# Delimitando a região viável
plt.fill_between(x_vals, 0, np.minimum(y_capacidade_total, y_demanda_barras),
                 where=(x_vals <= 550), color='grey', alpha=0.5)

# Marcando o ponto de interseção
plt.plot(x.x, y.x, 'ro', label="Solução Ótima")

# Adicionando rótulos e título
plt.xlim(0, 800)
plt.ylim(0, 600)
plt.xlabel("Quantidade de Chapas (x)")
plt.ylabel("Quantidade de Barras (y)")
plt.title("Região Viável e Função Objetivo")

# Mostrar legenda e gráfico
plt.legend()
plt.grid(True)
plt.show()
