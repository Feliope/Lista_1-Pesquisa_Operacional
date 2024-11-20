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

x = np.linspace(0, 250, 250)

restricao1 = (60 - 0.2 * x) / 0.4
plt.plot(x, restricao1, label="Limite de espaço disponível")

restricao2 = 200
plt.axvline(restricao2, color='purple', linestyle='--', label="Limite de demanda Grano")

restricao3 = 120
plt.axhline(restricao3, color='orange', linestyle='--', label="Limite de demanda Wheatie")

plt.xlim(0, 250)
plt.ylim(0, 250)

plt.xlabel("Grano")
plt.ylabel("Wheatie")
plt.plot(x_opt, y_opt, 'ro', label="Max")
plt.fill_between(x, np.minimum(restricao1, restricao3), where=(x <= restricao2), color='gray', alpha=0.5)

plt.grid()
plt.legend()
plt.show()