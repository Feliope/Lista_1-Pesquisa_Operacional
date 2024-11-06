# Importando as bibliotecas necessárias
from mip import Model, maximize, CONTINUOUS, MAXIMIZE
import matplotlib.pyplot as plt
import numpy as np

# Criando o modelo
model = Model(sense=MAXIMIZE)

# Definindo as variáveis de decisão
x = model.add_var(var_type=CONTINUOUS)  # Horas de estudo
y = model.add_var(var_type=CONTINUOUS)  # Horas de diversão

# Definindo a função objetivo (maximizar prazer total)
model.objective = maximize(1 * x + 2 * y)

# Adicionando as restrições de tempo e preferências
model += x + y <= 10     # Restrição de tempo total
model += x >= y          # Jack quer estudar pelo menos o mesmo tempo que se diverte
model += y <= 4          # Limite máximo de diversão

# Resolvendo o modelo
model.optimize()

# Extraindo os valores das variáveis
x_opt = x.x
y_opt = y.x
prazer_maximo = model.objective_value

print(f"Tempo ótimo de estudo: {x_opt} horas")
print(f"Tempo ótimo de diversão: {y_opt} horas")
print(f"Prazer máximo: {prazer_maximo} pontos")

# Plotando o gráfico da região viável e solução ótima

# Funções das restrições
def restricao_tempo_total(x):
    return 10 - x

def restricao_min_estudo(x):
    return x

def limite_diversao(x):
    return 4

# Intervalo de valores para o eixo x (Estudo)
x_vals = np.linspace(0, 10, 400)
y_vals1 = restricao_tempo_total(x_vals)
y_vals2 = restricao_min_estudo(x_vals)
y_vals3 = np.full_like(x_vals, 4)

# Plotando as restrições
plt.figure(figsize=(10, 8))
plt.plot(x_vals, y_vals1, label="x + y = 10 (Tempo Total)", color="blue")
plt.plot(x_vals, y_vals2, label="x = y (Estudo >= Diversão)", color="green")
plt.plot(x_vals, y_vals3, label="y = 4 (Limite de Diversão)", color="purple", linestyle="--")

# Região viável (restrições)
plt.fill_between(x_vals, np.minimum(np.minimum(y_vals1, y_vals2), y_vals3), color='gray', alpha=0.2)

# Ponto ótimo
plt.plot(x_opt, y_opt, 'ro', label="Solução Ótima (x, y)")

# Configurações do gráfico
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.xlabel("Horas de Estudo")
plt.ylabel("Horas de Diversão")
plt.title("Região Viável e Solução Ótima para Maximizar o Prazer de Jack")
plt.legend()
plt.grid(True)
plt.show()
