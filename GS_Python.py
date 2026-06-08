import random

# CONFIG

nome_missao = "MISSION CONTROL AI"
equipe = "Equipe Omega"

areas_monitoradas = [
    "Temperatura interna",
    "Comunicação com a base",
    "Sistema de energia",
    "Suporte de oxigênio",
    "Estabilidade operacional"
]

historico_missoes = []
eventos_ativos = []

# EVENTOS CONTÍNUOS

def aplicar_eventos_ativos(ciclo):
    global eventos_ativos

    novos_eventos = []

    for evento in eventos_ativos:
        tipo = evento["tipo"]

        if tipo == "tempestade_solar":
            ciclo[1] -= 10
            ciclo[2] -= 10

        elif tipo == "falha_energia":
            ciclo[2] -= 7
            ciclo[4] -= 3

        elif tipo == "vazamento_oxigenio":
            ciclo[3] -= 5

        elif tipo == "instabilidade_sistema":
            ciclo[4] -= 5
            ciclo[1] -= 3

        print(f"Efeito contínuo ativo: {tipo}")

        evento["duracao"] -= 1

        if evento["duracao"] > 0:
            novos_eventos.append(evento)

    eventos_ativos = novos_eventos

# GERAÇÃO DE DADOS

def gerar_dados_missao(qtd_ciclos=6):
    dados = []

    limites = [45, 100, 100, 100, 100]

    atual = [
        random.randint(25, 32),
        random.randint(70, 95),
        random.randint(70, 95),
        random.randint(85, 100),
        random.randint(75, 95)
    ]

    for ciclo in range(qtd_ciclos):

        print(f"\n===== CICLO {ciclo+1} =====")

        ciclo_atual = atual[:]

        # Eventos
        if ciclo >= 3 and random.random() < 0.4 and len(eventos_ativos) < 2:

            evento = random.choice([
                "tempestade_solar",
                "falha_energia",
                "vazamento_oxigenio",
                "instabilidade_sistema"
            ])

            duracao = random.randint(1, 2)

            eventos_ativos.append({
                "tipo": evento,
                "duracao": duracao
            })

            print("\nALERTA DE EVENTO CRÍTICO:", evento)

        # aplicar eventos ativos
        aplicar_eventos_ativos(ciclo_atual)

        # variação natural
        for i in range(5):
            if i == 0:
                variacao = random.randint(-5, 5)
            else:   
                variacao = random.randint(-13, 5)

            ciclo_atual[i] += variacao
            ciclo_atual[i] = max(10, min(limites[i], ciclo_atual[i]))

        dados.append(ciclo_atual)
        atual = ciclo_atual

        print("Dados:", ciclo_atual)

    return dados


dados_missao = gerar_dados_missao()

# CLASSIFICAÇÕES

def classificar_temp(t):
    if t < 18: return "ATENÇÃO", 1
    if t <= 30: return "NORMAL", 0
    if t <= 35: return "ATENÇÃO", 1
    return "CRÍTICO", 2

def classificar_com(c):
    if c < 30: return "CRÍTICO", 2
    if c < 60: return "ATENÇÃO", 1
    return "NORMAL", 0

def classificar_bat(b):
    if b < 20: return "CRÍTICO", 2
    if b < 50: return "ATENÇÃO", 1
    return "NORMAL", 0

def classificar_oxi(o):
    if o < 50: return "CRÍTICO", 2
    if o < 70: return "ATENÇÃO", 1
    return "NORMAL", 0

def classificar_est(e):
    if e < 40: return "CRÍTICO", 2
    if e < 70: return "ATENÇÃO", 1
    return "NORMAL", 0

# REPARO AUTOMÁTICO

def reparar(ciclo, classificacoes):
    reparos = 0
    limites = [45, 100, 100, 100, 100]

    itens = []

    for i in range(5):
        classe, pontos = classificacoes[i]

        if i == 0:
            severidade = ciclo[i]
        else:
            severidade = -ciclo[i]

        itens.append((i, classe, pontos, severidade))

    itens.sort(key=lambda x: (x[2], x[3]), reverse=True)

    for i, classe, pontos, _ in itens:
        if reparos >= 2:
            break

        if classe == "NORMAL":
            continue

        if i == 0:
            ciclo[i] -= 5
        elif i == 1:
            ciclo[i] += 10
        elif i == 2:
            ciclo[i] += 10
        elif i == 3:
            ciclo[i] += 5
        elif i == 4:
            ciclo[i] += 5

        ciclo[i] = max(10, min(limites[i], ciclo[i]))

        print(f"Reparo automático em {areas_monitoradas[i]}")

        reparos += 1

# PROCESSAMENTO

def analisar_ciclo(ciclo):
    funcs = [
        classificar_temp,
        classificar_com,
        classificar_bat,
        classificar_oxi,
        classificar_est
    ]

    classificacoes = []
    risco = 0

    for i in range(5):
        classe, pontos = funcs[i](ciclo[i])
        classificacoes.append((classe, pontos))
        risco += pontos

    return classificacoes, risco


def classificar_ciclo(r):
    if r <= 2: return "MISSÃO ESTÁVEL"
    if r <= 5: return "MISSÃO EM ATENÇÃO"
    return "MISSÃO CRÍTICA"


def gerar_recomendacao(classificacoes):
    for i, (classe, _) in enumerate(classificacoes):
        if classe == "CRÍTICO":
            return f"Prioridade crítica em {areas_monitoradas[i]}"
    return "Operação normal"

# EXECUÇÃO

def executar():
    riscos = []
    total_areas = [0]*5

    print("="*60)
    print("MISSION CONTROL AI")
    print("="*60)

    for i, ciclo in enumerate(dados_missao):

        print(f"\nCICLO {i+1}")
        print("-"*60)

        classificacoes, risco = analisar_ciclo(ciclo)

        reparar(ciclo, classificacoes)

        classificacoes, risco = analisar_ciclo(ciclo)

        riscos.append(risco)

        for j in range(5):
            total_areas[j] += classificacoes[j][1]
            print(f"{areas_monitoradas[j]}: {ciclo[j]} | {classificacoes[j][0]}")

        print("Risco:", risco)
        print("Classificação:", classificar_ciclo(risco))
        print("Recomendação:", gerar_recomendacao(classificacoes))

    # RELATÓRIO FINAL

    print("\n" + "="*60)
    print(f"RELATÓRIO FINAL {nome_missao}")
    print(equipe)
    print("="*60)

    medias = [sum(col)/len(dados_missao) for col in zip(*dados_missao)]

    for i in range(5):
        print(f"Média {areas_monitoradas[i]}: {round(medias[i],2)}")

    print("Maior risco:", max(riscos))
    print("Ciclo crítico:", riscos.index(max(riscos))+1)

    risco_medio = sum(riscos)/len(riscos)
    print("Risco médio:", round(risco_medio,2))

    if riscos[-1] > riscos[0]:
        print("Tendência: Piora")
    elif riscos[-1] < riscos[0]:
        print("Tendência: Melhora")
    else:
        print("Tendência: Estável")

    pior_area = total_areas.index(max(total_areas))
    print("Área mais afetada:", areas_monitoradas[pior_area])
    print("Riscos em cada etapa:", riscos)
    print("Soma dos riscos de cada Área:", total_areas)

executar()