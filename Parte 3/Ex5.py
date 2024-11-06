from mip import Model, xsum, MINIMIZE, INTEGER
import matplotlib.pyplot as plt

# Função para modelar a otimização multiobjetivo
def otimizar(peso_mao_obra, peso_arrecadacao, peso_leitos, peso_espaco):
    # Criação do modelo
    m = Model(sense=MINIMIZE)

    # Variáveis de decisão
    x1 = m.add_var(var_type=INTEGER, name='x1')  # Quartos com 1 leito
    x2 = m.add_var(var_type=INTEGER, name='x2')  # Quartos com 2 leitos
    x3 = m.add_var(var_type=INTEGER, name='x3')  # Quartos com 3 leitos

    # Funções objetivos

    # 1. Minimizar o esforço da mão de obra
    mao_obra = x1 + 0.8 * x2 + 0.8 * x3

    # 2. Maximizar a arrecadação (minimizando a inversa)
    arrecadacao = x1 + 0.5 * x2 + 0.33 * x3

    # 3. Maximizar o número de leitos (minimizando a inversa)
    leitos = -(x1 + 2 * x2 + 3 * x3)

    # 4. Minimizar o espaço necessário para a nova ala
    espaco = 10 * x1 + 14 * x2 + 17 * x3

    # Função objetivo agregada
    m.objective = peso_mao_obra * mao_obra + peso_arrecadacao * arrecadacao + peso_leitos * leitos + peso_espaco * espaco

    # Restrições
    m += x1 + x2 + x3 <= 70  # Total de quartos
    m += x1 + 2 * x2 + 3 * x3 >= 120  # Total de leitos
    m += 0.15 * (x1 + x2 + x3) <= x1  # Percentual de quartos com 1 leito
    m += x1 <= 0.30 * (x1 + x2 + x3)  # Percentual de quartos com 1 leito

    # Resolvendo o modelo
    m.optimize()

    # Extraindo resultados
    x1_value = x1.x
    x2_value = x2.x
    x3_value = x3.x

    # Resultados
    return {
        'quartos_1_leito': x1_value,
        'quartos_2_leitos': x2_value,
        'quartos_3_leitos': x3_value,
        'esforco_mao_obra': mao_obra.x,
        'arrecadacao': arrecadacao.x,
        'leitos': leitos.x,
        'espaco': espaco.x
    }

# Exemplos de otimização com diferentes pesos
resultados_1 = otimizar(peso_mao_obra=1, peso_arrecadacao=1, peso_leitos=1, peso_espaco=1)
resultados_2 = otimizar(peso_mao_obra=1, peso_arrecadacao=2, peso_leitos=1, peso_espaco=1)
resultados_3 = otimizar(peso_mao_obra=1, peso_arrecadacao=1, peso_leitos=2, peso_espaco=1)

# Exibindo resultados de cada otimização
print("Resultado 1 (Pesos iguais):")
print(resultados_1)
print("\nResultado 2 (Maior peso para arrecadação):")
print(resultados_2)
print("\nResultado 3 (Maior peso para número de leitos):")
print(resultados_3)

# Gráfico comparativo
labels = ['1 Leito', '2 Leitos', '3 Leitos']
valores_1 = [resultados_1['quartos_1_leito'], resultados_1['quartos_2_leitos'], resultados_1['quartos_3_leitos']]
valores_2 = [resultados_2['quartos_1_leito'], resultados_2['quartos_2_leitos'], resultados_2['quartos_3_leitos']]
valores_3 = [resultados_3['quartos_1_leito'], resultados_3['quartos_2_leitos'], resultados_3['quartos_3_leitos']]

# Plotando
x = range(len(labels))
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(x, valores_1, width=0.2, label='Resultado 1', align='center')
ax.bar([p + 0.2 for p in x], valores_2, width=0.2, label='Resultado 2', align='center')
ax.bar([p + 0.4 for p in x], valores_3, width=0.2, label='Resultado 3', align='center')

ax.set_xticks([p + 0.2 for p in x])
ax.set_xticklabels(labels)
ax.set_title('Distribuição de Quartos para Diferentes Pesos')
ax.legend()

plt.show()
