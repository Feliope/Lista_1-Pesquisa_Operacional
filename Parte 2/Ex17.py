from mip import Model, maximize, CONTINUOUS, MAXIMIZE
import matplotlib.pyplot as plt
import numpy as np

# Criando o modelo
model = Model(sense=MAXIMIZE)

# Definindo as variáveis de decisão
x = model.add_var(var_type=CONTINUOUS)  # Mesas
y = model.add_var(var_type=CONTINUOUS)  # Cadeiras

# Definindo a função objetivo (maximizar lucro total)
model.objective = maximize(100 * x + 50 * y)

# Adicionando as restrições de capacidade dos departamentos
model += x <= 80          # Restrição de serraria para mesas
model += y <= 200         # Restrição de serraria para cadeiras
model += x <= 60          # Restrição de montagem para mesas
model += y <= 120         # Restrição de montagem para cadeiras
model += (y / 150) + (x / 110) <= 1  # Restrição de capacidade de pintura

# Resolvendo o modelo
model.optimize()

# Extraindo os valores das variáveis
x_opt = x.x
y_opt = y.x
lucro_maximo = model.objective_value

print(f"Quantidade ótima de mesas: {x_opt}")
print(f"Quantidade ótima de cadeiras: {y_opt}")
print(f"Lucro máximo: ${lucro_maximo:.2f}")

# Plotando o gráfico da região viável e solução ótima

# Funções das restrições
def restricao_pintura(y):
    return 110 * (1 - (y / 150))

# Intervalo de valores para o eixo x (mesas) e y (cadeiras)
x_vals = np.linspace(0, 80, 200)
y_vals = np.linspace(0, 200, 200)
y_vals1 = np.minimum(200, 120)  # serraria e montagem para cadeiras
x_vals1 = np.minimum(80, 60)    # serraria e montagem para mesas
y_vals_pintura = restricao_pintura(x_vals)

# Plotando as restrições
plt.figure(figsize=(10, 8))
plt.plot(x_vals, y_vals_pintura, label="Pintura: (y/150) + (x/110) = 1", color="red")
plt.axhline(120, color="blue", linestyle="--", label="Montagem (cadeiras) y <= 120")
plt.axhline(200, color="green", linestyle="--", label="Serraria (cadeiras) y <= 200")
plt.axvline(60, color="purple", linestyle="--", label="Montagem (mesas) x <= 60")
plt.axvline(80, color="orange", linestyle="--", label="Serraria (mesas) x <= 80")

# Região viável (restrições)
plt.fill_between(x_vals, 0, np.minimum(np.minimum(y_vals_pintura, 120), 200), color='gray', alpha=0.2)

# Ponto ótimo
plt.plot(x_opt, y_opt, 'ro', label="Solução Ótima (x, y)")

# Configurações do gráfico
plt.xlim(0, 80)
plt.ylim(0, 200)
plt.xlabel("Quantidade de Mesas")
plt.ylabel("Quantidade de Cadeiras")
plt.title("Região Viável e Solução Ótima para Maximizar o Lucro")
plt.legend()
plt.grid(True)
plt.show()
