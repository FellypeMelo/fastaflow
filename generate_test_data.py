#!/usr/bin/env python3
"""
FastaFlow - Gerador de Dados de Teste

Este script gera 50+ conjuntos de dados para testar o pipeline.
Inclui arquivos válidos, inválidos, grandes e pequenos.

Os dados de teste são COMMITADOS no GitHub.
Para dados reais, use a pasta data/ (gitignored)
"""

import random
import os
from datetime import datetime

TEST_DATA_DIR = "test_data"
NUM_DATASETS = 55

VALID_BASES = ["A", "T", "G", "C"]
INVALID_CHARS = [
    "N",
    "X",
    "R",
    "Y",
    "K",
    "M",
    "S",
    "W",
    "B",
    "D",
    "H",
    "V",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "-",
    "_",
    "*",
    " ",
    "\n",
    "\t",
]


def generate_clean_sequence(length, gc_content=0.5):
    """Gera uma sequência válida de DNA."""
    seq = []
    for _ in range(length):
        if random.random() < gc_content:
            seq.append(random.choice(["G", "C"]))
        else:
            seq.append(random.choice(["A", "T"]))
    return "".join(seq)


def generate_dirty_sequence(length, contamination_rate=0.1):
    """Gera uma sequência com caracteres inválidos."""
    seq = generate_clean_sequence(length)
    seq_list = list(seq)

    num_contaminations = int(length * contamination_rate)
    positions = random.sample(range(length), num_contaminations)

    for pos in positions:
        seq_list[pos] = random.choice(INVALID_CHARS)

    return "".join(seq_list)


def create_fasta_entry(seq_id, sequence):
    """Cria uma entrada FASTA."""
    return f">{seq_id}\n{sequence}\n"


def generate_test_datasets():
    """Gera todos os datasets de teste."""
    datasets = []

    # 1-10: Arquivos limpos e válidos
    for i in range(10):
        num_seqs = random.randint(1, 5)
        sequences = []
        for j in range(num_seqs):
            length = random.randint(100, 500)
            seq = generate_clean_sequence(length)
            sequences.append((f"seq_{j + 1}", seq))
        datasets.append(
            (
                f"fastaflow_test_{i + 1:02d}_clean",
                sequences,
                f"Clean file, {num_seqs} sequences",
            )
        )

    # 11-20: Arquivos com contaminação leve (5-10%)
    for i in range(10, 20):
        num_seqs = random.randint(1, 5)
        sequences = []
        for j in range(num_seqs):
            length = random.randint(100, 500)
            seq = generate_dirty_sequence(
                length, contamination_rate=random.uniform(0.05, 0.10)
            )
            sequences.append((f"seq_{j + 1}", seq))
        datasets.append(
            (
                f"fastaflow_test_{i + 1:02d}_lightly_dirty",
                sequences,
                f"5-10% contamination, {num_seqs} seqs",
            )
        )

    # 21-25: Arquivos muito sujos (20-30%)
    for i in range(20, 25):
        num_seqs = random.randint(1, 3)
        sequences = []
        for j in range(num_seqs):
            length = random.randint(100, 300)
            seq = generate_dirty_sequence(
                length, contamination_rate=random.uniform(0.20, 0.30)
            )
            sequences.append((f"seq_{j + 1}", seq))
        datasets.append(
            (
                f"fastaflow_test_{i + 1:02d}_heavily_dirty",
                sequences,
                f"20-30% contamination",
            )
        )

    # 26-30: Arquivos grandes (muitas sequências)
    for i in range(25, 30):
        num_seqs = random.randint(20, 50)
        sequences = []
        for j in range(num_seqs):
            length = random.randint(50, 200)
            seq = generate_clean_sequence(length)
            sequences.append((f"seq_{j + 1}", seq))
        datasets.append(
            (
                f"fastaflow_test_{i + 1:02d}_many_sequences",
                sequences,
                f"{num_seqs} sequences",
            )
        )

    # 31-35: Arquivos com sequências muito longas
    for i in range(30, 35):
        num_seqs = random.randint(1, 3)
        sequences = []
        for j in range(num_seqs):
            length = random.randint(1000, 5000)
            seq = generate_clean_sequence(length)
            sequences.append((f"seq_{j + 1}", seq))
        datasets.append(
            (
                f"fastaflow_test_{i + 1:02d}_long_sequences",
                sequences,
                f"{num_seqs} long seqs ({length}bp)",
            )
        )

    # 36-40: Arquivos com sequências curtas
    for i in range(35, 40):
        num_seqs = random.randint(5, 15)
        sequences = []
        for j in range(num_seqs):
            length = random.randint(20, 50)
            seq = generate_clean_sequence(length)
            sequences.append((f"seq_{j + 1}", seq))
        datasets.append(
            (
                f"fastaflow_test_{i + 1:02d}_short_sequences",
                sequences,
                f"{num_seqs} short seqs",
            )
        )

    # 41-45: Variação de GC
    for i in range(40, 45):
        gc_targets = [0.2, 0.4, 0.5, 0.6, 0.8]
        sequences = []
        for j, gc in enumerate(gc_targets):
            length = random.randint(100, 300)
            seq = generate_clean_sequence(length, gc_content=gc)
            sequences.append((f"seq_{j + 1}_gc{int(gc * 100)}", seq))
        datasets.append(
            (
                f"fastaflow_test_{i + 1:02d}_gc_variation",
                sequences,
                "GC variation 20-80%",
            )
        )

    # 46-50: Cenários de pipeline
    # Arquivos que simulam saída de sequenciador
    for i in range(45, 50):
        num_seqs = random.randint(3, 8)
        sequences = []
        for j in range(num_seqs):
            length = random.randint(100, 400)
            # Mix de limpo e sujo
            if random.random() < 0.3:
                seq = generate_dirty_sequence(length, contamination_rate=0.08)
            else:
                seq = generate_clean_sequence(length)
            sequences.append((f"read_{j + 1}", seq))
        datasets.append(
            (
                f"fastaflow_test_{i + 1:02d}_sequencer_output",
                sequences,
                "Simulated sequencer output",
            )
        )

    # 51-55: Casos extremos
    # Arquivo quase vazio
    seq = generate_clean_sequence(30)
    datasets.append(
        ("fastaflow_test_51_minimal", [("seq1", seq)], "Minimal file (30bp)")
    )

    # Arquivo gigante (simulado - na verdade será grande mas não excessivo)
    sequences = []
    for j in range(100):
        seq = generate_clean_sequence(random.randint(30, 100))
        sequences.append((f"seq_{j + 1}", seq))
    datasets.append(
        ("fastaflow_test_52_massive", sequences, "100 sequences (stress test)")
    )

    # Arquivo com descrições longas
    sequences = []
    for j in range(3):
        seq = generate_clean_sequence(200)
        desc = f"seq_{j + 1}_description_with_lots_of_info_gc_{random.randint(40, 60)}_length_{len(seq)}"
        sequences.append((desc, seq))
    datasets.append(("fastaflow_test_53_long_headers", sequences, "Long FASTA headers"))

    # Arquivo com caracteres especiais nos headers
    sequences = []
    for j in range(3):
        seq = generate_clean_sequence(150)
        header = f"seq_{j + 1}|organism=Homo_sapiens|gene=BRCA{j + 1}"
        sequences.append((header, seq))
    datasets.append(
        ("fastaflow_test_54_special_headers", sequences, "Special chars in headers")
    )

    # Arquivo misto (vários tipos de problemas)
    sequences = []
    # Sequência limpa
    sequences.append(("clean", generate_clean_sequence(100)))
    # Sequência suja
    sequences.append(("dirty", generate_dirty_sequence(100, 0.15)))
    # Sequência muito curta
    sequences.append(("short", generate_clean_sequence(10)))
    # Sequência muito longa
    sequences.append(("long", generate_clean_sequence(1000)))
    # Sequência com GC extremo
    sequences.append(("gc_rich", generate_clean_sequence(100, gc_content=0.9)))
    datasets.append(("fastaflow_test_55_mixed", sequences, "Mixed scenarios"))

    return datasets


