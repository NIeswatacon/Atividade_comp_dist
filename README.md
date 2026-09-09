# Disponibilidade de um serviço replicado

Projeto Python para comparar a fórmula binomial com uma simulação de Monte Carlo.
Requer Python 3.10 ou superior. Não depende de Jupyter ou ipykernel.

## Instalar e executar

Abra o terminal nesta pasta e execute:

```sh
python -m venv .venv
```

No Windows, é possível instalar e executar sem ativar o ambiente:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

No Linux ou macOS:

```sh
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

Nos exemplos seguintes, `python` representa o Python do ambiente preparado.

```sh
python main.py --rodadas 100000 --semente 2026
python main.py --n 4 10 20 --p 0.3 0.5 0.8 --rodadas 100000
python main.py --sem-graficos
```

Sem `--semente`, cada execução gera uma nova sequência pseudoaleatória. A semente
é exibida e registrada para permitir a repetição com os mesmos parâmetros e ambiente.
A opção `--sem-graficos` precisa somente de NumPy.

## Organização

- `modelo.py`: fórmula e sorteio dos servidores, com validação dos parâmetros.
- `main.py`: parâmetros, execução e exportação dos resultados.
- `graficos.py`: gráficos comparativos, salvos em PNG.
- `requirements.txt`: dependências.

O comando padrão executa 120 combinações com 100.000 rodadas cada.
Em `resultados/`, gera `comparacao.csv`, `configuracao.json`,
`comparacao_por_n.png` e `comparacao_final.png`. A nova execução substitui os
arquivos dessa pasta. Use `--saida outra_pasta` para guardar execuções separadas.

## Modelo e interpretação

Assumimos disponibilidades independentes, mesma probabilidade p para cada servidor
e serviço operacional quando pelo menos k servidores estão disponíveis.

`A(n,k,p) = soma de i=k até n de C(n,i) * p**i * (1-p)**(n-i)`.

Em cada rodada da simulação, cada servidor recebe um sorteio uniforme entre 0 e 1.
Se o sorteio é menor ou igual a p, ele está disponível. A frequência de rodadas
com pelo menos k disponíveis é a estimativa experimental. A simulação não usa a
fórmula para obter sua frequência. O processamento em lotes limita o uso de memória.

Comparamos k=1, k=n/2 e k=n, usando n par. k=n/2 representa metade, **não maioria
estrita**. A hipótese de consistência depende do protocolo; aqui seguimos o limiar
fornecido pelo exercício. As funções em modelo.py aceitam qualquer inteiro 1<=k<=n.

Valores analíticos e experimentais próximos indicam concordância. O gráfico de
diferenças permite observar desvios que ficam escondidos pela sobreposição das curvas.
Mais rodadas reduzem o erro típico, mas não garantem menor erro em cada execução.
Uma frequência de 100% significa que nenhuma falha foi observada na amostra,
não que a probabilidade real seja exatamente 100%. Valores exibidos são arredondados.
