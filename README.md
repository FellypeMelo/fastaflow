# FastaFlow - Pipeline Automatizado

## Descrição

O **FastaFlow** é um pipeline integrado para processamento, limpeza e análise de arquivos FASTA. Ele automatiza tarefas repetitivas de bioinformática, funcionando como orquestrador para outras ferramentas do ecossistema (GCScan, SNPTracker, etc.).

### O que é um Pipeline?

Um pipeline é uma sequência automatizada de processos onde a saída de um estágio serve como entrada do próximo. No contexto de bioinformática, pipelines são essenciais para:

- Processamento em larga escala
- Padronização de análises
- Reprodutibilidade de resultados
- Economia de tempo

## Funcionalidades

### 1. Validação de Sequências
- Verifica se contêm apenas bases válidas (A, T, G, C)
- Detecta caracteres inválidos (N, X, números, etc.)

### 2. Limpeza Automática
- Remove caracteres não-ATGC
- Converte para maiúsculas
- Mantém integridade dos IDs

### 3. Estatísticas Básicas
- Número total de sequências
- Comprimento médio, mínimo e máximo
- Total de bases processadas

### 4. Processamento em Lote
- Processa todos os arquivos .fasta, .fa, .fna de uma pasta
- Organiza saída em diretório separado
- Mantém estrutura original

## Estrutura de Dados

### 📁 `test_data/` - Dados Sintéticos (Commitados)
Contém **55+ arquivos FASTA** para testar o pipeline:
- ✅ **Commitados no GitHub**
- 🧹 **Arquivos limpos** (válidos, prontos para processamento)
- 🧹 **Arquivos sujos** (com contaminação 5-30% para testar limpeza)
- 📊 **Variação de tamanhos** (curtas <50bp, longas >1000bp)
- 🧪 **Stress tests** (100 sequências, GC extremos)

**Regenerar:**
```bash
python generate_test_data.py
```

### 📁 `data/` - Dados Reais (Gitignored)
Para dados crus de sequenciamento:
- 🚫 **Ignorado pelo Git**
- 🧬 **Dados brutos** do sequenciador
- 📦 **Arquivos grandes** permitidos

**Fontes recomendadas:**
- **NCBI SRA** - Dados de sequenciamento públicos
- **Sequenciamento próprio** - Seu output de máquina
- **Bases de dados** - GenBank, RefSeq

**Formatos suportados:**
- **Nucleotide FASTA** (.fasta, .fa, .fna) ← Principal
- **FASTQ** - Com qualidade (futuro)

## Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip

### Passos

```bash
git clone https://github.com/FellypeMelo/fastaflow.git
cd fastaflow
pip install -r requirements.txt
```

## Como Usar

### Execução Básica

```bash
python main.py
```

### Estrutura de Pastas Esperada

```
fastaflow/
├── data/               # Coloque seus arquivos FASTA aqui
│   ├── amostra1.fasta
│   ├── amostra2.fa
│   └── amostra3.fna
├── processed/          # Arquivos processados (criado automaticamente)
│   ├── amostra1.fasta
│   ├── amostra2.fa
│   └── amostra3.fna
└── main.py
```

### Exemplo de Uso

1. **Adicione seus arquivos**:
```bash
mkdir -p data
cp seus_arquivos/*.fasta data/
```

2. **Execute o pipeline**:
```bash
python main.py
```

3. **Verifique os resultados**:
```bash
ls processed/
```

### Exemplo de Saída

```
============================================================
FastaFlow - Pipeline Automatizado
============================================================

3 arquivo(s) encontrado(s)

Processando: data/amostra1.fasta
------------------------------------------------------------
Total de sequências lidas: 5
Sequências válidas: 5
Sequências com caracteres inválidos: 0

Estatísticas:
  Total de bases: 1250
  Comprimento médio: 250.00 bp
  Menor sequência: seq_001 (150 bp)
  Maior sequência: seq_005 (400 bp)

Arquivo processado salvo em: processed/amostra1.fasta

============================================================
RESUMO DO PIPELINE
============================================================
Total de sequências processadas: 15
Arquivos de saída em: processed/

Pipeline concluído com sucesso!
```

## Estrutura do Projeto

```
fastaflow/
├── main.py              # Código principal do pipeline
├── requirements.txt     # Dependências (Biopython)
├── README.md           # Documentação
└── data/
    └── sample.fasta    # Arquivo de exemplo
```

## Guia de Desenvolvimento

### Milestones do Projeto

#### Milestone 1: Pipeline Básico ✅
- [x] Leitura de múltiplos arquivos FASTA
- [x] Validação de sequências
- [x] Limpeza de caracteres inválidos
- [x] Estatísticas básicas
- [x] Organização de saída
- [x] Documentação inicial

#### Milestone 2: Integração de Módulos 🚧
- [ ] Integração com GCScan para análise de GC
- [ ] Integração com SNPTracker para comparação
- [ ] Geração de relatório consolidado
- [ ] Suporte a configurações via arquivo JSON/YAML
- [ ] Logging profissional

