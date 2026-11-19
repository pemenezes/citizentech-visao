# Visão computacional — CitizenTech (FIAP Global Solution 2026.2)

Componente de visão do CitizenTech. A entrega é um farol de fase para faixa de pedestre: a tela mostra `ABRE VIA` ou `PEDESTRE`. O relatório está em `docs/relatorio.html`.

## Grupo

- Anny Carolina — RM98295
- Henrique Lima — RM551528
- Pedro Menezes — RM97432

Disciplina Applied Computer Vision, FIAP, Global Solution 2026.2.

Repositório: https://github.com/pemenezes/citizentech-visao

## Ambiente

Tudo que o projeto baixa (venv, caches, dados, pesos, treinos, vídeo) fica em `D:\citizentech\cv`. Este repositório é só `D:\citizentech\cv\repo`.

No PowerShell, no início de cada sessão:

```powershell
. D:\citizentech\cv\repo\scripts\env.ps1
python D:\citizentech\cv\repo\scripts\check_env.py
```

O ambiente virtual já criado é `D:\citizentech\cv\envs\cv` (Python 3.12). O peso usado no farol é o YOLO26n público do COCO, em `D:\citizentech\cv\models\yolo26n.pt`. Não houve treino novo para este tema.

## Demo

O script lê um vídeo, conta pessoa e veículo nas regiões da cena e grava a fase quadro a quadro. Os clipes ficam fora do Git, em `D:\citizentech\cv\video\farol`, porque há rostos e placas. A licença é a da Pexels.

```powershell
. D:\citizentech\cv\repo\scripts\env.ps1
python D:\citizentech\cv\repo\scripts\rodar_farol.py --cena londres
```

As cenas prontas são `londres`, `espera`, `esquina`, `faixa` e `transito`. A saída padrão é `D:\citizentech\cv\video\farol\{cena}_anotada.mp4`. A tela escreve a fase e as contagens `faixa`, `via` e `espera`.

A fase começa em `ABRE VIA`. Pessoa com o pé na pintura passa para `PEDESTRE` na hora. A volta pede 5 segundos sem pessoa na faixa. Com a via aberta, quem espera na calçada só recebe a fase com a faixa livre de veículo, o verde mínimo já corrido e a via vazia há 3 segundos, ou aos 20 segundos de espera.

## Medidas (19/11/2026)

O tempo inclui detecção, desenho e gravação do mp4, na RTX 2060.

| Cena | Quadros/s | Fase |
| --- | ---: | --- |
| londres | 29,9 | PEDESTRE 12 s, ABRE VIA 15 s |
| espera | 14,0 | ABRE VIA 21 s |
| esquina | 27,8 | PEDESTRE 55 s |
| faixa | 32,5 | PEDESTRE 56 s |
| transito | 30,3 | PEDESTRE 84 s |

A comparação de 60% contra um operador não foi feita. O detalhe quadro a quadro está em `docs/farol_andamento.md`.
