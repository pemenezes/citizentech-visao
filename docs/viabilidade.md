# Prova de viabilidade — farol da faixa

**Recomendação: o tema da entrega é o farol.** Data: 19/11/2026.

O grupo trocou a demo ao vivo de letras por uma fase de faixa lida em vídeo de internet. A câmera da prova é o arquivo. A regra foi combinada antes da medida e não foi alterada depois: verde mínimo de 5 segundos, via vazia de 3 segundos, espera máxima de 20 segundos, e pessoa na pintura fura o mínimo.

## O que foi medido

Peso `yolo26n.pt` do COCO, confiança 0,25, imagem 640, RTX 2060. O tempo inclui detecção, desenho e gravação do mp4.

- Londres, Pexels 2863232: 29,9 quadros por segundo. `PEDESTRE` 12 s e `ABRE VIA` 15 s.
- Espera, Pexels 2836277: 14,0 quadros por segundo. `ABRE VIA` os 21 s.
- Esquina, Pexels 17526711: 27,8. `PEDESTRE` os 55 s.
- Faixa, Pexels 25775484: 32,5. `PEDESTRE` os 56 s.
- Trânsito, Pexels 20221532: 30,3. `PEDESTRE` os 84 s.

## O que ficou em aberto

O piso de 60% dos quadros contra um operador não foi marcado. Esse número não entra como resultado. A contagem de pés na faixa usa o mesmo detector que alimenta a regra. Ela mostra que a fase segurou quando o detector viu alguém na pintura. Não substitui o operador.

## O que ficou de fora

Clipe sem zebra, câmera em movimento, tilt-shift e timelapse. Os arquivos ficam em `D:\citizentech\cv\video\farol` e fora do Git.
