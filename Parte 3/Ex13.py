from mip import Model, xsum, MAXIMIZE, INTEGER
import matplotlib.pyplot as plt

# Dados do problema
horas_materias = {
    "Matemática": [24, 30, 28, 24, 30, 24, 28, 20, 28, 24],
    "Química": [20, 18, 20, 18, 20, 18, 18, 18, 18, 18],
    "Física": [18, 20, 18, 20, 18, 18, 20, 18, 20, 18],
    "Biologia": [18, 20, 18, 20, 18, 20, 20, 18, 18, 20],
    "Português": [24, 20, 20, 24, 20, 20, 20, 20, 20, 20],
    "Línguas": [8, 10, 8, 10, 8, 10, 8, 8, 8, 8],
    "Geografia": [10, 12, 10, 12, 10, 12, 10, 10, 10, 10],
    "História": [10, 12, 10, 12, 10, 10, 12, 10, 10, 10]
}
meses = list(range(10))  # Representando de março a dezembro
materias = list(horas_materias.keys())

# Tempo necessário para cada trabalho e prova por mês
trabalhos = { 
    "Matemática": [1, 0, 0, 1, 1, 1, 0, 1, 0, 1],
    "Química": [1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
    "Física": [1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
    "Biologia": [1, 1, 1, 0, 1, 1, 1, 1, 0, 0],
    "Português": [0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
    "Línguas": [1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    "Geografia": [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
    "História": [1, 0, 1, 1, 1, 0, 1, 1, 1, 1]
}

provas = {
    "Matemática": [1, 1, 1, 0, 2, 1, 0, 1, 1, 1],
    "Química": [1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    "Física": [0, 1, 1, 0, 2, 1, 1, 1, 1, 0],
    "Biologia": [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    "Português": [1, 1, 0, 1, 2, 1, 0, 1, 1, 0],
    "Línguas": [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    "Geografia": [0, 1, 0, 1, 2, 1, 1, 1, 1, 0],
    "História": [1, 0, 1, 1, 1, 0, 1, 1, 1, 1]
}

# Parâmetros de tempo
horas_por_mes = 720 - 8*30 - (1+2)*30  # Total de horas no mês ajustado
min_lazer_mes = 20  # Horas mínimas de lazer por mês
total_lazer = 250   # Lazer total ao longo dos nove meses

# Criando o modelo
model = Model(sense=MAXIMIZE)

# Variáveis de decisão
x = [[model.add_var(var_type=INTEGER, lb=0, name=f"x_{mes}_{materia}") for materia in materias] for mes in meses]  # Horas de estudo para cada matéria em cada mês

# Função objetivo: maximizar as horas de estudo totais
model.objective = xsum(x[mes][s] for mes in meses for s in range(len(materias)))

# Restrições
# Restrições de carga horária para cada matéria em cada mês
for mes in meses:
    for s, materia in enumerate(materias):
        model += x[mes][s] <= horas_materias[materia][mes]  # Respeitar o máximo de horas disponível por matéria

# Restrições de lazer mínimo por mês e lazer total
for mes in meses:
    total_trabalhos_provas = xsum(trabalhos[materia][mes] * 4 + provas[materia][mes] * 10 for materia in materias)
    model += xsum(x[mes][s] for s in range(len(materias))) + total_trabalhos_provas <= horas_por_mes - min_lazer_mes

# Restrição de lazer total ao longo do ano
model += xsum(min_lazer_mes for _ in meses) >= total_lazer

# Otimizar
model.optimize()

# Imprimir solução
if model.num_solutions:
    for mes in meses:
        print(f"Mês {mes + 3}:")
        for s, materia in enumerate(materias):
            print(f"  {materia}: {x[mes][s].x} horas de estudo")
else:
    print("Não foi encontrada nenhuma solução viável.")
