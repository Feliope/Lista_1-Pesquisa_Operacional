from mip import Model, maximize, CONTINUOUS, MAXIMIZE
import matplotlib.pyplot as plt
import numpy as np

# Criando o modelo
model = Model(sense=MAXIMIZE)

# Definindo as variáveis de decisão
x = model.add_var(var_type=CONTINUOUS)  # Comerciais de rádio (inteiro)
y = model.add_var(var_type=CONTINUOUS)  # Anúncios de TV (inteiro)

# Definindo a função objetivo (maximizar alcance total)
model.objective = maximize(2000 * x + 3000 * y + 4500)

# Adicionando as restrições de orçamento e alocação de verba
model += 300 * x + 2000 * y <= 20000    # Orçamento total
model += 300 * x <= 16000               # Limite máximo para rádio
model += 2000 * y <= 16000              # Limite máximo para TV

# Restrição de pelo menos um comercial em cada mídia
model += x >= 1
model += y >= 1

# Resolvendo o modelo
model.optimize()

# Extraindo os valores das variáveis
x_opt = x.x
y_opt = y.x
alcance_maximo = model.objective_value

print(f"Quantidade ótima de comerciais de rádio: {x_opt}")
print(f"Quantidade ótima de anúncios de TV: {y_opt}")
print(f"Alcance máximo: {alcance_maximo:.0f} pessoas")

# Plotando o gráfico da região viável e solução ótima

# Funções das restrições
def restricao_orcamento(x):
    return (20000 - 300 * x) / 2000

def limite_radio(x):
    return 16000 / 2000

def limite_tv(x):
    return 16000 / 300

# Intervalo de valores para o eixo x (rádio)
x_vals = np.linspace(1, 70, 400)
y_vals1 = restricao_orcamento(x_vals)
y_vals2 = np.full_like(x_vals, 8)
y_vals3 = np.full_like(x_vals, 53.33)

# Plotando as restrições
plt.figure(figsize=(10, 8))
plt.plot(x_vals, y_vals1, label="300x + 2000y = 20000 (Orçamento Total)", color="blue")
plt.plot(x_vals, y_vals2, label="y = 8 (Limite TV)", color="purple", linestyle="--")
plt.axvline(53.33, color="red", linestyle="--", label="x = 53.33 (Limite Rádio)")

# Região viável (restrições)
plt.fill_between(x_vals, np.minimum(y_vals1, y_vals2), where=(x_vals <= 53.33), color='gray', alpha=0.2)

# Ponto ótimo
plt.plot(x_opt, y_opt, 'ro', label="Solução Ótima (x, y)")

# Configurações do gráfico
plt.xlim(0, 70)
plt.ylim(0, 10)
plt.xlabel("Quantidade de Comerciais de Rádio")
plt.ylabel("Quantidade de Anúncios de TV")
plt.title("Região Viável e Solução Ótima para Maximizar o Alcance")
plt.legend()
plt.grid(True)
plt.show()