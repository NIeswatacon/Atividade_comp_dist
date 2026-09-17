"""Gráficos exportados em PNG, sem necessidade de interface gráfica."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from modelo import analitica

CASOS = ('k=1', 'k=n/2', 'k=n')
CASOS_EXTREMOS = (('k=1', 'consulta'), ('k=n', 'atualização'))


def gerar_graficos(resultados, destino):
    gerar_grafico_por_p(resultados, destino)
    gerar_grafico_curvas_n(resultados, destino)
    gerar_grafico_final(resultados, destino)


def gerar_grafico_por_p(resultados, destino):
    """Eixo x = probabilidade (p), disponibilidade (fórmula e simulação) no eixo y,
    com um painel por valor de n travado (fixo) e uma coluna por caso de k."""
    valores_n = sorted({r['n'] for r in resultados})
    fig, eixos = plt.subplots(len(valores_n), 3, squeeze=False,
                             figsize=(13, 3.5*len(valores_n)),
                             layout='constrained')
    for i, n in enumerate(valores_n):
        for j, caso in enumerate(CASOS):
            ax = eixos[i, j]
            grupo = sorted((r for r in resultados if r['n']==n and r['caso']==caso),
                           key=lambda r: r['p'])
            ax.plot([r['p'] for r in grupo], [r['analitica'] for r in grupo],
                    label='Fórmula', color='tab:blue')
            ax.scatter([r['p'] for r in grupo], [r['experimental'] for r in grupo],
                       label='Simulação', marker='x', color='tab:orange', zorder=3)
            ax.set(title=f'{caso} | n={n}', xlabel='Probabilidade (p)',
                   ylabel='Disponibilidade', ylim=(-0.02, 1.02))
            ax.grid(alpha=0.25)
            ax.legend()
    fig.savefig(destino/'comparacao_por_p.png', dpi=160)
    plt.close(fig)


def gerar_grafico_curvas_n(resultados, destino):
    """Estilo do slide do enunciado (Exercício 1.2): um painel para k=1 (consulta) e
    outro para k=n (atualização), eixo x = probabilidade (p) variando continuamente de
    0 a 1, eixo y = disponibilidade, com uma curva por valor de n travado. A linha usa
    a fórmula analítica (grade densa de p, não só os pontos simulados); os marcadores
    'x' mostram a frequência experimental apenas nos valores de p realmente simulados."""
    valores_n = sorted({r['n'] for r in resultados})
    grade_p = [i/200 for i in range(201)]  # 0.000, 0.005, ..., 1.000
    cmap = plt.get_cmap('viridis')
    cores = [cmap(i/max(1, len(valores_n)-1)) for i in range(len(valores_n))]
    fig, eixos = plt.subplots(1, 2, figsize=(12, 5.5), layout='constrained')
    for ax, (caso, nome) in zip(eixos, CASOS_EXTREMOS):
        for n, cor in zip(valores_n, cores):
            k = 1 if caso == 'k=1' else n
            ax.plot(grade_p, [analitica(n, k, p) for p in grade_p],
                    color=cor, label=f'n={n}')
            grupo = sorted((r for r in resultados if r['n']==n and r['caso']==caso),
                           key=lambda r: r['p'])
            if grupo:
                ax.scatter([r['p'] for r in grupo], [r['experimental'] for r in grupo],
                           color=cor, marker='x', zorder=3)
        ax.set(title=f'{caso} ({nome})', xlabel='Probabilidade (p)',
               ylabel='Disponibilidade', xlim=(-0.02, 1.02), ylim=(-0.02, 1.02))
        ax.grid(alpha=0.25)
        ax.legend(title='n (linha = fórmula, x = simulação)', fontsize=8)
    fig.savefig(destino/'comparacao_curvas_n.png', dpi=160)
    plt.close(fig)


def gerar_grafico_final(resultados, destino):
    fig, (ax, erro) = plt.subplots(1, 2, figsize=(12, 5), layout='constrained')
    for caso in CASOS:
        grupo = [r for r in resultados if r['caso']==caso]
        x = [r['analitica'] for r in grupo]
        ax.scatter(x, [r['experimental'] for r in grupo], label=caso, alpha=0.7)
        erro.scatter(x, [r['experimental']-r['analitica'] for r in grupo],
                     label=caso, alpha=0.7)
    ax.plot([0, 1], [0, 1], 'k--', label='Concordância perfeita')
    ax.set(title='Fórmula versus simulação', xlabel='Disponibilidade analítica',
           ylabel='Disponibilidade experimental', xlim=(-0.02, 1.02), ylim=(-0.02, 1.02))
    erro.axhline(0, color='black', linestyle='--')
    erro.set(title='Diferenças entre os métodos', xlabel='Disponibilidade analítica',
             ylabel='Experimental − analítica')
    for eixo in (ax, erro):
        eixo.grid(alpha=0.25)
        eixo.legend()
    fig.savefig(destino/'comparacao_final.png', dpi=160)
    plt.close(fig)
