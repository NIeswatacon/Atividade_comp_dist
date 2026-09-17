# Disponibilidade de um serviço replicado

Projeto Python para comparar a fórmula binomial com uma simulação de Monte Carlo.
Requer Python 3.10 ou superior. Não depende de Jupyter ou ipykernel.

## Dedução da fórmula (Exercício 1.1)

Considere um serviço replicado em `n` servidores independentes, cada um disponível
em um dado instante com probabilidade `p` (e indisponível com probabilidade `1-p`).
O serviço é acessado de forma consistente quando pelo menos `k` dos `n` servidores
estão disponíveis, com `0 < k ≤ n`.

**Caso k = 1 (operação de consulta).** O serviço fica indisponível somente se
*todos* os `n` servidores estiverem indisponíveis ao mesmo tempo. Como os
servidores são independentes, a probabilidade de todos falharem é o produto das
probabilidades individuais de falha: `(1-p)^n`. Logo, a disponibilidade é o
complemento desse evento:

`A(n, 1, p) = 1 - (1-p)^n`

**Caso k = n (operação de atualização).** Aqui o serviço só fica disponível se
*todos* os `n` servidores estiverem disponíveis simultaneamente. Novamente pela
independência, essa probabilidade é o produto das probabilidades individuais de
sucesso:

`A(n, n, p) = p^n`

**Caso geral (1 ≤ k ≤ n).** Seja `X` o número de servidores disponíveis entre os
`n`. Como cada servidor é um ensaio de Bernoulli independente com probabilidade de
sucesso `p`, `X` segue uma distribuição binomial: `P(X = i) = C(n,i) · p^i · (1-p)^(n-i)`,
onde `C(n,i)` é o número de combinações de `n` servidores tomados `i` a `i`
(quais deles estão disponíveis). O serviço está disponível quando `X ≥ k`, ou seja,
quando ocorre qualquer uma das combinações com `k`, `k+1`, ..., ou `n` servidores
disponíveis (eventos mutuamente exclusivos, então as probabilidades se somam):

`A(n, k, p) = P(X ≥ k) = Σ (i = k até n) de C(n,i) · p^i · (1-p)^(n-i)`

Essa fórmula geral é consistente com os dois casos extremos: para `k=1`, a soma de
`i=1` até `n` é o complemento de `P(X=0) = (1-p)^n`, recaindo em `1-(1-p)^n`; para
`k=n`, a soma tem um único termo, `C(n,n)·p^n·(1-p)^0 = p^n`. É essa fórmula geral
que está implementada em `analitica()`, no arquivo `modelo.py`.

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
python main.py --n 1 5 10 20 --p 0.3 0.5 0.8 --rodadas 100000
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

O comando padrão compara `n` em 1, 5, 10 e 20 (valores fixos/travados) contra
`p` em 0.8, 0.9, 0.95 e 0.99, com 100.000 rodadas cada combinação: 48 combinações
no total. Em `resultados/`, gera `comparacao.csv`, `configuracao.json`,
`comparacao_por_p.png`, `comparacao_curvas_n.png` e `comparacao_final.png`. A nova
execução substitui os arquivos dessa pasta. Use `--saida outra_pasta` para guardar
execuções separadas.

## Gráficos

`comparacao_por_p.png` é o gráfico mais detalhado: eixo x = probabilidade (p), eixo
y = disponibilidade, comparando a fórmula analítica (linha) com a simulação
(marcador "x"). Ele tem um painel por valor de `n` travado (cada `n` passado em
`--n` vira uma linha de painéis) e uma coluna por caso de `k` (k=1, k=n/2, k=n) —
assim dá para ver como a disponibilidade cresce com p, para cada configuração de
servidores.

`comparacao_curvas_n.png` segue o esboço do enunciado do Exercício 1.2: dois
painéis (k=1/consulta e k=n/atualização), cada um com uma curva por valor de `n`
sobreposta no mesmo eixo, mostrando o efeito da probabilidade `p` (de 0 a 1) na
disponibilidade. A linha usa a fórmula analítica em uma grade densa de p; os
marcadores "x" mostram a frequência experimental apenas nos valores de p realmente
simulados. Fica evidente o trade-off: aumentar `n` melhora a disponibilidade da
consulta (k=1), mas piora a da atualização (k=n), exceto quando p está bem
próximo de 1.

`comparacao_final.png` mostra a fórmula versus a simulação diretamente (dispersão
com a diagonal de concordância perfeita) e as diferenças experimental − analítica,
juntando todas as combinações de n, p e k testadas.

## Modelo e interpretação

Assumimos disponibilidades independentes, mesma probabilidade p para cada servidor
e serviço operacional quando pelo menos k servidores estão disponíveis, conforme a
fórmula deduzida acima (`A(n,k,p)`, implementada em `analitica()`).

Em cada rodada da simulação, cada servidor recebe um sorteio uniforme entre 0 e 1.
Se o sorteio é menor ou igual a p, ele está disponível. A frequência de rodadas
com pelo menos k disponíveis é a estimativa experimental. A simulação não usa a
fórmula para obter sua frequência. O processamento em lotes limita o uso de memória.

Comparamos k=1, k=n/2 e k=n para qualquer n inteiro positivo, incluindo ímpar.
Para n ímpar, k=n/2 é arredondado (`round(n/2)`, com empate ".5" indo para o par
mais próximo — ex.: n=5 vira k=2); o mínimo é sempre 1, então para n=1 os três
casos coincidem (k=1). k=n/2 representa metade, **não maioria estrita**. A hipótese
de consistência depende do protocolo; aqui seguimos o limiar fornecido pelo
exercício. As funções em modelo.py aceitam qualquer inteiro 1<=k<=n.

Valores analíticos e experimentais próximos indicam concordância. O gráfico de
diferenças permite observar desvios que ficam escondidos pela sobreposição das curvas.
Mais rodadas reduzem o erro típico, mas não garantem menor erro em cada execução.
Uma frequência de 100% significa que nenhuma falha foi observada na amostra,
não que a probabilidade real seja exatamente 100%. Valores exibidos são arredondados.
