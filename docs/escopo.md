# Escopo

Status: **farol da faixa**, entrega de 19/11/2026. O relatório está em `docs/relatorio.html`.

## Grupo

- Anny Carolina — RM98295
- Henrique Lima — RM551528
- Pedro Menezes — RM97432

- Cidadão: pedestre na calçada e quem dirige a via que cruza a pintura.
- O que detectar: pessoa, carro, moto, ônibus e caminhão, com o YOLO26n público do COCO, sem treino novo.
- O que decidir: a fase `ABRE VIA` ou `PEDESTRE`, com três regiões desenhadas à mão (faixa, via e espera).
- Demo: um vídeo no lugar da câmera. A tela mostra a fase, as três contagens e as regiões. Sem voz e sem acionar um semáforo de rua.
- Tempos da regra: verde mínimo de 5 segundos, via vazia de 3 segundos, espera máxima de 20 segundos. Pessoa na pintura fura o mínimo.
- Clipes: licença Pexels, câmera parada, fora do Git, em `D:\citizentech\cv\video\farol`.
- Piso combinado: 60% dos quadros contra um operador. Essa comparação ficou por fazer. Os números do relatório são a fase produzida pela regra e os quadros por segundo medidos.
