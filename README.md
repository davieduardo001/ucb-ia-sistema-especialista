# 🏥 Sistema Especialista para Diagnóstico de Doenças Tropicais

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)

## 📋 Sumário

---

## 🎯 Sobre o Projeto

Este projeto consiste em um **Sistema Especialista** desenvolvido para auxiliar no diagnóstico diferencial de doenças tropicais, utilizando técnicas de Inteligência Artificial baseadas em conhecimento. O sistema foi desenvolvido como trabalho acadêmico da disciplina de Inteligência Artificial, abordando os seguintes tópicos:

- ✅ História e fundamentos da IA
- ✅ Métodos de resolução de problemas
- ✅ Representação do conhecimento
- ✅ Tratamento de incertezas
- ✅ Introdução à aprendizagem de máquina

### 🎓 Contexto Acadêmico

**Disciplina:** Inteligência Artificial  
**Instituição:** Universidade Católica de Brasília
**Período:** Setimo Periodo
**Tipo:** AT1 – Trabalho em Grupo

---

## 📚 Fundamentação Teórica

### Sistemas Especialistas

Sistemas Especialistas são programas de computador que emulam a capacidade de tomada de decisão de um especialista humano em um domínio específico. Surgidos na década de 1970 com projetos pioneiros como MYCIN (Stanford, 1975), esses sistemas representam uma das primeiras aplicações práticas bem-sucedidas da Inteligência Artificial.

#### Componentes Clássicos:

1. **Base de Conhecimento**: Armazena fatos e regras sobre o domínio
2. **Motor de Inferência**: Processa o conhecimento para chegar a conclusões
3. **Interface do Usuário**: Facilita a comunicação entre usuário e sistema
4. **Módulo de Explicação**: Justifica as conclusões obtidas

### Escolha do Domínio: Diagnóstico Médico

O diagnóstico médico foi escolhido por ser um problema clássico de sistemas especialistas, que envolve:

- **Conhecimento estruturado**: Sintomas, doenças e suas relações
- **Raciocínio sob incerteza**: Sintomas podem variar em intensidade
- **Múltiplas hipóteses**: Várias doenças podem compartilhar sintomas
- **Alto valor prático**: Potencial de auxílio em triagens e áreas remotas

---

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────┐
│                 INTERFACE DO USUÁRIO                │
│              (Streamlit Web Interface)              │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│              MÓDULO DE AQUISIÇÃO                    │
│         (Entrada de Sintomas: Escala 1-5)           │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│              MOTOR DE INFERÊNCIA                    │
│    (Algoritmo de Proximidade - Dist. Manhattan)     │
│                                                     │
│  • Cálculo de Distâncias                            │
│  • Agregação de Pontuações                          │
│  • Normalização de Confiança                        │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│              BASE DE CONHECIMENTO                   │
│           (sintomas_doencas.csv)                    │
│                                                     │
│  • Perfis de Doenças                                │
│  • Intensidades de Sintomas                         │
│  • Relações Sintoma-Doença                          │
└─────────────────────────────────────────────────────┘
```

---

## 💻 Instalação e Execução

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório** (ou extraia os arquivos do projeto):

```bash
git clone [URL_DO_REPOSITORIO]
cd sistema-especialista-medico
```

2. **Crie um ambiente virtual** (recomendado):

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**:

```bash
pip install streamlit pandas numpy matplotlib seaborn
```

Ou usando o arquivo de requisitos:

```bash
pip install -r requirements.txt
```

4. **Certifique-se de que o arquivo `sintomas_doencas.csv` está presente** no diretório raiz do projeto.

5. **Execute a aplicação**:

```bash
streamlit run app.py
```

6. **Acesse no navegador**: O Streamlit abrirá automaticamente em `http://localhost:8501`

---

## 📊 Base de Conhecimento

### Formato do Arquivo CSV

A base de conhecimento é armazenada em formato CSV com a seguinte estrutura:

