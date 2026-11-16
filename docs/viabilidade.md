# Prova de viabilidade — alfabeto manual de Libras

**Recomendação: NO-GO para congelar o tema agora. O plano B (cédulas) não entra ainda.**

O critério combinado era acerto de pelo menos 60% num vídeo do Pedro, depois de misturar uma amostra dele no treino. Esse vídeo não existe. O número alto abaixo é da mesma mão e do mesmo cômodo do dataset público, não do celular.

Status: tema **não aprovado**. `docs/escopo.md` não foi congelado.

Data da verificação: 15/11/2026.

## O que o Pedro já respondeu

- Teste de campo com outra pessoa: por enquanto só ele sinaliza.
- Gravação: câmera do celular, mão direita.
- Demo: só texto na tela. Sem voz.

## Letras com movimento

Fonte lida: artigo “O alfabeto manual como recurso…” (doi:10.22456/2236-6385.129250). O alfabeto manual da Libras tem 27 sinais. Têm movimento apenas **H, J, K, X, Y e Z**. As estáticas são as outras, inclusive o Ç: cerca de 21, não 15.

A página do INES confirma que existe material oficial do alfabeto, mas o texto público que abri não descreve o movimento letra a letra.

## Dataset que a decisão apontou (4.410 imagens)

Página: [Alfabeto em libras, v1, validaes mos](https://universe.roboflow.com/validaes-mos/alfabeto-em-libras/dataset/1).

- Existe. Versão 1, sem aumento de dados: **4.410** imagens, divisão publicada **3.087 / 882 / 441**.
- A licença **não aparece** nessa página.
- As 15 classes publicadas num espelho do mesmo tamanho ([Globaltec ByLab](https://universe.roboflow.com/globaltec-bylab/alfabeto-em-libras-usm1h)) são `a b c d e i l m n o r s u v w`.

O conjunto baixado para o D: é o repositório [biankatpas/Brazilian-Sign-Language-Alphabet-Dataset](https://github.com/biankatpas/Brazilian-Sign-Language-Alphabet-Dataset) (MIT no arquivo `LICENSE` do código). O próprio README e o XML dizem que as fotos vieram do [ASL Alphabet no Kaggle](https://www.kaggle.com/datasets/grassknoted/asl-alphabet), cuja licença publicada é **GPL-2**. Os caminhos dentro do XML são `asl_alphabet_train`. Contagem conferida no disco: **4.410** caixas com imagem (2 XML sem JPG), 200×200, uma caixa por foto.

Não é um alfabeto de Libras fotografado no Brasil. São fotos de ASL das 15 letras cuja forma a autora considerou igual à da Libras. Faltam letras estáticas que diferem da ASL, entre elas **F, G, P, Q e T**, além do Ç e das letras com movimento.

### Balanceamento (caixas)

| Letra | Caixas | Letra | Caixas |
| --- | ---: | --- | ---: |
| a | 540 | l | 150 |
| b | 589 | m | 197 |
| c | 502 | n | 156 |
| d | 504 | o | 150 |
| e | 609 | r | 154 |
| i | 260 | s | 151 |
|  |  | u, v, w | 150 cada |

E tem cerca de quatro vezes o volume de L, O, R, S, U, V e W.

### Amostra visual (uma foto do meio de cada letra)

Abri A, E, M, L, R e V. Não há rosto. É a mesma mão, no mesmo cômodo (claraboia e parede branca na maior parte). A e E, nessas fotos de 200 px, parecem punhos fechados muito parecidos. Cerca de 2% das caixas encostam na borda; a área mediana da caixa é 31% da imagem.

Divisão usada no treino curto, contígua por número do arquivo dentro de cada letra: treino 3.083, validação 878, teste 449. Isso evita sortear fotos vizinhas, mas **não separa pessoas**: só existe uma pessoa.

## Outros conjuntos de Libras olhados e não baixados

- [projeto libras, gomes](https://universe.roboflow.com/gomes-project/projeto-libras): a versão antiga v8 tem 212 imagens (bate com “cerca de 213”). A versão atual tem 2.038 imagens e mistura letras com sinais de palavra (Ajuda, Banheiro, Vacina). Licença não publicada na página.
- [Alfabeto em libras, libras-gglhu](https://universe.roboflow.com/libras-gglhu/alfabeto-em-libras-qrvnw-te3gf): 1,7 mil imagens, 22 classes, texto diz “letras que não apresentam movimento”. Inclui F, G, P, Q, T e também K, que o artigo cita como letra com movimento. Licença não publicada. Exige chave do Roboflow, que não está no ambiente.
- [Alfabeto de Libras, DigoTKT](https://universe.roboflow.com/digotkt/alfabeto-de-libras): 1,6 mil imagens, 17 classes, licença **CC BY 4.0**. Também sem F, P, Q, T.

## Plano B — cédulas

- [Cédulas de real brasileiro, Roboflow](https://universe.roboflow.com/vision-fbche/cedulas-de-real-brasileiro): 245 imagens, 6 classes (2, 5, 10, 20, 50, 100). Não tem R$ 200. Licença não publicada. O mAP de 99,5% é o número deles, num conjunto pequeno.
- [Cédulas do Real, Kaggle](https://www.kaggle.com/datasets/karenalmeida340/cdulas-do-real): licença **MIT**, notas de 2 a 200, cerca de 9,2 GB, organizado por pastas (classificação, não caixas). Não baixei.

## Treino curto (feito)

YOLO26n, 5 épocas, imagem 640, lote 16, cache na RAM, semente 42, workers 0 (no Windows o lote com workers travou o processo). Pesos iniciais: `D:\citizentech\cv\models\yolo26n.pt`. Ultralytics 8.4.214, licença **AGPL-3.0** no `LICENSE` do pacote. Ollama sem modelo na GPU. VRAM de treino cerca de 2,4 GB. Tempo acumulado na `results.csv`: **369 s** (época 1: 82 s). Saída: `D:\citizentech\cv\runs\viabilidade\yolo26n_e5`.

Validação (878 fotos, mesma pessoa): na época 5, precisão 0,922, recall 0,949, mAP@50 0,979, mAP@50-95 0,832.

### Teste separado (449 fotos finais de cada letra, ainda a mesma pessoa)

| | Precisão | Recall | mAP@50 | mAP@50-95 |
| --- | ---: | ---: | ---: | ---: |
| Todas | 0,915 | 0,835 | 0,956 | 0,796 |

Recall por letra no teste (uma mão por foto; o recall é o acerto da letra):

| Letra | Fotos | Recall | Letra | Fotos | Recall |
| --- | ---: | ---: | --- | ---: | ---: |
| a | 54 | 1,00 | n | 16 | **0,00** |
| b | 60 | 0,85 | o | 15 | 1,00 |
| c | 50 | 1,00 | r | 17 | 1,00 (precisão 0,58) |
| d | 52 | 1,00 | s | 16 | **0,28** |
| e | 62 | 1,00 | u | 15 | **0,39** |
| i | 26 | 1,00 | v | 15 | 1,00 |
| l | 15 | 1,00 | w | 15 | 1,00 |
| m | 21 | 1,00 |  |  |  |

N não foi recuperada nenhuma vez nessas 16 fotos. Com limiar 0,25, 13 delas nem geram caixa: a foto de treino `N_404` é um punho de frente, e a de teste `N_1141` é outro ângulo, dedos para baixo. A divisão por número de arquivo separou vistas diferentes, não só fotos vizinhas. S e U ficam com recall 0,28 e 0,39. R acerta as suas fotos, mas a precisão cai para 0,58. L tem mAP@50-95 de 0,34: a letra é achada, a caixa fica frouxa. A matriz está em `runs/viabilidade/yolo26n_e5_teste`.

Inferência em arquivo, lote 1, 640 px, 100 fotos do teste depois de 10 de aquecimento: **49,6 FPS**, 20 ms por foto. Isso não inclui abrir a câmera. Pico de VRAM nessa medição: 506 MiB.

## Rodada de 40 épocas (16/11, de manhã)

Parou na época 22 por paciência 15. O melhor ponto da validação foi restaurado: precisão 0,978, recall 0,939, mAP@50 0,990, mAP@50-95 0,830, em 0,414 h. Saída: `D:\citizentech\cv\runs\yolo26n_e40`.

No teste de 449 fotos, esse peso ficou em mAP@50 0,952 e mAP@50-95 0,775. O recall geral subiu de 0,835 para 0,871. S passou de recall 0,28 para 1,00. N continua em 0. U continua perto de 0,38. A demo segue com o peso das 5 épocas (`models\libras15_yolo26n.pt`), porque o mAP mais estrito do teste não melhorou.

## Baseline sem treino nas letras

O mesmo YOLO26n pré-treinado no COCO, sem fine-tuning, rodou nas 449 fotos de teste (`scripts/baseline_coco.py`). Em **0** fotos o nome da classe coincidiu com a letra. Em 410 fotos houve alguma caixa: 407 vezes a classe `person`. O treino customizado é o que cria as letras.

## Demo já exercitada

Um vídeo montado só com fotos de teste de D, E, D e O (`D:\citizentech\cv\video\prova_dedo.mp4`) passou pela demo. O texto acumulado foi `dedo`. A saída anotada está em `D:\citizentech\cv\video\prova_dedo_anotado.mp4`. No trecho final a tela marcou cerca de 42 FPS de processamento. O começo marca menos porque a medida ainda inclui a carga do modelo.

## O que falta para um GO

Um vídeo do celular, mão direita, sem rosto, com as letras paradas. Aí entra uma amostra pequena no treino e o resto fica de fora, para medir o acerto de verdade. Se esse acerto ficar abaixo de 60%, o plano B passa a valer.
