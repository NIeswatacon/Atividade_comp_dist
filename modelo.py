"""Modelo binomial e simulação independente da disponibilidade."""
from math import comb, fsum

import numpy as np


def validar(n, k, p):
    if type(n) is not int or n <= 0:
        raise ValueError('n deve ser um inteiro positivo')
    if type(k) is not int or not 1 <= k <= n:
        raise ValueError('k deve ser um inteiro entre 1 e n')
    if not 0 <= p <= 1:
        raise ValueError('p deve estar entre 0 e 1')


def analitica(n, k, p):
    """Probabilidade de pelo menos k dos n servidores estarem disponíveis."""
    validar(n, k, p)
    return min(1.0, fsum(comb(n, i) * p**i * (1-p)**(n-i)
                         for i in range(k, n+1)))


def simular(n, k, p, rodadas, rng):
    """Sorteia cada servidor em cada rodada; retorna a frequência de sucesso.

    Os lotes limitam a memória utilizada, mesmo com milhões de rodadas.
    Não utiliza a fórmula analítica para produzir o resultado.
    """
    validar(n, k, p)
    if type(rodadas) is not int or rodadas <= 0:
        raise ValueError('rodadas deve ser um inteiro positivo')
    sucessos = 0
    tamanho_lote = max(1, min(10_000, 1_000_000 // n))
    for inicio in range(0, rodadas, tamanho_lote):
        quantidade = min(tamanho_lote, rodadas-inicio)
        sorteios = rng.random((quantidade, n))
        disponiveis = sorteios <= p
        if p == 0:  # Garante o limite exato mesmo se o gerador retornar zero.
            disponiveis[:] = False
        sucessos += int(np.count_nonzero(disponiveis.sum(axis=1) >= k))
    return sucessos / rodadas
