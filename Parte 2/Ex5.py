from mip import Model, xsum, maximize, CONTINUOUS
import numpy as np
import matplotlib.pyplot as plt

# Inicializando o modelo
m = Model(sense=maximize)

# Definindo as variáveis de decisão
x = m.add_var(name="A", var_type=CONTINUOUS)
y = m.add_var(name="B", var_type=CONTINUOUS)

# Adicionando as restrições
m += x >= 4 * y, "Restrição de demanda mínima para A"
m += x <= 100, "Limite de vendas para A"
m += x + 2 * y <= 120, "Restrição de disponibilidade de matéria-prima"

# Definindo a função objetivo
m.objective = maximize(20 * x + 50 * y)

# Resolvendo o modelo
m.optimize()

# Exibindo o resultado
print(f"Quantidade ótima de A (x): {x.x}")
print(f"Quantidade ótima de B (y): {y.x}")
print(f"Lucro máximo: ${m.objective_value}")


# Criação da faixa de valores para x
x_vals = np.linspace(0, 120, 500)

# Cálculo dos valores de y para cada restrição
y1 = x_vals / 4 
y2 = (120 - x_vals) / 2
y3 = np.full_like(x_vals, 100)

# Limite para y não negativo
y1 = np.clip(y1, 0, None)
y2 = np.clip(y2, 0, None)

# Plot das restrições
plt.figure(figsize=(10, 8))
plt.plot(x_vals, y1, label=r'$x \geq 4y$ (ou $y \leq x/4$)', color='blue')
plt.plot(x_vals, y2, label=r'$x + 2y \leq 120$', color='green')
plt.axvline(100, label=r'$x \leq 100$', color='red', linestyle='--')

# Sombreando a região factível
plt.fill_between(x_vals, 0, np.minimum(y1, y2), where=(x_vals <= 100), color='gray', alpha=0.3)

#Ponto de solução ótima
plt.plot(x.x, y.x, 'ro', label="Solução Ótima")

# Definindo os rótulos e limites do gráfico
plt.xlim(0, 120)
plt.ylim(0, 40)
plt.xlabel("Quantidade de A (x)")
plt.ylabel("Quantidade de B (y)")
plt.title("Solução Gráfica do Problema de Otimização")
plt.legend()
plt.grid(True)
plt.show()

