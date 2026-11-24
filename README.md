

 # FACE ID

**Reconhecimento facial com verificação de uso de óculos em tempo real**

Projeto acadêmico da disciplina de Python que combina detecção de objetos com YOLO e reconhecimento facial com OpenCV para identificar pessoas cadastradas e verificar se estão usando óculos.

[Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
[Ultralytics YOLO](https://img.shields.io/badge/Ultralytics-YOLO-111F68?style=flat-square)
[OpenCV](https://img.shields.io/badge/OpenCV-YuNet%20%2B%20SFace-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
[CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-1F6FEB?style=flat-square)
[Pillow](https://img.shields.io/badge/Pillow-imagens-3E7BB6?style=flat-square)
[SQLite](https://img.shields.io/badge/SQLite-banco%20local-003B57?style=flat-square&logo=sqlite&logoColor=white)
[ONNX](https://img.shields.io/badge/ONNX-modelos-005CED?style=flat-square&logo=onnx&logoColor=white)


---

# Sumário

- [Sobre o projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Arquitetura](#arquitetura)
- [Estrutura de pastas](#estrutura-de-pastas)
- [Banco de dados](#banco-de-dados)
- [Conceitos de programação aplicados](#conceitos-de-programação-aplicados)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e configuração](#instalação-e-configuração)
- [Como usar](#como-usar)
- [Diferenciais](#diferenciais)
- [Limitações conhecidas](#limitações-conhecidas)
- [Melhorias futuras](#melhorias-futuras)

---

## Sobre o projeto

O **FACE ID** é uma aplicação desktop que acessa a webcam, detecta rostos, identifica a pessoa comparando o rosto com os usuários cadastrados em um banco SQLite e verifica, com um modelo YOLO treinado, se ela está usando óculos.

A proposta da disciplina era desenvolver um sistema de reconhecimento facial com YOLO. Neste projeto, o modelo foi direcionado para a detecção de óculos, o que permitiu adicionar uma camada extra de verificação: além de dizer **quem** está diante da câmera, o sistema compara a situação atual (com ou sem óculos) com a informação registrada no cadastro da pessoa.

### Problema abordado

Sistemas simples de identificação costumam responder apenas "quem é". O FACE ID também verifica se a aparência atual está **conforme o cadastro**, sinalizando divergências como uma pessoa cadastrada com óculos que aparece sem eles. Esse tipo de verificação é útil em cenários de controle de acesso ou de conferência de equipamentos de proteção, em que um acessório específico precisa estar presente.

---

## Funcionalidades

### Implementadas

| Funcionalidade | Descrição |

| Visualização da câmera em tempo real | Captura da webcam em 640x480 exibida dentro da interface. |
| Detecção facial | Localização de rostos com o modelo **YuNet** (OpenCV `FaceDetectorYN`). |
| Reconhecimento facial | Extração de características com **SFace** (OpenCV `FaceRecognizerSF`) e comparação por similaridade de cosseno com os usuários cadastrados. |
| Detecção de óculos | Modelo **YOLO** personalizado (`best.pt`) que detecta as classes `eyeglasses` e `sunglasses`. |
| Associação óculos e rosto | Uma detecção de óculos só é considerada quando o centro da caixa está na região superior (65%) do rosto detectado. |
| Verificação de conformidade | Compara o uso atual de óculos com o registro do usuário e informa o resultado na tela. |
| Cadastro de usuários | Tela própria com captura de foto pela webcam, detecção automática de óculos e gravação no banco. |
| Prevenção de cadastro duplicado | Bloqueia o cadastro quando o rosto já existe no banco (por similaridade) ou quando o nome já está registrado. |
| Marcação visual | Caixas e nomes desenhados sobre o vídeo: verde para pessoa reconhecida e vermelho para desconhecida. |
| Processamento em segundo plano | A inferência roda em uma thread separada para não travar a interface. |

### Estados de conformidade exibidos

| Situação | Mensagem na interface |

| Rosto não corresponde a nenhum cadastro | `Pessoa desconhecida` |
| Usuário cadastrado sem informação de óculos | `Cadastro sem informação de óculos` |
| Uso atual igual ao cadastro | `Situação conforme cadastro` |
| Cadastrado com óculos, aparece sem | `ATENÇÃO: ÓCULOS AUSENTES` |
| Cadastrado sem óculos, aparece com | `ATENÇÃO: ÓCULOS NÃO CADASTRADOS` |

### Planejadas ou em andamento

- Exibição de mais informações no painel de identificação (o painel "Status do sistema" ainda mostra um texto fixo).
- Remoção do módulo legado de janela de identificação, que não é mais utilizado pela aplicação.

---

## Tecnologias

| Tecnologia | Uso no projeto |
| --- | --- |
| **Python 3** | Linguagem principal. |
| **Ultralytics YOLO** | Carregamento e inferência do modelo de detecção de óculos (`best.pt`), executado em CPU com `imgsz=416` e confiança mínima de 0,40. |
| **OpenCV** | Captura da webcam, detecção facial (YuNet), reconhecimento facial (SFace), desenho das marcações e gravação das fotos. |
| **ONNX** | Formato dos modelos YuNet e SFace usados pelo OpenCV. |
| **CustomTkinter** | Interface gráfica moderna em tema escuro. |
| **Tkinter** | Componentes base (`Label`, `messagebox`) e agendamento com `after`. |
| **Pillow** | Conversão dos frames do OpenCV para exibição na interface. |
| **SQLite3** | Armazenamento local dos usuários cadastrados. |
| **threading / queue** | Execução da IA em paralelo à interface. |
| **Git LFS** | Versionamento dos pesos do modelo (`*.pt`). |

---

## Arquitetura

A aplicação é organizada em módulos com responsabilidades separadas: interface, visão computacional, persistência e utilidades.

Aplicação
│
├── Interface gráfica
│   ├── Interface principal (CustomTkinter)
│   └── interface_cadastro.py
│
├── Visão computacional (cam_ia.py)
│   ├── YOLO — Detecção de objetos (best.pt)
│   ├── YuNet — Detecção facial
│   └── SFace — Reconhecimento facial
│
└── Persistência de dados
    ├── banco.py — Gerenciamento de dados
    └── misterINFRA.db — Banco de dados SQLite


### Fluxo de reconhecimento

1. Ao ligar a câmera, os usuários são carregados do banco e as características faciais de cada foto cadastrada são extraídas com SFace.
2. A webcam é lida continuamente pela interface. A cada três frames, um frame é enviado para uma fila de tamanho 1, que sempre mantém apenas o mais recente.
3. Uma thread dedicada consome a fila e executa:
   - o YOLO para localizar óculos no frame;
   - o YuNet para localizar os rostos;
   - o SFace para comparar cada rosto com os cadastrados (limiar de similaridade de cosseno `0.363`).
4. Os resultados são gravados em um estado compartilhado protegido por `threading.Lock`.
5. A interface lê esse estado a cada 200 ms e atualiza nome, situação dos óculos e conformidade.

### Fluxo de cadastro

1. O usuário abre a tela de cadastro (a câmera do menu é desligada automaticamente).
2. Liga a câmera da tela de cadastro, que roda sem a thread de IA para economizar processamento.
3. Ao tirar a foto, o sistema detecta o rosto, verifica se ele já está cadastrado e identifica se a pessoa usa óculos.
4. A foto é salva na pasta `fotos/` com nome baseado em data e hora, e o cadastro é gravado no banco com nome, caminho da foto e uso de óculos.

---

## Estrutura de pastas

```text
.
├── Interfaces_inicial.py         # Ponto de entrada: janela principal e painel de monitoramento
├── interface_cadastro.py         # Tela de cadastro de usuários
├── cam_ia.py                     # Câmera, detecção facial, reconhecimento e detecção de óculos
├── banco.py                      # Acesso ao banco SQLite
├── funções.py                    # Utilidades (encerramento de janelas e câmera)
├── interface_gravação.py         # Módulo legado, não utilizado pela aplicação atual
├── misterINFRA.db                # Banco SQLite (criado automaticamente se não existir)
├── models/
│   └── best.pt                   # Pesos do modelo YOLO de detecção de óculos
├── modelos_reconhecimento/
│   ├── face_detection_yunet_2023mar.onnx
│   └── face_recognition_sface_2021dec.onnx
├── fotos/                        # Fotos dos cadastros (criada automaticamente)
├── .gitattributes                # Configuração do Git LFS para arquivos .pt
└── .gitignore
```


### Responsabilidade dos módulos

| Módulo | Responsabilidade |

| `Interfaces_inicial.py` | Monta a janela principal, alterna a câmera, abre o cadastro e atualiza o painel de identificação. |
| `interface_cadastro.py` | Coleta nome e foto, valida duplicidade e salva o usuário. |
| `cam_ia.py` | Carrega os modelos, gerencia a câmera e a thread de inferência e expõe as funções `ligar_camera`, `desligar_camera`, `detectar_uso_oculos` e `verificar_rosto_cadastrado`. |
| `banco.py` | Cria e migra a tabela `usuarios` e oferece funções de cadastro e consulta. |
| `funções.py` | Encerra janelas e libera a câmera. |

---

## Banco de dados

O banco é um arquivo SQLite local criado automaticamente pelo módulo `banco.py`.

**Tabela `usuarios`**

| Coluna | Tipo | Descrição |

| `idUsuario` | `INTEGER` (PK, autoincremento) | Identificador do usuário. |
| `nome` | `TEXT NOT NULL` | Nome do usuário. |
| `foto` | `TEXT` | Caminho da foto usada no reconhecimento. |
| `usa_oculos` | `INTEGER` | `1` para usa óculos, `0` para não usa, `NULL` quando não informado. |

Na inicialização, o módulo verifica as colunas existentes com `PRAGMA table_info` e adiciona `foto` e `usa_oculos` caso o banco tenha sido criado por uma versão anterior. Todas as consultas usam parâmetros (`?`), o que evita injeção de SQL.

---

## Conceitos de programação aplicados

O projeto segue um estilo **procedural e modular**, sem definição de classes próprias. Ainda assim, aplica conceitos importantes:

- **Modularização e separação de responsabilidades:** interface, visão computacional e persistência ficam em arquivos distintos.
- **Uso de bibliotecas orientadas a objetos:** widgets do CustomTkinter, objetos `VideoCapture`, `FaceDetectorYN`, `FaceRecognizerSF` e o modelo `YOLO` são instanciados e manipulados como objetos.
- **Programação concorrente:** padrão produtor e consumidor com `threading.Thread`, `queue.Queue(maxsize=1)`, `threading.Event` para parada e `threading.Lock` para acesso seguro ao estado compartilhado.
- **Programação orientada a eventos:** callbacks de botões e atualização periódica com `after()`.
- **Closures e `nonlocal`:** a tela de cadastro e a câmera mantêm estado em funções internas.
- **Persistência com SQL parametrizado** e migração simples de esquema.
- **Tratamento de exceções:** falhas na inferência e no encerramento de widgets não derrubam a aplicação.
- **Caminhos independentes do diretório de execução** com `pathlib.Path(__file__)`.

---

## Pré-requisitos

- Python 3 instalado
- Webcam
- Windows, pois a captura usa o backend `cv2.CAP_DSHOW` (DirectShow)
- Git LFS, para baixar o arquivo `best.pt`
- Arquivos de modelo:
  - `models/best.pt` (modelo YOLO de óculos treinado pelo grupo)
  - `modelos_reconhecimento/face_detection_yunet_2023mar.onnx`
  - `modelos_reconhecimento/face_recognition_sface_2021dec.onnx`

Os modelos YuNet e SFace estão disponíveis no repositório oficial [OpenCV Zoo](https://github.com/opencv/opencv_zoo).

---

## Instalação e configuração

**1. Clone o repositório com Git LFS**

```bash
git lfs install
git clone https://github.com/caua220407/ProjetoPython.git
cd ProjetoPython
```

**2. Crie e ative o ambiente virtual**

O `.gitignore` já ignora a pasta `AmbienteVirtual/`.

```bash
python -m venv AmbienteVirtual
AmbienteVirtual\Scripts\activate
```

**3. Instale as dependências**

```bash
pip install ultralytics opencv-python customtkinter pillow
```

> O OpenCV precisa ser da versão 4.8 ou superior para oferecer `FaceDetectorYN` e `FaceRecognizerSF`. `sqlite3`, `tkinter`, `threading` e `queue` fazem parte da biblioteca padrão do Python.

**4. Confira os modelos**

Verifique se `best.pt` está em `models/` e se os dois arquivos `.onnx` estão em `modelos_reconhecimento/`, conforme a [estrutura de pastas](#estrutura-de-pastas).

---

## Como usar

**Iniciar a aplicação**

```bash
python Interfaces_inicial.py
```

**Cadastrar uma pessoa**

1. Clique em **CADASTRAR PESSOA**.
2. Digite o nome do usuário.
3. Clique em **LIGAR CÂMERA** e posicione o rosto diante da webcam.
4. Clique em **TIRAR FOTO**. O sistema confere se o rosto já está cadastrado e informa se detectou óculos.
5. Clique em **SALVAR CADASTRO** e use a seta para voltar ao menu.

**Monitorar em tempo real**

1. No painel principal, clique em **LIGAR CÂMERA**.
2. O painel **IDENTIFICAÇÃO** mostra o nome da pessoa, se ela está usando óculos e a conformidade com o cadastro.
3. Clique em **DESLIGAR CÂMERA** para encerrar a captura.

### Parâmetros ajustáveis (`cam_ia.py`)

| Constante | Valor | Efeito |
| --- | --- | --- |
| `LIMIAR_RECONHECIMENTO` | `0.363` | Similaridade mínima para considerar dois rostos como a mesma pessoa. |
| `CONFIANCA_YOLO` | `0.40` | Confiança mínima para aceitar uma detecção de óculos. |

---

## Diferenciais

- **Dois níveis de verificação:** identidade e conformidade do uso de óculos com o cadastro.
- **Pipeline com três modelos** (YOLO, YuNet e SFace), cada um aplicado na tarefa em que é mais eficiente.
- **Associação espacial** entre óculos e rosto, o que evita contar óculos que estão fora do rosto.
- **Interface responsiva:** inferência em thread separada, fila que descarta frames antigos e processamento de um a cada três frames.
- **Validação de cadastro duplicado** por reconhecimento facial e não apenas por nome.
- **Banco autoinicializável** com migração de colunas para versões antigas.

---

## Limitações conhecidas

- O painel exibe o resultado do primeiro rosto processado. Com várias pessoas no quadro, apenas uma aparece no painel lateral.
- A captura usa `cv2.CAP_DSHOW`, recurso específico do Windows.
- A inferência roda apenas em CPU (`device="cpu"`).
- Os usuários são carregados ao ligar a câmera; um cadastro novo só é reconhecido depois de religá-la.
- Não há arquivo `requirements.txt` com versões fixadas.

---

## Melhorias futuras

- Adicionar `requirements.txt` com as versões das dependências.
- Exibir no painel todas as pessoas detectadas, e não apenas a primeira.
- Armazenar o vetor de características no banco para evitar reprocessar as fotos a cada inicialização.
- Permitir edição e exclusão de usuários pela interface.
- Registrar um histórico de identificações e alertas de não conformidade.
- Detectar a GPU automaticamente para acelerar a inferência.
- Tornar a captura de vídeo compatível com Linux e macOS.
- Reorganizar os módulos em classes para facilitar testes e manutenção.

--

Este projeto foi desenvolvido para a instituição "Anchieta".

