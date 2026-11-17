# Visão computacional — CitizenTech (FIAP Global Solution 2026.2)

Componente de visão do produto CitizenTech. O tema é o alfabeto manual de Libras (soletração, não a língua inteira). O teste com o vídeo do celular está em `docs/viabilidade.md`. Ver `docs/escopo.md`.

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

O ambiente virtual já criado é `D:\citizentech\cv\envs\cv` (Python 3.12). PyTorch entra pelo índice CUDA 13.2, compatível com a RTX 2060 (Turing, sm_75) e com o driver instalado (CUDA 13.5).

## Verificação do ambiente (15/11/2026)

`scripts/check_env.py` viu a RTX 2060 (sm_75), CUDA 13.2 e um kernel executando na GPU. O teste `scripts/smoke_infer.py` carregou o `yolo26n.pt` (5,3 MB, em `D:\citizentech\cv\models`) e mediu **55,2 FPS** numa imagem sintética de 640 px. A webcam não abriu neste processo (DirectShow sem câmera utilizável). Pico de VRAM nesse teste: 52 MiB.

## Demo

O peso desta prova está em `D:\citizentech\cv\models\libras16_pedro2_yolo26n.pt` (YOLO26n ajustado com a segunda amostra do celular). O arquivo anterior, `libras16_pedro_yolo26n.pt`, permanece no mesmo diretório. A letra só entra na palavra depois de 8 quadros, numa janela de 12, com confiança de pelo menos 0,60. Abaixo disso a tela mostra "incerto".

```powershell
. D:\citizentech\cv\repo\scripts\env.ps1
python D:\citizentech\cv\repo\src\demo\app.py --origem 0 --reserva D:\citizentech\cv\video\prova_dedo.mp4
```

Sem câmera, o arquivo de reserva entra no lugar. Para só gravar, sem abrir janela:

```powershell
python D:\citizentech\cv\repo\src\demo\app.py --origem D:\citizentech\cv\video\prova_dedo.mp4 --sem-janela --saida D:\citizentech\cv\video\prova_dedo_anotado.mp4
```

Na janela: espaço acrescenta um espaço, backspace apaga, `x` limpa, `q` sai.

Em 15/11 esse vídeo de prova, montado com fotos públicas das letras D, E, D e O, produziu o texto `dedo`. Não é filmagem do Pedro. Em 16/11 o peso da segunda amostra repetiu o texto `dedo`. O vídeo anotado desta conferência ficou em `D:\citizentech\cv\video\prova_dedo_pedro2.mp4`.

## Vídeos do celular

Os clipes de 16/11 estão em `D:\citizentech\cv\video\pedro`. `scripts/preparar_pedro.py` separa o trecho estável, guarda uma amostra no treino e deixa o fim de cada clipe para o teste. Um arquivo novo, uma letra por nome, entra pelo mesmo script.
