from typing import List

def check_gc_content(dna_sequence: str) -> float:
    """Calculate the GC content percentage of a DNA sequence."""
    gc_count = dna_sequence.count('G') + dna_sequence.count('C')
    if len(dna_sequence) == 0:
        return 0.0
    return (gc_count / len(dna_sequence)) * 100


def has_long_homopolymers(dna_sequence: str, max_run: int = 3) -> bool:
    """Check if the DNA sequence contains homopolymer runs longer than max_run."""
    if max_run < 1:
        return False
    last_base = ''
    run_length = 0
    for base in dna_sequence:
        if base == last_base:
            run_length += 1
            if run_length > max_run:
                return True
        else:
            last_base = base
            run_length = 1
    return False


def contains_unstable_motifs(dna_sequence: str, motifs: List[str]) -> bool:
    """Check if the DNA sequence contains any unstable or repeating motifs."""
    for motif in motifs:
        if motif in dna_sequence:
            return True
    return False


def enforce_constraints(dna_sequence: str) -> str:
    """Modify the DNA sequence to enforce biological constraints (GC content, homopolymers, motifs)."""
    import random
    MAX_ATTEMPTS = 1000
    GC_MIN, GC_MAX = 40.0, 60.0
    MAX_HOMOPOLYMER = 2
    FORBIDDEN_MOTIFS = ["ATATAT", "CGCGCG"]
    BASES = ['A', 'C', 'G', 'T']

    # Handle empty sequences
    if not dna_sequence:
        return dna_sequence

    def mutate(seq, idx):
        current = seq[idx]
        choices = [b for b in BASES if b != current]
        return seq[:idx] + random.choice(choices) + seq[idx+1:]

    attempt = 0
    seq = dna_sequence
    while attempt < MAX_ATTEMPTS:
        gc = check_gc_content(seq)
        if gc < GC_MIN or gc > GC_MAX:
            # Mutate a random base to bring GC content closer to target
            idx = random.randrange(len(seq))
            if gc < GC_MIN:
                # Prefer G/C
                seq = seq[:idx] + random.choice(['G', 'C']) + seq[idx+1:]
            else:
                # Prefer A/T
                seq = seq[:idx] + random.choice(['A', 'T']) + seq[idx+1:]
            attempt += 1
            continue
        if has_long_homopolymers(seq, max_run=MAX_HOMOPOLYMER):
            # Break homopolymer by mutating a random run
            last_base = ''
            run_length = 0
            for i, base in enumerate(seq):
                if base == last_base:
                    run_length += 1
                    if run_length > MAX_HOMOPOLYMER:
                        seq = mutate(seq, i)
                        break
                else:
                    last_base = base
                    run_length = 1
            attempt += 1
            continue
        if contains_unstable_motifs(seq, FORBIDDEN_MOTIFS):
            # Replace one base in the motif
            for motif in FORBIDDEN_MOTIFS:
                idx = seq.find(motif)
                if idx != -1:
                    seq = mutate(seq, idx + len(motif)//2)
                    break
            attempt += 1
            continue
        # All constraints satisfied
        return seq
    raise ValueError("Unable to enforce constraints after many attempts.") 