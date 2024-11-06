from mip import Model, maximize, CONTINUOUS
import numpy as np
import matplotlib.pyplot as plt

# Criação do modelo
model = Model(sense=maximize)

# Variáveis de decisão (quantidade de produção das ligas em toneladas)
x = model.add_var(name="Liga de Baixa Resistência", var_type=CONTINUOUS)  # Liga de Baixa Resistência
y = model.add_var(name="Liga de Alta Resistência", var_type=CONTINUOUS)  # Liga de Alta Resistência

# Função objetivo: Maximizar a receita Z = 3000x + 5000y
model.objective = maximize(3000 * x + 5000 * y)

# Restrições de disponibilidade de matéria-prima
model += 0.5 * x + 0.2 * y <= 16  # Cobre
model += 0.25 * x + 0.3 * y <= 11  # Zinco
model += 0.25 * x + 0.5 * y <= 15  # Chumbo

model.optimize()

solution_x = x.x
solution_y = y.x
optimal_value = model.objective_value

print(f"Quantidade de Liga de Baixa Resistência (x): {solution_x:.2f}")
print(f"Quantidade de Liga de Alta Resistência (y): {solution_y:.2f}")
print(f"Receita Bruta Máxima: R$ {optimal_value:.2f}")


x = np.linspace(0, 40, 400)
y = np.linspace(0, 40, 400)

y1 = (16 - 0.5 * x) / 0.2

y2 = (11 - 0.25 * x) / 0.3

y3 = (15 - 0.25 * x) / 0.5

plt.figure(figsize=(10, 8))
plt.plot(x, y1, label=r'$0.5x + 0.2y \leq 16$', color='blue')
plt.plot(x, y2, label=r'$0.25x + 0.3y \leq 11$', color='green')
plt.plot(x, y3, label=r'$0.25x + 0.5y \leq 15$', color='red')
plt.plot(solution_x, solution_y, 'ro', label="Solução Ótima")

plt.fill_between(x, 0, np.minimum(np.minimum(y1, y2), y3), where=(y1 >= 0) & (y2 >= 0) & (y3 >= 0), color='grey', alpha=0.3)

plt.xlim((0, 40))
plt.ylim((0, 40))
plt.xlabel('x (Toneladas de Liga de Baixa Resistência)')
plt.ylabel('y (Toneladas de Liga de Alta Resistência)')
plt.legend()
plt.title('Região Viável para o Problema de Produção de Ligas Metálicas')

plt.grid(True)
plt.show()

