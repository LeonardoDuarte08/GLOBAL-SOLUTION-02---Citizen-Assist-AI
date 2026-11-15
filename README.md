# Citizen Assist AI — Cidadania Digital

**Global Solution 2026.2 | FIAP | Pensamento Computacional e Automação com Python**

> **Escopo deste repositório:** implementação acadêmica em Python, executada no terminal, criada para atender aos requisitos da disciplina de Pensamento Computacional e Automação com Python. O **Citizen Assist AI completo** será desenvolvido posteriormente em **outro repositório**, com funcionalidades e interfaces adicionais. Este repositório é a base da entrega desta disciplina, não o produto final.

## Integrantes

| Integrante | RM |
| --- | --- |
| Leonardo Duarte | 569029 |
| Enzo | 569985 |

## 1. Público e problema

**Público-alvo:** cidadãos brasileiros que precisam de orientações acessíveis sobre cidadania digital, especialmente pessoas com pouca familiaridade com serviços digitais.

**Problema:** informações sobre golpes virtuais, compras online e serviços públicos digitais estão espalhadas em diferentes canais. Isso dificulta a identificação de orientações confiáveis e pode expor o cidadão a fraudes.

**Proposta:** um assistente simples, em Python, que recebe dúvidas em texto livre, procura orientações em uma base JSON, informa as fontes consultadas e permite verificar links por meio da API Google Safe Browsing.

O programa **não é um canal oficial** e não substitui órgãos públicos, instituições financeiras, serviços de emergência ou profissionais especializados.

## 2. Funcionalidades desta versão

- Fazer perguntas em texto livre e obter uma orientação cadastrada, com fonte, data de verificação e nível de confiança.
- Navegar por categorias e selecionar orientações numeradas.
- Consultar uma URL na **Google Safe Browsing API v4** para verificar se há correspondência com ameaças conhecidas.
- Recusar perguntas com **@** ou **8 ou mais dígitos**, como proteção básica contra inserção de dados pessoais.
- Registrar atendimentos em JSON e gerar indicadores de uso.
- Exportar atendimentos para CSV.
- Receber avaliação de facilidade de uso de **1 a 5** ao encerrar.

**Importante:** uma URL sem correspondência nas listas do Google **não é necessariamente segura**. A verificação utiliza um serviço externo e depende de conexão com a internet e de uma chave válida.

## 3. Categorias e base de conhecimento

O arquivo `data/base_conhecimento.json` contém **10 orientações**, com no mínimo 3 palavras-chave por orientação, organizadas em três categorias:

| Categoria | Quantidade | Exemplos |
| --- | ---: | --- |
| Segurança Digital | 4 | Phishing, golpe Pix, autenticação em duas etapas e conta invadida |
| Direitos do Consumidor | 3 | Reclamação de compras, arrependimento e produto não entregue |
| Serviços Públicos Digitais | 3 | Conta gov.br, Carteira de Trabalho Digital e documentos digitais |

Cada orientação possui os campos: `id`, `categoria`, `titulo`, `palavras_chave`, `resposta`, `documentos`, `onde`, `fonte` e `verificado_em`. O conteúdo deve ser revisto sempre que houver mudanças nos procedimentos oficiais.

## 4. Organização dos arquivos

```text
GLOBAL-SOLUTION-02---Citizen-Assist-AI/
├── main.py
├── orientacao.py
├── base_conhecimento.py
├── assistente.py
├── validador_url.py
├── teste_busca.py
├── README.md
├── .gitignore
└── data/
    └── base_conhecimento.json
```

Os arquivos `data/historico.json`, `data/avaliacoes.json` e `data/atendimentos.csv` são gerados durante o uso e **não devem conter informações reais de identificação pessoal**. O arquivo `.env` é local e não deve ser publicado.

### Orientação a objetos

| Classe | Responsabilidade |
| --- | --- |
| `Orientacao` | Armazenar e apresentar uma orientação da base JSON |
| `BaseConhecimento` | Carregar orientações, listar categorias, pontuar e buscar resultados |
| `Assistente` | Realizar atendimentos, registrar histórico, calcular indicadores e exportar CSV |

