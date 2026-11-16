# Erros no teste (peso YOLO26n, melhor época da rodada de 40)

Teste de 449 fotos. Limiar 0,25. Contagem feita em 16/11 com `runs/yolo26n_e40/weights/best.pt`.

| Tipo | Quantidade |
| --- | ---: |
| Sem caixa | 23 |
| Letra trocada | 10 |

Sem caixa por letra: N 16 (todas as fotos de N do teste), I 4, M 2, U 1.

Trocas: U lida como V em 8 fotos, U lida como R em 1, V lida como W em 1.

Doze exemplos anotados estão em `D:\citizentech\cv\runs\erros_e40`. O que as imagens mostram:

- I e M que sumiram continuam no cômodo da claraboia, com a mão inteira. O modelo não marca caixa nem com confiança baixa. Não é oclusão.
- N do teste é outro enquadramento: a mão entra de cima, dedos para baixo, bem perto da lente. As 16 fotos dessa letra ficaram sem caixa. O treino quase não viu esse ângulo.
- U e V se confundem porque a diferença é dedos juntos ou separados. W entra na mesma família.

Causa provável e correção: incluir no treino o ângulo de cima das letras N, I e M, e mais pares U/V/W com as duas mãos. O dataset público não separa pessoas, então o vídeo do celular continua sendo o teste que importa.
