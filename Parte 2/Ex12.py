from mip import Model, maximize, CONTINUOUS, MAXIMIZE
import matplotlib.pyplot as plt
import numpy as np

# Criando o modelo
model = Model(sense=MAXIMIZE)

# Definindo as variáveis de decisão
x = model.add_var(var_type=CONTINUOUS)  # Chapéus do tipo 1
y = model.add_var(var_type=CONTINUOUS) # Chapéus do tipo 2

# Definindo a função objetivo (maximizar lucro total)
model.objective = maximize(8 * x + 5 * y)

# Adicionando as restrições de produção e mercado
model += 2 * x + y <= 400      # Restrição de mão-de-obra
model += x <= 150              # Limite de mercado para chapéus tipo 1
model += y <= 200              # Limite de mercado para chapéus tipo 2

# Resolvendo o modelo
model.optimize()

# Extraindo os valores das variáveis
x_opt = x.x
y_opt = y.x
lucro_maximo = model.objective_value

print(f"Quantidade ótima de chapéus do tipo 1: {x_opt}")
print(f"Quantidade ótima de chapéus do tipo 2: {y_opt}")
print(f"Lucro máximo: ${lucro_maximo:.2f}")

# Plotando o gráfico da região viável e solução ótima

# Funções das restrições
def restricao_mao_obra(x):
    return 400 - 2 * x

def limite_tipo1(x):
    return 150

def limite_tipo2(x):
    return 200

# Intervalo de valores para o eixo x (tipo 1)
x_vals = np.linspace(0, 160, 400)
y_vals1 = restricao_mao_obra(x_vals)
y_vals2 = np.full_like(x_vals, 200)
y_vals3 = np.full_like(x_vals, 150)

# Plotando as restrições
plt.figure(figsize=(10, 8))
plt.plot(x_vals, y_vals1, label="2x + y = 400 (Mão-de-Obra)", color="blue")
plt.plot(x_vals, y_vals2, label="y = 200 (Limite Tipo 2)", color="purple", linestyle="--")
plt.axvline(150, color="red", linestyle="--", label="x = 150 (Limite Tipo 1)")

# Região viável (restrições)
plt.fill_between(x_vals, np.minimum(y_vals1, y_vals2), 0, where=(x_vals <= 150), color='gray', alpha=0.2)

# Ponto ótimo
plt.plot(x_opt, y_opt, 'ro', label="Solução Ótima (x, y)")

# Configurações do gráfico
plt.xlim(0, 160)
plt.ylim(0, 210)
plt.xlabel("Quantidade de Chapéus Tipo 1")
plt.ylabel("Quantidade de Chapéus Tipo 2")
plt.title("Região Viável e Solução Ótima para Maximizar o Lucro")
plt.legend()
plt.grid(True)
plt.show()