from mip import Model, minimize, CONTINUOUS, MINIMIZE
import matplotlib.pyplot as plt
import numpy as np

# Criando o modelo
model = Model(sense=MINIMIZE)
# Definindo as variáveis de decisão
x = model.add_var(var_type=CONTINUOUS)  # Unidades de HiFi-1
y = model.add_var(var_type=CONTINUOUS)  # Unidades de HiFi-2

# Definindo a função objetivo (minimizar o tempo ocioso total)
model.objective = minimize((432 - (6 * x + 4 * y)) +
                           (412.8 - (5 * x + 5 * y)) +
                           (422.4 - (4 * x + 6 * y)))

# Adicionando as restrições de tempo das estações
model += 6 * x + 4 * y <= 432       # Restrição da estação 1
model += 5 * x + 5 * y <= 412.8     # Restrição da estação 2
model += 4 * x + 6 * y <= 422.4     # Restrição da estação 3

# Resolvendo o modelo
model.optimize()

# Extraindo os valores das variáveis
x_opt = x.x
y_opt = y.x
tempo_ocioso_min = model.objective_value

print(f"Quantidade ótima de HiFi-1: {x_opt}")
print(f"Quantidade ótima de HiFi-2: {y_opt}")
print(f"Tempo ocioso mínimo total: {tempo_ocioso_min:.2f} minutos")

# Plotando o gráfico da região viável e solução ótima

# Funções das restrições
def restricao1(y):
    return (432 - 4 * y) / 6

def restricao2(y):
    return (412.8 - 5 * y) / 5

def restricao3(y):
    return (422.4 - 6 * y) / 4

# Intervalo de valores para o eixo x (HiFi-1) e y (HiFi-2)
y_vals = np.linspace(0, max(y_opt + 10, 100), 200)
x_vals1 = restricao1(y_vals)
x_vals2 = restricao2(y_vals)
x_vals3 = restricao3(y_vals)

# Plotando as restrições
plt.figure(figsize=(10, 8))
plt.plot(x_vals1, y_vals, label="Estação 1: 6x + 4y <= 432", color="red")
plt.plot(x_vals2, y_vals, label="Estação 2: 5x + 5y <= 412.8", color="blue")
plt.plot(x_vals3, y_vals, label="Estação 3: 4x + 6y <= 422.4", color="green")

# Região viável (restrições)
plt.fill_betweenx(y_vals, 0, np.minimum(np.minimum(x_vals1, x_vals2), x_vals3), color='gray', alpha=0.2)

# Ponto ótimo
plt.plot(x_opt, y_opt, 'ro', label="Solução Ótima (x, y)")

# Configurações do gráfico
plt.xlim(0, max(x_opt + 10, 100))
plt.ylim(0, max(y_opt + 10, 100))
plt.xlabel("Quantidade de HiFi-1")
plt.ylabel("Quantidade de HiFi-2")
plt.title("Região Viável e Solução Ótima para Minimizar o Tempo Ocioso")
plt.legend()
plt.grid(True)
plt.show()
