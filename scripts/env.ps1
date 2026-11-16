# Variáveis desta sessão. Executar no início de cada terminal:
#   . D:\citizentech\cv\repo\scripts\env.ps1
# Tudo que pode ser redirecionado fica no disco D: (HDD).
# Python, Git e o driver NVIDIA permanecem onde o Windows os instalou (C:).

$root = "D:\citizentech\cv"
$env:HF_HOME               = "$root\cache\hf"
$env:TORCH_HOME            = "$root\cache\torch"
$env:PIP_CACHE_DIR         = "$root\cache\pip"
$env:YOLO_CONFIG_DIR       = "$root\cache\ultralytics"
$env:TMP                   = "$root\cache\tmp"
$env:TEMP                  = "$root\cache\tmp"
$env:CV_DATA_DIR           = "$root\data"
$env:KAGGLE_CONFIG_DIR     = "$root\cache\kaggle"
$env:FIFTYONE_DATABASE_DIR = "$root\cache\fiftyone"
$env:PYTHONUTF8            = "1"
$env:PYTHONNOUSERSITE      = "1"

$venvPy = "$root\envs\cv\Scripts\python.exe"
if (Test-Path $venvPy) {
    $env:VIRTUAL_ENV = "$root\envs\cv"
    $env:PATH = "$root\envs\cv\Scripts;" + $env:PATH
}

Write-Host "CV root: $root"
Write-Host "Python:  $venvPy"
Write-Host "HF_HOME: $env:HF_HOME"
