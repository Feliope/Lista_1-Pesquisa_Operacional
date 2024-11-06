from mip import Model, xsum, maximize, CONTINUOUS
import matplotlib.pyplot as plt
import numpy as np

# Criando o modelo
model = Model()

# Definindo as variáveis de decisão
x = model.add_var(var_type=CONTINUOUS)  # Caixas de Grano
y = model.add_var(var_type=CONTINUOUS)  # Caixas de Wheatie

# Definindo a função objetivo (maximizar lucro total)
model.objective = maximize(1 * x + 1.35 * y)

# Adicionando as restrições de espaço e demanda
model += 0.2 * x + 0.4 * y <= 60    
model += x <= 200                   
model += y <= 120                   
model += 0.2 * x <= 25.8            
model += 0.4 * y <= 34.2            

# Resolvendo o modelo
model.optimize()

# Extraindo os valores das variáveis
x_opt = x.x
y_opt = y.x
lucro_maximo = model.objective_value

print(f"Quantidade ótima de Grano: {x_opt}")
print(f"Quantidade ótima de Wheatie: {y_opt}")
print(f"Lucro máximo: ${lucro_maximo:.2f}")

# Plotando o gráfico da região viável e solução ótima

# Funções das restrições
def restricao_espaco_total(x):
    return (60 - 0.2 * x) / 0.4

def restricao_grano(x):
    return (25.8 - 0.2 * x) / 0.4

def restricao_wheatie(x):
    return 120  # y não pode ultrapassar 120 caixas

# Intervalo de valores para o eixo x (Grano)
x_vals = np.linspace(0, 220, 400)
y_vals1 = restricao_espaco_total(x_vals)
y_vals2 = np.full_like(x_vals, 120)
y_vals3 = restricao_grano(x_vals)
y_vals4 = np.full_like(x_vals, 200)  # Limite de demanda para x

# Plotando as restrições
plt.figure(figsize=(10, 8))
plt.plot(x_vals, y_vals1, label="0.2x + 0.4y = 60 (Espaço Total)", color="blue")
plt.plot(x_vals, y_vals2, label="y = 120 (Demanda Max Wheatie)", color="purple", linestyle="--")
plt.plot(x_vals, y_vals3, label="0.2x = 25.8 (Espaço Max Grano)", color="green", linestyle="--")
plt.plot(x_vals, y_vals4, label="x = 200 (Demanda Max Grano)", color="red", linestyle="--")

# Região viável (restrições)
plt.fill_between(x_vals, np.minimum(np.minimum(y_vals1, y_vals2), y_vals3), color='gray', alpha=0.2)

# Ponto ótimo
plt.plot(x_opt, y_opt, 'ro', label="Solução Ótima (x, y)")

# Configurações do gráfico
plt.xlim(0, 220)
plt.ylim(0, 130)
plt.xlabel("Quantidade de Grano")
plt.ylabel("Quantidade de Wheatie")
plt.title("Região Viável e Solução Ótima")
plt.legend()
plt.grid(True)
plt.show()
