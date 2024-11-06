from mip import Model, xsum, maximize, CONTINUOUS 
import matplotlib.pyplot as plt  

# Criar um modelo  
model = Model("production")  

# Definir as variáveis de decisão  
x1 = model.add_var(name="Calças", var_type=CONTINUOUS)  # Lotes de calças  
x2 = model.add_var(name="Camisas", var_type=CONTINUOUS)  # Lotes de camisas  

# Função objetivo  
model.objective = maximize(500 * x1 + 800 * x2)  

# Restrições  
model.add_constr(10 * x1 + 20 * x2 <= 50, "mão_de_obra_nao_especializada")  
model.add_constr(10 * x2 <= 30, "mão_de_obra_especializada")  
model.add_constr(x1 / 5 + x2 / 10 <= 80, "maquina_1")  
model.add_constr(x1 / 3 + x2 / 3.5 <= 130, "maquina_2")  
model.add_constr(12 * x1 + 8 * x2 <= 120, "materia_prima_A")  
model.add_constr(10 * x1 + 15 * x2 <= 100, "materia_prima_B")  

# Resolver o modelo  
model.optimize()  

# Mostrar os resultados  
print("Solução ótima:")  
print(f"Lotes de Calças: {x1.x}")  
print(f"Lotes de Camisas: {x2.x}")  

# Dados para a visualização  
labels = ['Calças', 'Camisas']  
values = [x1.x, x2.x]  

# Plotando os resultados  
plt.bar(labels, values, color=['blue', 'orange'])  
plt.ylabel('Quantidade de Lotes')  
plt.title('Produção Ótima de Calças e Camisas')  
plt.show()