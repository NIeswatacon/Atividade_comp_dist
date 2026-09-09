"""Gráficos exportados em PNG, sem necessidade de interface gráfica."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

CASOS = ('k=1', 'k=n/2', 'k=n')


def gerar_graficos(resultados, destino):
    probabilidades = sorted({r['p'] for r in resultados})
    fig, eixos = plt.subplots(len(probabilidades), 3, squeeze=False,
                             figsize=(13, 3.5*len(probabilidades)),
                             layout='constrained')
    for i, p in enumerate(probabilidades):
        for j, caso in enumerate(CASOS):
            ax = eixos[i, j]
            grupo = sorted((r for r in resultados if r['p']==p and r['caso']==caso),
                           key=lambda r: r['n'])
            ax.plot([r['n'] for r in grupo], [r['analitica'] for r in grupo],
                    label='Fórmula', color='tab:blue')
            ax.scatter([r['n'] for r in grupo], [r['experimental'] for r in grupo],
                       label='Simulação', marker='x', color='tab:orange', zorder=3)
            ax.set(title=f'{caso} | p={p:g}', xlabel='Servidores (n)',
                   ylabel='Disponibilidade', ylim=(-0.02, 1.02))
            ax.grid(alpha=0.25)
            ax.legend()
    fig.savefig(destino/'comparacao_por_n.png', dpi=160)
    plt.close(fig)

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