```csv
doenca,febre,dor_cabeca,dor_articular,dor_muscular,manchas_pele,dor_olhos,tosse,nausea_vomito,dor_garganta,congestao_nasal
Dengue,alta,forte,leve,forte,frequente,forte,ausente,frequente,ausente,ausente
Zika,baixa,leve,moderada,leve,muito_frequente,leve,ausente,raro,ausente,ausente
Chikungunya,alta,leve,muito_forte,leve,frequente,leve,ausente,raro,ausente,ausente
Gripe,moderada,moderada,ausente,forte,ausente,ausente,forte,raro,forte,frequente
...
```

### Escala de Intensidade

Cada sintoma é classificado usando uma escala qualitativa que é convertida para valores numéricos:

| Termo Qualitativo      | Valor Numérico |           Significado      |
|------------------------|----------------|----------------------------|
| Ausente                | 1              | Sintoma não presente       |
| Leve/Baixo/Raro        | 2              | Manifestação mínima        |
| Moderado               | 3              | Manifestação média         |
| Alto/Forte/Frequente   | 4              | Manifestação significativa |
| Muito Alto/Muito Forte | 5              | Manifestação extrema       |

### Representação do Conhecimento

O conhecimento é representado através de **perfis sintomáticos** para cada doença, utilizando uma abordagem inspirada em **Lógica Fuzzy**. Cada doença é caracterizada por um vetor de intensidades:

```
Dengue = [febre: 5, dor_cabeça: 4, dor_articular: 5, ...]
```

Esta representação permite:
- Modelar a **gradação** dos sintomas (não apenas presente/ausente)
- Capturar a **variabilidade** individual nas manifestações clínicas
- Facilitar o **cálculo de similaridade** entre casos

---

## ⚙️ Motor de Inferência

### Algoritmo de Raciocínio

O sistema utiliza um algoritmo de **Pontuação por Proximidade** baseado na **Distância de Manhattan**, implementando os seguintes passos:

#### 1. Cálculo de Distância por Sintoma

Para cada sintoma *i*:

```
distância(i) = |valor_paciente(i) - valor_esperado_doença(i)|
```

#### 2. Conversão em Pontuação

```
pontos(i) = 4 - distância(i)
```

Onde:
- Distância = 0 → 4 pontos (match perfeito)
- Distância = 4 → 0 pontos (extremos opostos)

#### 3. Agregação Total

```
pontuação_total = Σ pontos(i) para todos os sintomas
```

#### 4. Normalização de Confiança

```
confiança(%) = (pontuação_total / pontuação_máxima_possível) × 100
```

### Pseudocódigo

```python
FUNÇÃO diagnosticar(sintomas_paciente):
    Para cada doença na base_conhecimento:
        pontuação_total = 0
        
        Para cada sintoma:
            diferença = ABS(sintomas_paciente[sintoma] - doença[sintoma])
            pontos = 4 - diferença
            pontuação_total += pontos
        
        confiança = (pontuação_total / pontuação_máxima) × 100
        
        Armazenar (doença, confiança)
    
    Retornar doenças ordenadas por confiança decrescente
FIM FUNÇÃO
```

### Justificativa Metodológica

Esta abordagem foi escolhida porque:

1. **Simplicidade e Transparência**: O cálculo é facilmente auditável e explicável
2. **Adequação ao Domínio**: Médicos frequentemente raciocinam em termos de "proximidade" ao quadro clínico típico
3. **Tratamento de Incerteza Implícito**: Aceita variações nas intensidades sintomáticas
4. **Baixo Custo Computacional**: O(n × m) onde n = doenças, m = sintomas

---

## Tratamento de Incertezas

### Fontes de Incerteza no Domínio Médico

1. **Subjetividade da Percepção**: A mesma dor pode ser relatada diferentemente por pacientes distintos
2. **Variabilidade Biológica**: Nem todos os pacientes manifestam sintomas com a mesma intensidade
3. **Ambiguidade Diagnóstica**: Múltiplas doenças podem compartilhar sintomas similares
4. **Incompletude de Informação**: Alguns sintomas podem ainda não ter se manifestado

### Estratégias Implementadas

#### 1. Escala Gradual de Intensidade

Ao invés de representação binária (presente/ausente), utilizamos uma **escala de 5 pontos**, permitindo:

