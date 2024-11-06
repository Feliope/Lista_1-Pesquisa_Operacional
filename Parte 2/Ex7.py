from mip import Model, CONTINUOUS, MAXIMIZE, xsum
import matplotlib.pyplot as plt
import numpy as np

# Parâmetros do problema
capital_total = 5000
taxa_retorno_a = 0.05
taxa_retorno_b = 0.08
min_percentual_a = 0.25
max_percentual_b = 0.5

# Modelo de otimização
model = Model(sense=MAXIMIZE)

# Variáveis de decisão
x = model.add_var(name="x", var_type=CONTINUOUS)  # investimento em A
y = model.add_var(name="y", var_type=CONTINUOUS)  # investimento em B

# Função objetivo: maximizar o retorno total
model.objective = xsum([taxa_retorno_a * x, taxa_retorno_b * y])

# Restrições
model += x + y == capital_total  # restrição do total investido
model += x >= min_percentual_a * capital_total  # mínimo de 25% no investimento A
model += y <= max_percentual_b * capital_total  # máximo de 50% no investimento B
model += x >= y / 2  # investimento em A no mínimo metade de B

# Resolver o problema
model.optimize()

# Valores ótimos para x, y e retorno total
x_val = x.x
y_val = y.x
retorno_total = model.objective_value

# Plotagem do gráfico com a região viável e a solução ótima
fig, ax = plt.subplots(figsize=(8, 6))

# Criar um grid para avaliar as restrições
x_vals = np.linspace(0, capital_total, 200)
y_total = capital_total - x_vals
y_min_a = np.maximum(0, (x_vals / 2))  # x >= y / 2 --> y <= 2 * x
y_max_b = np.full_like(x_vals, max_percentual_b * capital_total)

# Adicionar áreas das restrições
ax.plot(x_vals, y_total, 'c-', label="x + y <= 5000")
ax.plot(x_vals, y_min_a, 'g-', label="x >= y / 2")
ax.plot(x_vals, y_max_b, 'r-', label="y <= 2500")
ax.axvline(x=min_percentual_a * capital_total, color="purple", linestyle="--", label="x >= 1250")

# Plotar a solução ótima
ax.plot(x_val, y_val, 'ro', markersize=8, label=f'Solução ótima: x={x_val:.2f}, y={y_val:.2f}')

# Configurações do gráfico
ax.set_xlim(0, capital_total)
ax.set_ylim(0, capital_total)
ax.set_xlabel("Investimento em A (x)")
ax.set_ylabel("Investimento em B (y)")
ax.set_title("Região Viável e Solução Ótima para Alocação de Investimento")
ax.legend()
plt.grid(True)

# Exibir o gráfico
plt.show()

print(f"Solução ótima: Investimento em A = {x_val:.2f}, Investimento em B = {y_val:.2f}, Retorno Total = {retorno_total:.2f}")
