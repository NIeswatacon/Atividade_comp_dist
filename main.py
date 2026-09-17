"""Execução: python main.py --rodadas 100000 --semente 2026."""
import argparse
import csv
import json
import secrets
from pathlib import Path

import numpy as np
from modelo import analitica, simular


def main():
    parser = argparse.ArgumentParser(description='Compara fórmula binomial e simulação.')
    parser.add_argument('--n', nargs='+', type=int, default=[1, 5, 10, 20])
    parser.add_argument('--p', nargs='+', type=float, default=[0.3, 0.3, 0.8, 0.95])
    parser.add_argument('--rodadas', type=int, default=100_000)
    parser.add_argument('--semente', type=int, help='Omitir gera uma nova sequência a cada execução.')
    parser.add_argument('--saida', type=Path, default=Path('resultados'))
    parser.add_argument('--sem-graficos', action='store_true')
    args = parser.parse_args()
    if any(n < 1 for n in args.n):
        parser.error('--n deve conter inteiros positivos (n >= 1)')
    if any(not 0 <= p <= 1 for p in args.p) or args.rodadas <= 0:
        parser.error('Use probabilidades entre 0 e 1 e rodadas positivas')
    if args.semente is not None and args.semente < 0:
        parser.error('A semente deve ser não negativa')
    if not args.sem_graficos:
        try:
            from graficos import gerar_graficos
        except ModuleNotFoundError as exc:
            parser.error(f'Dependência ausente: {exc.name}. Execute python -m pip install -r requirements.txt')
    semente = args.semente if args.semente is not None else secrets.randbits(64)
    rng = np.random.default_rng(semente)
    resultados = []
    print(f'Semente: {semente}; rodadas por combinação: {args.rodadas}')
    print(' n    p    caso       analítica experimental erro absoluto')
    for n in args.n:
        k_meio = max(1, round(n/2))  # Para n ímpar, arredonda (empates vão para o par mais próximo).
        for p in args.p:
            for caso, k in [('k=1', 1), ('k=n/2', k_meio), ('k=n', n)]:
                a = analitica(n, k, p)
                e = simular(n, k, p, args.rodadas, rng)
                resultados.append(dict(n=n, k=k, p=p, caso=caso, rodadas=args.rodadas,
                                       analitica=a, experimental=e, erro_absoluto=abs(e-a)))
                print(f'{n:2} {p:5.2f} {caso:7} {a:12.8f} {e:12.8f} {abs(e-a):12.8f}')
    args.saida.mkdir(parents=True, exist_ok=True)
    with (args.saida/'comparacao.csv').open('w', newline='', encoding='utf-8-sig') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(resultados[0]), delimiter=';')
        escritor.writeheader()
        escritor.writerows(resultados)
    with (args.saida/'configuracao.json').open('w', encoding='utf-8') as arquivo:
        json.dump(dict(n=args.n, p=args.p, rodadas=args.rodadas, semente=semente,
                       numpy=np.__version__), arquivo, indent=2)
    if not args.sem_graficos:
        gerar_graficos(resultados, args.saida)
    print(f'Resultados salvos em {args.saida.resolve()}')


if __name__ == '__main__':
    main()