def save_datasets(datasets):
    """Salva os datasets em arquivos FASTA."""
    os.makedirs(TEST_DATA_DIR, exist_ok=True)

    manifest_path = os.path.join(TEST_DATA_DIR, "MANIFEST.txt")
    with open(manifest_path, "w") as manifest:
        manifest.write("=" * 70 + "\n")
        manifest.write("FastaFlow - Dados de Teste Sintéticos\n")
        manifest.write("=" * 70 + "\n\n")
        manifest.write(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        manifest.write(f"Total de datasets: {len(datasets)}\n\n")
        manifest.write("ATENÇÃO: Estes são dados FABRICADOS para teste.\n")
        manifest.write("Alguns contêm erros propositais para testar limpeza.\n\n")
        manifest.write("Lista de arquivos:\n")
        manifest.write("-" * 70 + "\n")

        for filename, sequences, description in datasets:
            filepath = os.path.join(TEST_DATA_DIR, f"{filename}.fasta")

            with open(filepath, "w") as f:
                for seq_id, sequence in sequences:
                    f.write(create_fasta_entry(seq_id, sequence))

            total_bp = sum(len(seq) for _, seq in sequences)
            manifest.write(f"{filename}.fasta - {description}\n")
            manifest.write(f"  {len(sequences)} seqs, {total_bp} total bp\n")
            print(f"[OK] Gerado: {filename}.fasta ({len(sequences)} seqs, {total_bp} bp)")

    print(f"\n[OK] Manifesto salvo em: {manifest_path}")
    print(f"[OK] Total: {len(datasets)} arquivos FASTA gerados")


def main():
    print("=" * 70)
    print("FastaFlow - Gerador de Dados de Teste")
    print("=" * 70)
    print()

    datasets = generate_test_datasets()
    save_datasets(datasets)

    print()
    print("=" * 70)
    print("Geração concluída!")
    print("=" * 70)
    print(f"\nDados em: {TEST_DATA_DIR}/")
    print("Execute: python main.py")


if __name__ == "__main__":
    main()
