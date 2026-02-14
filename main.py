"""
FastaFlow - Pipeline Automatizado

Propósito: Pipeline integrado para processamento de arquivos FASTA.
Realiza validação, limpeza de sequências inválidas, cálculo de estatísticas
e integração com módulos de análise (GCScan, SNPTracker, etc.).

Este pipeline serve como orquestrador para as ferramentas de bioinformática.
"""

from Bio import SeqIO
import os


def validate_sequence(sequence):
    """
    Valida se uma sequência contém apenas bases válidas (ATGC).

    Args:
        sequence: Sequência de DNA (string)

    Returns:
        bool: True se válida, False caso contrário
    """
    valid_bases = set("ATGC")
    sequence_upper = str(sequence).upper()

    for base in sequence_upper:
        if base not in valid_bases:
            return False

    return True


def clean_sequence(sequence):
    """
    Remove caracteres inválidos de uma sequência.

    Args:
        sequence: Sequência de DNA (string)

    Returns:
        str: Sequência limpa (apenas ATGC)
    """
    valid_bases = set("ATGC")
    cleaned = "".join([base for base in str(sequence).upper() if base in valid_bases])
    return cleaned


def calculate_statistics(records):
    """
    Calcula estatísticas básicas das sequências.

    Args:
        records: Lista de objetos SeqRecord

    Returns:
        dict: Dicionário com estatísticas
    """
    stats = {
        "total_sequences": len(records),
        "total_bases": sum(len(r.seq) for r in records),
        "avg_length": sum(len(r.seq) for r in records) / len(records) if records else 0,
        "shortest": min((len(r.seq), r.id) for r in records) if records else (0, ""),
        "longest": max((len(r.seq), r.id) for r in records) if records else (0, ""),
    }

    return stats


def process_fasta(input_file, output_dir="processed"):
    """
    Processa arquivo FASTA executando todo o pipeline.

    Args:
        input_file: Caminho para arquivo FASTA de entrada
        output_dir: Diretório para arquivos processados

    Returns:
        list: Lista de registros processados
    """
    print(f"\nProcessando: {input_file}")
    print("-" * 60)

    if not os.path.exists(input_file):
        print(f"Erro: Arquivo não encontrado: {input_file}")
        return []

    # Lê sequências
    records = list(SeqIO.parse(input_file, "fasta"))
    print(f"Total de sequências lidas: {len(records)}")

    # Valida e limpa
    valid_records = []
    invalid_count = 0

    for record in records:
        if validate_sequence(record.seq):
            valid_records.append(record)
        else:
            invalid_count += 1
            # Limpa sequência inválida
            record.seq = clean_sequence(record.seq)
            if len(record.seq) > 0:
                valid_records.append(record)

    print(f"Sequências válidas: {len(valid_records)}")
    print(f"Sequências com caracteres inválidos: {invalid_count}")

    # Calcula estatísticas
    if valid_records:
        stats = calculate_statistics(valid_records)
        print(f"\nEstatísticas:")
        print(f"  Total de bases: {stats['total_bases']}")
        print(f"  Comprimento médio: {stats['avg_length']:.2f} bp")
        print(f"  Menor sequência: {stats['shortest'][1]} ({stats['shortest'][0]} bp)")
        print(f"  Maior sequência: {stats['longest'][1]} ({stats['longest'][0]} bp)")

    # Cria diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Salva arquivo processado
    output_file = os.path.join(output_dir, os.path.basename(input_file))
    SeqIO.write(valid_records, output_file, "fasta")
    print(f"\nArquivo processado salvo em: {output_file}")

    return valid_records


def run_pipeline(input_dir="data", output_dir="processed"):
    """
    Executa o pipeline completo em todos os arquivos FASTA do diretório.

    Args:
        input_dir: Diretório com arquivos FASTA de entrada
        output_dir: Diretório para arquivos processados
    """
    print("=" * 60)
    print("FastaFlow - Pipeline Automatizado")
    print("=" * 60)

    # Lista arquivos FASTA
    fasta_files = []
    if os.path.exists(input_dir):
        for file in os.listdir(input_dir):
            if file.endswith((".fasta", ".fa", ".fna")):
                fasta_files.append(os.path.join(input_dir, file))

    if not fasta_files:
        print(f"\nNenhum arquivo FASTA encontrado em: {input_dir}")
        print("Crie a pasta 'data/' e adicione arquivos .fasta")
        return

    print(f"\n{len(fasta_files)} arquivo(s) encontrado(s)")

    # Processa cada arquivo
    all_records = []
    for fasta_file in fasta_files:
        records = process_fasta(fasta_file, output_dir)
        all_records.extend(records)

    # Resumo final
    print("\n" + "=" * 60)
    print("RESUMO DO PIPELINE")
    print("=" * 60)
    print(f"Total de sequências processadas: {len(all_records)}")
    print(f"Arquivos de saída em: {output_dir}/")
    print("\nPipeline concluído com sucesso!")

    return all_records


def main():
    """Função principal do programa."""
    run_pipeline()


if __name__ == "__main__":
    main()