- Capturar nuances na manifestação sintomática
- Modelar incerteza através de valores intermediários
- Aproximar-se da lógica fuzzy sem sua complexidade formal

#### 2. Pontuação por Proximidade (Fuzzy-like)

O sistema **não exige match exato**. Um paciente com febre "forte" (4) ainda recebe pontuação alta para uma doença que tipicamente apresenta febre "muito forte" (5):

```
Diferença = |4 - 5| = 1
Pontos = 4 - 1 = 3 (de um máximo de 4)
```

#### 3. Ranking Probabilístico

Em vez de um diagnóstico único, o sistema retorna um **ranking de hipóteses** com índices de confiança, permitindo ao usuário:

- Visualizar diagnósticos alternativos
- Compreender a margem de incerteza
- Tomar decisões mais informadas

#### 4. Visualização da Incerteza

- **Gap de Diferenciação**: Mostra quanto a hipótese principal se destaca das demais
- **Gráfico de Radar**: Evidencia visualmente as discrepâncias entre sintomas relatados e perfil esperado
- **Análise de Contribuição**: Identifica quais sintomas são mais/menos compatíveis

### Comparação com Outras Abordagens

| Abordagem | Vantagens | Desvantagens |
|-----------|-----------|--------------|
| **Lógica Booleana** | Simples, determinística | Não trata incerteza |
| **Lógica Fuzzy Completa** | Tratamento robusto de incerteza | Complexidade de implementação |
| **Redes Bayesianas** | Probabilidade formal | Requer dados estatísticos extensos |
| **Nossa Abordagem (Proximidade)** | Equilíbrio entre simplicidade e flexibilidade | Menos rigor matemático que Bayesianas |

---

## 🖥️ Interface do Usuário

### Componentes Principais

#### 1. Sidebar - Entrada de Dados
- Sliders para cada sintoma (escala 1-5)
- Descrições visuais com emojis
- Legenda explicativa da escala
- Botão de consulta destacado

#### 2. Aba "Diagnóstico"
- **Métricas principais**: Doença provável e índice de confiança
- **Tabela de ranking**: Todas as hipóteses ordenadas
- **Gráfico de barras**: Comparação visual das probabilidades

#### 3. Aba "Análise Detalhada"
- **Gráfico de Radar**: Comparação sintoma a sintoma entre paciente e perfil da doença
- **Análise de Contribuição**: Identificação dos sintomas mais decisivos

#### 4. Aba "Distribuição"
- **Gráfico de linha**: Evolução das probabilidades ao longo das hipóteses
- **Gap de Diferenciação**: Métrica de certeza diagnóstica
- **Heatmap comparativo**: Visualização global de todos os perfis

#### 5. Aba "Base de Conhecimento"
- Visualização da base numérica processada
- Opção de exibir dados originais em texto

### Recursos de Usabilidade

-  **Design responsivo** com layout em colunas
-  **Visualizações interativas** usando Matplotlib e Seaborn
-  **Explicações contextuais** através de expanders
-  **Disclaimers de segurança** destacados
-  **Persistência de estado** mantém resultados ao ajustar parâmetros

---

## Resultados e Análises

### Capacidades do Sistema

O sistema demonstra capacidade de:

1. **Diferenciar doenças com perfis sintomáticos distintos** (ex: Dengue vs. Gripe)
2. **Identificar casos ambíguos** quando sintomas são compartilhados (ex: Dengue vs. Chikungunya)
3. **Tolerar variações individuais** nas intensidades sintomáticas
4. **Prover explicações visuais** para suas conclusões

### Cenários de Teste

#### Cenário 1: Caso Típico de Dengue
**Entrada:**
- Febre: 5, Dor de cabeça: 4, Dor articular: 5, Dor muscular: 4, Manchas na pele: 4, Dor nos olhos: 4

**Resultado Esperado:**
- Dengue: >85% de confiança
- Gap significativo em relação a outras doenças

#### Cenário 2: Sintomas Inespecíficos (Gripe Comum)
**Entrada:**
- Febre: 3, Dor de cabeça: 3, Tosse: 4, Dor de garganta: 3, Congestão nasal: 4