Há **composição**: o objeto `Assistente` contém uma `BaseConhecimento`, que contém uma lista de objetos `Orientacao`. A verificação de URLs está organizada separadamente no arquivo `validador_url.py`.

## 5. Como executar

**Requisitos:** Python 3, Git (para clonar o projeto) e internet apenas para consultar o Google Safe Browsing. Não são necessárias bibliotecas externas para a versão atual.

Clone o repositório:

```bash
git clone https://github.com/LeonardoDuarte08/GLOBAL-SOLUTION-02---Citizen-Assist-AI.git
cd GLOBAL-SOLUTION-02---Citizen-Assist-AI
```

No Windows, execute:

```powershell
py main.py
```

Em ambientes onde o comando `python` esteja disponível:

```bash
python main.py
```

**Menu principal:**

```text
1 - Fazer uma pergunta
2 - Navegar por categorias
3 - Verificar URL suspeita
4 - Visualizar indicadores
5 - Exportar atendimentos
0 - Sair
```

O assistente de perguntas e categorias funciona sem a chave da API. A opção de verificar URL exige a configuração descrita a seguir.

### Configuração da API (sem publicar a chave)

1. Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/).
2. Ative a **Safe Browsing API** e gere uma chave, restringindo-a à API utilizada.
3. Na raiz do projeto, crie um arquivo local chamado `.env` contendo:

```dotenv
GOOGLE_SAFE_BROWSING_KEY=COLOQUE_SUA_CHAVE_AQUI
```

4. Execute novamente `py main.py` e utilize a opção 3.

A implementação também aceita a variável de ambiente `GOOGLE_SAFE_BROWSING_KEY`; caso ela esteja definida, terá prioridade sobre o arquivo `.env`. **Nunca publique uma chave real no código, em prints, no README ou no histórico do Git.** O `.gitignore` protege o arquivo `.env`, mas é preciso conferir os arquivos antes de cada commit.

A integração atual usa o endpoint `threatMatches:find` da **Safe Browsing API v4**, com requisição POST e resposta JSON. É uma integração acadêmica e poderá ser atualizada no projeto futuro.

## 6. Como a busca funciona

A busca é **baseada em regras, não em uma IA generativa**. As perguntas são comparadas com os títulos e as palavras-chave de cada orientação.

1. A função `normalizar()` converte o texto para minúsculas e remove acentos e sinais de pontuação definidos no código.
2. Cada palavra-chave cadastrada soma **3 pontos** quando todas as suas palavras estão presentes na pergunta, mesmo com outras palavras entre elas.
3. Cada palavra **distinta** da pergunta, com 4 letras ou mais, encontrada no título soma **1 ponto**.
4. A função `buscar()` retorna uma lista de **tuplas** `(pontos, orientacao)`, ordenada da maior para a menor pontuação.

| Pontuação | Resultado |
| --- | --- |
| 6 pontos ou mais | Confiança **ALTA** |
| 3 a 5 pontos | Confiança **MÉDIA** |
| Menos de 3 pontos | Orientação não encontrada |

O programa exibe a melhor orientação e até duas alternativas quando disponíveis.

**Melhoria realizada nos testes iniciais:** a busca inicialmente exigia uma expressão exata. Por exemplo, `cancelar compra` não encontrava `Quero cancelar uma compra online`. A regra foi alterada para permitir palavras intermediárias. Essa mudança será demonstrada na apresentação técnica.

## 7. Histórico, indicadores e privacidade

Cada atendimento registra data, origem (pergunta ou categoria), texto da pergunta quando permitido, ID da orientação, resultado encontrado, indicação de ajuda, tentativas e tempo em segundos.

Os indicadores incluem:
- Percentual de respostas encontradas;
- Percentual de atendimentos marcados como úteis;
- Tempo médio por atendimento;
- Média de tentativas;
- Dúvidas sem solução;
- Média das avaliações de facilidade de uso (1 a 5).

O CSV é exportado com `csv.DictWriter` para `data/atendimentos.csv`.

