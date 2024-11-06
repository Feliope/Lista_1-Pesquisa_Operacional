from mip import Model, xsum, MAXIMIZE, INTEGER
import matplotlib.pyplot as plt

# Criando o modelo
m = Model(sense=MAXIMIZE)

# Variáveis de decisão
x1 = m.add_var(var_type=INTEGER, name='Boeing_717')      # Boeing 717
x2 = m.add_var(var_type=INTEGER, name='Boeing_737_500')  # Boeing 737-500
x3 = m.add_var(var_type=INTEGER, name='MD_11')           # MD-11

# Função objetivo: maximizar a receita teórica total
m.objective = xsum([330 * x1, 300 * x2, 420 * x3])

# Restrições
m += 5.1 * x1 + 3.6 * x2 + 6.8 * x3 <= 220     # Restrição de orçamento
m += x2 <= 40                                   # Limite de manutenção para Boeing 737-500
m += x3 <= (3 / 4) * x2                         # Esforço de manutenção relativo ao MD-11
m += x1 <= 30                                   # Limite de pilotos para Boeing 717
m += x2 <= 20                                   # Limite de pilotos para Boeing 737-500
m += x3 <= 10                                   # Limite de pilotos para MD-11

# Resolvendo o modelo
m.optimize()

# Extraindo os valores ótimos das variáveis
x1_value = x1.x
x2_value = x2.x
x3_value = x3.x

# Exibindo os resultados
print(f"Quantidade ótima de Boeing 717: {x1_value}")
print(f"Quantidade ótima de Boeing 737-500: {x2_value}")
print(f"Quantidade ótima de MD-11: {x3_value}")
print(f"Receita total: {m.objective_value}")

# Plotando o gráfico com a quantidade de cada avião
labels = ['Boeing 717', 'Boeing 737-500', 'MD-11']
values = [x1_value, x2_value, x3_value]

plt.bar(labels, values)
plt.title('Quantidade de Aviões Adquiridos')
plt.ylabel('Quantidade')
plt.show()