#### Milestone 3: Funcionalidades Avançadas 📊
- [ ] Processamento paralelo (multiprocessing)
- [ ] Suporte a arquivos grandes (>1GB)
- [ ] Compressão automática (gzip)
- [ ] Validação de checksum (MD5/SHA)
- [ ] Backup automático

#### Milestone 4: Automação Completa 🔄
- [ ] Interface de linha de comando completa (argparse)
- [ ] Modo daemon (monitoramento de pasta)
- [ ] Notificações (email/Slack)
- [ ] Relatórios em PDF/HTML
- [ ] Dashboard web

### Tarefas para Contribuidores

**Nível Iniciante:**
1. Adicionar argparse para CLI completa
2. Implementar logging em vez de print
3. Criar arquivo de configuração
4. Adicionar barra de progresso (tqdm)

**Nível Intermediário:**
1. Integrar com módulos GCScan e SNPTracker
2. Implementar processamento paralelo
3. Criar relatório consolidado
4. Adicionar suporte a qualidade (FASTQ)

**Nível Avançado:**
1. Criar sistema de plugins
2. Implementar pipeline em DAG (Airflow/Prefect)
3. Criar interface web
4. Adicionar execução em nuvem (AWS/GCP)

## Arquitetura do Pipeline

```
┌─────────────────┐
│   Input (data/) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Validação      │
│  • Formato      │
│  • Bases ATGC   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Limpeza       │
│  • Remove inválidos
│  • Uppercase    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Estatísticas  │
│  • N, min, max  │
│  • Tamanhos     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Output         │
│  (processed/)   │
└─────────────────┘
```

## Integração com Outros Módulos

### Exemplo de Workflow Completo

```python
# Pipeline completo integrado
from fastaflow import process_fasta
from gcscan import calculate_gc_content
from snptracker import detect_snps

# 1. Limpar e validar
records = process_fasta("input.fasta")

# 2. Analisar GC
for record in records:
    gc = calculate_gc_content(record)
    
# 3. Comparar com referência
snps = detect_snps(reference, sample)

# 4. Gerar relatório
save_report(gc_results, snps)
```

## Casos de Uso

### 1. Preparação de Dados para Análise
```bash
# Limpar dados crus de sequenciamento
python main.py --input raw_data/ --output cleaned/
```

### 2. Quality Control (QC)
```bash
# Filtrar sequências por tamanho
python main.py --min-length 100 --max-length 1000
```

### 3. Pipeline de Produção
```bash
# Processar todos os arquivos de um projeto
python main.py --project PROJ001 --notify email
```

### 4. Automação de Rotina
```bash
# Agendar no cron (Linux/Mac)
0 2 * * * cd /path/to/fastaflow && python main.py
```

## Conceitos Relacionados

### Formatos Suportados
- **FASTA**: Formato padrão (>.id + sequência)
- **Multi-FASTA**: Múltiplas sequências em um arquivo
- **FAA/FNA**: FASTA de aminoácidos/nucleotídeos

### Qualidade de Dados
- **N bases**: Representam ambiguidade
- **Low complexity**: Regiões repetitivas
- **Vector contamination**: Sequências de vetores

### Boas Práticas
- Sempre manter backup dos dados originais
- Versionar os parâmetros do pipeline
- Documentar cada etapa
- Validar saídas antes de prosseguir

## Limitações Atuais

- Apenas arquivos FASTA (não FASTQ)
- Sem filtro de qualidade
- Sem processamento paralelo
- Sem análises avançadas
- Sem integração automática (manual)

## Próximos Passos Recomendados

1. **CLI Completa**: Usar argparse para todas as opções
2. **Config File**: Suporte a YAML/JSON de configuração
3. **Logging**: Implementar sistema de logging
4. **Integração**: Conectar automaticamente com outros módulos
5. **Documentação**: Criar wiki ou site de documentação

## Comparação com Ferramentas Existentes

| Ferramenta | Propósito | Diferença do FastaFlow |
|------------|-----------|----------------------|
| **SeqKit** | Processamento FASTA/Q | FastaFlow é Python puro, mais simples |
| **Biopython SeqIO** | Parsing | FastaFlow é pipeline completo |
| **Snakemake** | Workflow engine | FastaFlow é mais simples, sem DSL |

## Referências

- [Biopython](https://biopython.org/)
- [FASTA Format](https://en.wikipedia.org/wiki/FASTA_format)
- [Workflow Management](https://en.wikipedia.org/wiki/Workflow_engine)
- [Snakemake](https://snakemake.readthedocs.io/)
- [Nextflow](https://www.nextflow.io/)

## Licença

MIT License - veja arquivo LICENSE

## Contato

Abra uma issue para dúvidas ou sugestões.

---

**Status**: 🟢 Funcional - Pronto para uso e expansão

**Última Atualização**: 2026