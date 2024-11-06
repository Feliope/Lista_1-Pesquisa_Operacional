# Importando as bibliotecas necessárias
from mip import Model, maximize, CONTINUOUS, MAXIMIZE
import matplotlib.pyplot as plt
import numpy as np

# Criando o modelo
model = Model(sense=MAXIMIZE)

# Definindo as variáveis de decisão
x = model.add_var(var_type=CONTINUOUS)  # Produto A
y = model.add_var(var_type=CONTINUOUS)  # Produto B

# Definindo a função objetivo (maximizar lucro total)
model.objective = maximize(8 * x + 10 * y)

# Adicionando as restrições de matérias-primas
model += 0.5 * x + 0.5 * y <= 150  # Matéria-prima I
model += 0.6 * x + 0.4 * y <= 145  # Matéria-prima II

# Adicionando as restrições de demanda
model += x >= 30
model += x <= 150
model += y >= 40
model += y <= 200

# Resolvendo o modelo
model.optimize()

# Extraindo os valores das variáveis
x_opt = x.x
y_opt = y.x
lucro_maximo = model.objective_value

print(f"Quantidade ótima de A: {x_opt}")
print(f"Quantidade ótima de B: {y_opt}")
print(f"Lucro máximo: ${lucro_maximo}")


# Funções das restrições
def restricao_materia_prima1(x):
    return (150 - 0.5 * x) / 0.5

def restricao_materia_prima2(x):
    return (145 - 0.6 * x) / 0.4

# Intervalo de valores para o eixo x (Produto A)
x_vals = np.linspace(0, 200, 400)
y_vals1 = restricao_materia_prima1(x_vals)
y_vals2 = restricao_materia_prima2(x_vals)

# Plotando as restrições
plt.figure(figsize=(10, 8))
plt.plot(x_vals, y_vals1, label="0.5x + 0.5y = 150 (Matéria-prima I)", color="blue")
plt.plot(x_vals, y_vals2, label="0.6x + 0.4y = 145 (Matéria-prima II)", color="green")

# Limitações de demanda
plt.axvline(x=30, label="x = 30 (Demanda min de A)", color="red", linestyle="--")
plt.axvline(x=150, label="x = 150 (Demanda max de A)", color="red", linestyle="--")
plt.axhline(y=40, label="y = 40 (Demanda min de B)", color="purple", linestyle="--")
plt.axhline(y=200, label="y = 200 (Demanda max de B)", color="purple", linestyle="--")

# Região viável (restrições)
plt.fill_between(x_vals, np.minimum(y_vals1, y_vals2), 200, where=(y_vals1 >= 0) & (y_vals2 >= 0), color='gray', alpha=0.2)

# Ponto ótimo
plt.plot(x_opt, y_opt, 'ro', label="Solução Ótima (x, y)")

# Configurações do gráfico
plt.xlim(0, 200)
plt.ylim(0, 300)
plt.xlabel("Quantidade de A")
plt.ylabel("Quantidade de B")
plt.title("Região Viável e Solução Ótima")
plt.legend()
plt.grid(True)
plt.show()