**Privacidade:** o assistente não solicita nome, CPF, telefone ou e-mail. Perguntas contendo `@` ou 8 ou mais dígitos são recusadas e não são registradas. Esse filtro é **limitado** e não identifica todos os dados sensíveis; URLs enviadas à API são compartilhadas com o serviço externo. Não insira URLs com senhas, tokens, dados pessoais ou informações confidenciais.

## 8. Testes realizados e testes pendentes

**Testes iniciais de desenvolvimento realizados:** execução do menu, carregamento das 10 orientações, busca por palavras-chave, navegação por categorias, consulta de URL via API, recusa de entrada com CPF, geração de histórico, indicadores, exportação CSV e avaliação de facilidade.

Esses testes iniciais **não substituem** a validação obrigatória com usuários externos.

**Teste exigido pela disciplina — pendente de consolidação:**
- Testar com **pelo menos 3 pessoas de fora da equipe**;
- Somar **10 atendimentos ou mais**;
- Registrar os indicadores consolidados e dúvidas sem solução, sem guardar nomes nem dados pessoais;
- Descrever pelo menos uma melhoria feita a partir desse teste.

**Resultados dos testes com usuários externos:** a preencher após os testes.

## 9. Limitações e decisões técnicas

- A resposta está limitada aos conteúdos cadastrados no JSON; o programa não cria orientações novas.
- A pontuação por palavras pode gerar correspondências incorretas ou não reconhecer algumas formas de escrever uma pergunta.
- As fontes precisam ser revisadas periodicamente.
- A integração do Google depende de internet, da disponibilidade da API e de uma chave válida.
- O Google Safe Browsing indica correspondências com ameaças conhecidas, **não certifica a segurança de sites**.
- O bloqueio de dados pessoais é básico e necessita evolução.
- A interface é propositalmente **somente terminal**, conforme o foco desta disciplina.

A escolha de manter as classes e a lógica simples permite demonstrar os conceitos de orientação a objetos, listas, dicionários, arquivos, condicionais e laços de repetição estudados nas aulas.

## 10. ODS relacionados

- **ODS 4 — Educação de Qualidade:** acesso a orientações claras e promoção de educação digital.
- **ODS 10 — Redução das Desigualdades:** facilitar o acesso à informação para cidadãos com diferentes níveis de familiaridade digital.
- **ODS 16 — Paz, Justiça e Instituições Eficazes:** direcionamento a serviços e fontes públicas confiáveis.

## 11. Fontes de consulta

As fontes específicas e as datas de verificação de cada orientação estão no arquivo `data/base_conhecimento.json`.

Principais referências:
- [Portal gov.br](https://www.gov.br/)
- [Banco Central do Brasil](https://www.bcb.gov.br/)
- [Consumidor.gov.br](https://www.consumidor.gov.br/)
- [Procon-SP](https://www.procon.sp.gov.br/)
- [Google Safe Browsing — documentação](https://developers.google.com/safe-browsing/)

## 12. Vídeo técnico e entrega da disciplina

**Vídeo técnico (YouTube não listado):** link a adicionar após a gravação.

O vídeo deverá ter de **5 a 8 minutos** e demonstrar: base JSON, dicionários e tuplas, classes e composição, normalização e pontuação, execução de cenários válidos/inválidos, bloqueio de dados pessoais, navegação, inclusão de palavra-chave ao vivo, histórico, CSV, indicadores, decisão técnica e limitação. **Leonardo e Enzo devem participar da explicação.**

A entrega no portal FIAP é um arquivo `.txt` contendo o nome do assistente, público atendido, integrantes e RMs, link do repositório e link do vídeo.

**Prazo informado no enunciado:** 19/11/2026, às 23h59.

## 13. Continuidade do projeto

Este repositório representa **somente a entrega de Pensamento Computacional e Automação com Python**. Depois da entrega, a equipe pretende ampliar o Citizen Assist AI em **outro repositório**, reunindo recursos adicionais do projeto completo.

Possíveis evoluções incluem uma interface gráfica/web, integração com outras disciplinas e aperfeiçoamento da análise de URLs. Esses itens **não fazem parte da implementação atual**.

---

**Citizen Assist AI — Global Solution 2026.2 — FIAP**
