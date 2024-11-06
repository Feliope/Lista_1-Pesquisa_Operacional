from mip import Model, maximize, CONTINUOUS
import matplotlib.pyplot as plt

# Definindo o modelo
m = Model(sense=maximize)

# Variáveis de decisão: toneladas de gasolina bruta e gás/óleo processadas
x = m.add_var(var_type=CONTINUOUS, name="Gasolina Bruta")
y = m.add_var(var_type=CONTINUOUS, name="Gás/Óleo")

# Função objetivo (maximizar lucro total)
m.objective = 10 * x + 7 * y

# Restrições de capacidade em cada operação
m += x <= 500000  # Destilação para gasolina bruta
m += y <= 600000  # Destilação para gás/óleo
m += x <= 400000  # Dessulfurização para gasolina bruta
m += y <= 500000  # Dessulfurização para gás/óleo
m += x <= 300000  # Reforming para gasolina bruta
m += y <= 450000  # Cracking para gás/óleo

# Resolver o modelo
m.optimize()

# Verificar se uma solução viável foi encontrada
if m.num_solutions:
    print("Quantidade a ser processada em toneladas:")
    print(f"Gasolina Bruta (x): {x.x} toneladas")
    print(f"Gás/Óleo (y): {y.x} toneladas")
    print(f"Lucro Total: {m.objective_value} reais")
else:
    print("Não foi encontrada uma solução viável para as restrições dadas.")


# Dados para o gráfico
produtos = ['Gasolina Bruta', 'Gás/Óleo']
quantidades = [x.x, y.x]
lucro_unitario = [10, 7]
lucro_total = [q * l for q, l in zip(quantidades, lucro_unitario)]

# Gráfico de barras das quantidades processadas e lucro total
fig, ax1 = plt.subplots()

# Plotando as quantidades
ax1.bar(produtos, quantidades, color='b', alpha=0.6)
ax1.set_xlabel("Produtos")
ax1.set_ylabel("Quantidade (toneladas)", color='b')
ax1.tick_params(axis='y', labelcolor='b')

# Criando eixo secundário para o lucro total
ax2 = ax1.twinx()
ax2.plot(produtos, lucro_total, color='r', marker='o')
ax2.set_ylabel("Lucro Total (reais)", color='r')
ax2.tick_params(axis='y', labelcolor='r')

plt.title("Quantidade Processada e Lucro Total")
plt.show()
