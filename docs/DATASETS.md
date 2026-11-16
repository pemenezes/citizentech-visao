# Datasets

Conferido em 15/11/2026 e usado no treino de 16/11. As imagens ficam em `D:\citizentech\cv\data` e não entram no Git.

## Conjunto usado no treino

Repositório: [biankatpas/Brazilian-Sign-Language-Alphabet-Dataset](https://github.com/biankatpas/Brazilian-Sign-Language-Alphabet-Dataset)

O arquivo `LICENSE` desse repositório é MIT e cobre o software. As fotos, segundo o README e o caminho dentro dos XML (`asl_alphabet_train`), vêm do [ASL Alphabet no Kaggle](https://www.kaggle.com/datasets/grassknoted/asl-alphabet), com licença publicada **GPL-2**. Há também o registro [Mendeley 10.17632/k4gs3bmx5k.5](https://data.mendeley.com/datasets/k4gs3bmx5k/5). A página do Mendeley descreve o mesmo recorte e não exibiu uma licença diferente no texto lido.

Não é um alfabeto fotografado com sinalizantes brasileiros. São 15 letras de ASL cuja forma a autora tratou como igual à da Libras: `a b c d e i l m n o r s u v w`. Faltam, entre as estáticas que diferem da ASL, F, G, P, Q e T.

Contagem no disco: 4.411 JPG e 4.412 XML. Caixas com imagem correspondente: **4.410**. Todas 200×200, uma caixa por foto. Não há rosto nas amostras abertas. O fundo é o mesmo cômodo na maior parte.

| Letra | Caixas | Letra | Caixas |
| --- | ---: | --- | ---: |
| a | 540 | l | 150 |
| b | 589 | m | 197 |
| c | 502 | n | 156 |
| d | 504 | o | 150 |
| e | 609 | r | 154 |
| i | 260 | s | 151 |
|  |  | u, v, w | 150 cada |

Divisão contígua pelo número do arquivo, dentro de cada letra: treino 3.083, validação 878, teste 449. Os números altos de N caem no teste e mostram outro ângulo. Cópia YOLO: `D:\citizentech\cv\data\processed\libras15_passos`.

O espelho do Roboflow com 4.410 imagens e a mesma divisão 3.087/882/441 é [validaes mos, v1](https://universe.roboflow.com/validaes-mos/alfabeto-em-libras/dataset/1). A licença não aparece nessa página. Não foi baixado.

## Outros conjuntos vistos e não usados no treino

- [projeto libras](https://universe.roboflow.com/gomes-project/projeto-libras): a versão v8 tem 212 imagens. A versão atual mistura letras e sinais de palavra. Licença não publicada.
- [Alfabeto em libras, libras-gglhu](https://universe.roboflow.com/libras-gglhu/alfabeto-em-libras-qrvnw-te3gf): cerca de 1,7 mil imagens e 22 classes, texto diz letras sem movimento. Licença não publicada. Exige chave do Roboflow.
- [Alfabeto de Libras, DigoTKT](https://universe.roboflow.com/digotkt/alfabeto-de-libras): cerca de 1,6 mil imagens, 17 classes, licença **CC BY 4.0**.

## Plano B, não baixado

- [Cédulas de real brasileiro](https://universe.roboflow.com/vision-fbche/cedulas-de-real-brasileiro): 245 imagens, seis valores, sem R$ 200. Licença não publicada.
- [Cédulas do Real no Kaggle](https://www.kaggle.com/datasets/karenalmeida340/cdulas-do-real): licença **MIT**, notas de 2 a 200, cerca de 9,2 GB, pastas por valor.
