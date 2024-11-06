from mip import Model, xsum, MINIMIZE, BINARY, INTEGER, OptimizationStatus
import matplotlib.pyplot as plt

# Parâmetros do problema
b = [10, 12, 15, 14, 13, 9, 8, 7, 12, 10, 11, 14, 16, 15, 13, 10, 12, 14, 16, 18, 20, 15, 10, 8]  # Demanda mínima por hora
c = [5, 4, 6, 5, 5, 4, 4, 3, 5, 4, 5, 6, 7, 6, 5, 5, 4, 6, 7, 8, 9, 6, 4, 3]  # Custo adicional por hora excedente
n_hours = 24  # Número de horas

# Criando o modelo
m = Model(sense=MINIMIZE)

# Variáveis de decisão
x = [m.add_var(var_type=BINARY, name=f"x_{i}") for i in range(n_hours)]  # x[i] indica se um ônibus inicia na hora i
e = [m.add_var(var_type=INTEGER, lb=0, name=f"e_{i}") for i in range(n_hours)]  # e[i] é o excesso de ônibus na hora i

# Função objetivo: minimizar o custo adicional de ônibus excedentes
m.objective = xsum(c[i] * e[i] for i in range(n_hours))

# Restrições de operação por hora
for i in range(n_hours):
    # Somatório dos ônibus em operação na hora i (cada ônibus trafega por seis horas consecutivas)
    buses_in_operation = xsum(x[(i - j) % n_hours] for j in range(6))
    # Excesso de ônibus em relação à demanda mínima
    m += buses_in_operation - e[i] >= b[i]

# Resolvendo o modelo
status = m.optimize()

# Verificação do status da solução
if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
    # Extraindo os valores ótimos das variáveis
    x_values = [x[i].x for i in range(n_hours)]
    e_values = [e[i].x for i in range(n_hours)]
    buses_in_operation_values = [sum(x_values[(i - j) % n_hours] for j in range(6)) for i in range(n_hours)]

    # Exibindo os resultados
    print("Ônibus que iniciam em cada hora:", x_values)
    print("Excesso de ônibus por hora:", e_values)
    print("Ônibus em operação por hora:", buses_in_operation_values)
    print("Custo total adicional:", m.objective_value)

    # Plotando o gráfico de operação de ônibus e demanda
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 25), b, label="Demanda mínima (b)", marker='o', color="blue")
    plt.plot(range(1, 25), buses_in_operation_values, label="Ônibus em operação", marker='x', color="green")
    plt.bar(range(1, 25), e_values, label="Excesso de ônibus (e)", color="red", alpha=0.3)
    plt.xlabel("Hora do Dia")
    plt.ylabel("Número de Ônibus")
    plt.title("Planejamento de Operação de Ônibus por Hora")
    plt.legend()
    plt.show()
else:
    print("Não foi encontrada uma solução viável para o problema.")
