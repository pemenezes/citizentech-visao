# Farol — andamento da madrugada

Branch `farol`. O Libras continua em `main`, no commit `a05dfdf`. Nada foi enviado ao GitHub.

## O que já está no disco

Os clipes ficam fora do Git, em `D:\citizentech\cv\video\farol`.

- `cruzamento.mp4` — Pexels 30609021, 1280×720, 30 fps, licença Pexels. Página: https://www.pexels.com/video/busy-urban-traffic-flow-at-intersection-30609021/
- `faixa.mp4` — Pexels 25775484, 720×1280, 30 fps, licença Pexels. Página: https://www.pexels.com/video/a-crosswalk-in-a-city-with-cars-and-people-25775484/

## Regra combinada

Três regiões: via A, via B e faixa. A tela mostra `ABRE A`, `ABRE B` ou `PEDESTRE`.

- Pessoa dentro da faixa segura `PEDESTRE`. A via que cruza não abre.
- Via aberta 3 s sem veículo, com veículo na outra, troca.
- Pedestre esperando abre a fase quando a faixa está livre de carro, ou aos 20 s.
- Verde mínimo de 5 s. A pessoa na faixa fura esse mínimo.
- Piso de aceite: 60% dos quadros, medido no clipe. O número só entra no relatório depois de medido.
- Peso: `D:\citizentech\cv\models\yolo26n.pt`, sem treino novo nesta primeira versão.

## Energia

Na tomada, suspender estava em 10 minutos e hibernar em 30. Os dois foram para nunca, para o trabalho seguir de madrugada. De manhã, para voltar:

```powershell
powercfg /change standby-timeout-ac 10
powercfg /change hibernate-timeout-ac 30
```

## Sondagem, 17/11 à noite

Sete quadros de cada clipe, confiança 0,25, peso `yolo26n.pt`.

- `cruzamento.mp4`: 1280×720, 30 fps, 2117 quadros. Pessoa em 7/7 e veículo em 7/7. No total das caixas: carro 67, pessoa 22, caminhão 19, moto 9, ônibus 2. A imagem é uma avenida reta, sem zebra. Ficou de fora da regra.
- `faixa.mp4`: 720×1280, 30 fps, 1655 quadros. Pessoa em 7/7 e veículo em 7/7. Carro 39, pessoa 16, moto 2. A câmera está parada na zebra. É o clipe da demo.

## Regra no clipe da faixa

Saída: `D:\citizentech\cv\video\farol\faixa_anotada.mp4`. 1655 quadros em 32,5 fps na RTX 2060.

A fase ficou `PEDESTRE` nos 56 segundos. Em 1385 quadros o detector marcou alguém com o pé dentro da zebra, e nesses 1385 a fase segurou `PEDESTRE`. Essa conferência usa o mesmo detector que alimenta a regra. Não é o teste de 60% contra um operador.

A troca para `ABRE VIA` não apareceu: a zebra não ficou livre o bastante para vencer o verde mínimo de 5 s. Este enquadramento também não tem uma segunda via.

## Segundo clipe, pessoas esperando (18/11)

`espera.mp4`, Pexels 2836277, 1280×720, 23,98 fps, 503 quadros, 21 s. Licença Pexels. Página: https://www.pexels.com/video/people-waiting-to-cross-the-street-on-the-pedestrian-lane-2836277/

A câmera está parada. A zebra fica vazia e os carros passam por ela. A fila espera na calçada, com o sinal de pedestre fechado.

Saída: `D:\citizentech\cv\video\farol\espera_anotada.mp4`. 503 quadros em 14,0 fps. A fase ficou `ABRE VIA` nos 21 segundos. Nenhum quadro teve pé de pessoa dentro da zebra. Num quadro conferido à mão, a tela lia faixa 0, via 8 e espera 10.

Os dois clipes juntos mostram as duas fases. Nenhum dos dois troca de fase no meio: no primeiro a zebra não esvazia, no segundo os carros não param.

## Terceiro clipe, cruzamento de 84 s (18/11)

`transito.mp4`, Pexels 20221532, 960×540, 29,97 fps, 2510 quadros, 84 s. Licença Pexels. Página: https://www.pexels.com/video/pedestres-e-transito-20221532/

A câmera está parada. Há zebra na frente e outra no cruzamento de trás. Saída: `D:\citizentech\cv\video\farol\transito_anotada.mp4`. 2510 quadros em 30,3 fps. A fase ficou `PEDESTRE` nos 84 segundos. Em 1948 quadros havia pé de pessoa dentro de uma das zebras, e nesses 1948 a fase segurou. Os intervalos sem gente foram menores que o verde mínimo de 5 s.

## Quarto clipe, esquina com uma zebra (18/11)

`esquina.mp4`, Pexels 17526711, 1366×720, 29,97 fps, 1646 quadros, 55 s. Licença Pexels. Página: https://www.pexels.com/video/a-city-street-with-people-crossing-the-street-17526711/

A câmera fica parada. A zebra da frente ocupa o meio do quadro, as pessoas aparecem de corpo inteiro e os carros passam ao lado, grandes o bastante. A calçada de espera fica fora da pintura. A faixa de trás, menor, ficou de fora do polígono.

Saída: `D:\citizentech\cv\video\farol\esquina_anotada.mp4`. 1646 quadros em 27,8 fps. A fase ficou `PEDESTRE` nos 55 segundos. Em 1569 quadros havia pé de pessoa dentro da zebra, e nesses 1569 a fase segurou. Os intervalos sem gente somam cerca de 2,6 s e não completam o verde mínimo de 5 s.

## Quinto clipe, Londres, a fase troca (18/11)

`londres.mp4`, Pexels 2863232, 960×540, 30 fps, 789 quadros, 26 s. Licença Pexels. Página: https://www.pexels.com/video/cars-stopping-at-a-pedestrian-crossing-2863232/

A câmera fica parada. Três pessoas atravessam no começo. Depois a faixa esvazia e os carros passam.

Saída: `D:\citizentech\cv\video\farol\londres_anotada.mp4`. 789 quadros em 29,9 fps. A fase ficou `PEDESTRE` nos primeiros 12 segundos e `ABRE VIA` nos 15 segundos seguintes. Em 203 quadros havia pé de pessoa na faixa, e nesses 203 a fase segurou. A troca acontece quando a faixa fica vazia por mais que o verde mínimo de 5 s.

## Relatório da entrega (19/11)

`docs/relatorio.html`, `README.md`, `docs/escopo.md`, `docs/roteiro_video.md`, `docs/viabilidade.md`, `docs/DATASETS.md` e `docs/erros.md` passaram a descrever o farol. Os números são os desta página. A comparação de 60% contra um operador continua por fazer e o relatório diz isso.

## Próximo passo

Marcar, segundo a segundo, a fase que um operador abriria e comparar com o programa.