**Resultado Esperado:**
- Gripe: >70% de confiança
- Outras doenças respiratórias em posições próximas

#### Cenário 3: Caso Ambíguo (Sintomas Mistos)
**Entrada:**
- Valores intermediários em múltiplos sintomas

**Resultado Esperado:**
- Múltiplas hipóteses com confiança próxima
- Gap baixo entre 1º e 2º lugares

### Métricas de Qualidade

- **Transparência**: Sistema explica cada passo do raciocínio
- **Cobertura**: Avalia todas as doenças na base de conhecimento
- **Robustez**: Funciona mesmo com dados incompletos (valores padrão = 1)

---

## Limitações e Trabalhos Futuros

### Limitações Atuais

1. **Base de Conhecimento Limitada**
   - Número reduzido de doenças e sintomas
   - Ausência de fatores epidemiológicos (região, época do ano)
   - Não considera histórico médico do paciente

2. **Ausência de Aprendizado**
   - Sistema não aprende com novos casos
   - Perfis de doenças são estáticos
   - Não há feedback loop para refinamento

3. **Simplificação Clínica**
   - Não considera exames laboratoriais
   - Ignora progressão temporal dos sintomas
   - Ausência de comorbidades

4. **Validação Médica**
   - Não validado por profissionais de saúde
   - Dados sintomáticos baseados em descrições genéricas
   - Não testado com casos reais

## Equipe de Desenvolvimento

- **Davi Eduardo** 
- **Vitória Cordeiro** 
- **Nathália Gualberto**
- **Caio Queiroz**

---

## Referências

### Sistemas Especialistas Clássicos

1. **Shortliffe, E. H. (1976)**. *Computer-Based Medical Consultations: MYCIN*. Elsevier.
   - Sistema pioneiro em diagnóstico de infecções bacterianas

2. **Miller, R. A. et al. (1982)**. *INTERNIST-1: An Experimental Computer-Based Diagnostic Consultant for General Internal Medicine*. New England Journal of Medicine.

### Inteligência Artificial e Lógica Fuzzy

3. **Russell, S., & Norvig, P. (2020)**. *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
   - Capítulos 8, 9 e 13 (Representação do Conhecimento e Incerteza)

4. **Zadeh, L. A. (1965)**. *Fuzzy Sets*. Information and Control, 8(3), 338-353.
   - Artigo seminal sobre lógica fuzzy

5. **Pearl, J. (1988)**. *Probabilistic Reasoning in Intelligent Systems*. Morgan Kaufmann.
   - Redes Bayesianas aplicadas a sistemas especialistas

### Aplicações Médicas de IA

6. **Musen, M. A. et al. (2014)**. *Clinical Decision-Support Systems*. Biomedical Informatics, 643-674.

7. **Hamet, P., & Tremblay, J. (2017)**. *Artificial Intelligence in Medicine*. Metabolism, 69, S36-S40.

### Documentação Técnica

8. **Streamlit Documentation**. https://docs.streamlit.io
9. **Pandas Documentation**. https://pandas.pydata.org/docs
10. **Seaborn Documentation**. https://seaborn.pydata.org

---

## ⚖️ Disclaimer Legal

⚠️ AVISO IMPORTANTE - USO ACADÊMICO

Este software foi desenvolvido exclusivamente para fins educacionais e de demonstração
de conceitos de Inteligência Artificial (Sistemas Especialistas).

ESTE SISTEMA NÃO:
❌ Fornece diagnóstico médico real ou confiável
❌ Substitui consulta com profissional de saúde qualificado
❌ Deve ser utilizado para tomada de decisões clínicas
❌ Foi validado clinicamente ou aprovado por autoridades sanitárias

EM CASO DE SINTOMAS REAIS:
✅ Procure imediatamente um médico ou serviço de saúde
✅ Não baseie decisões de saúde neste sistema
✅ Considere este software apenas como exercício acadêmico

Os desenvolvedores e instituição de ensino não se responsabilizam por qualquer uso indevido desta ferramenta.