# app.py
import random
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# ---- Fixed GA Parameters----
POP_SIZE = 300
CHROM_LEN = 80
TARGET_ONES = 50
MAX_FITNESS = 80
N_GENERATIONS = 50

# ---- GA Hyperparameters ----
TOURNAMENT_K = 3
CROSSOVER_RATE = 0.9
MUTATION_RATE = 1.0 / CHROM_LEN  
ELITISM_COUNT = 2                

# ---- Fitness Function ----
def fitness(individual: np.ndarray) -> float:
    """
    Fitness reaches maximum value of 80 when the number of 1s equals 50.
    """
    ones = int(individual.sum())
    return float(MAX_FITNESS - abs(ones - TARGET_ONES))

# ---- GA Operators ----
def init_population(pop_size: int, chrom_len: int) -> np.ndarray:
    return np.random.randint(0, 2, size=(pop_size, chrom_len), dtype=np.int8)

def tournament_selection(pop: np.ndarray, fits: np.ndarray, k: int) -> np.ndarray:
    idxs = np.random.randint(0, len(pop), size=k)
    best_idx = idxs[np.argmax(fits[idxs])]
    return pop[best_idx].copy()

def single_point_crossover(p1: np.ndarray, p2: np.ndarray):
    if np.random.rand() > CROSSOVER_RATE:
        return p1.copy(), p2.copy()
    point = np.random.randint(1, CHROM_LEN)
    c1 = np.concatenate([p1[:point], p2[point:]])
    c2 = np.concatenate([p2[:point], p1[point:]])
    return c1, c2

def mutate(individual: np.ndarray) -> np.ndarray:
    mask = np.random.rand(CHROM_LEN) < MUTATION_RATE
    individual[mask] = 1 - individual[mask]
    return individual

def evolve(pop: np.ndarray, generations: int):
    best_fitness_per_gen = []
    avg_fitness_per_gen = []
    worst_fitness_per_gen = []
    best_individual = None
    best_f = -np.inf

    for _ in range(generations):
        fits = np.array([fitness(ind) for ind in pop])

        # Track population statistics (Best, Average, Worst)
        gen_best_idx = np.argmax(fits)
        gen_best_f = float(fits[gen_best_idx])
        gen_avg_f = float(np.mean(fits))
        gen_worst_f = float(np.min(fits))

        best_fitness_per_gen.append(gen_best_f)
        avg_fitness_per_gen.append(gen_avg_f)
        worst_fitness_per_gen.append(gen_worst_f)

        if gen_best_f > best_f:
            best_f = gen_best_f
            best_individual = pop[gen_best_idx].copy()

        # Elitism: retain top individuals
        elite_indices = np.argsort(fits)[-ELITISM_COUNT:]
        elites = [pop[idx].copy() for idx in elite_indices]

        # Generate next generation
        new_pop = list(elites)
        while len(new_pop) < len(pop):
            p1 = tournament_selection(pop, fits, TOURNAMENT_K)
            p2 = tournament_selection(pop, fits, TOURNAMENT_K)
            c1, c2 = single_point_crossover(p1, p2)
            c1 = mutate(c1)
            c2 = mutate(c2)
            new_pop.append(c1)
            if len(new_pop) < len(pop):
                new_pop.append(c2)

        pop = np.array(new_pop, dtype=np.int8)

    return best_individual, best_f, best_fitness_per_gen, avg_fitness_per_gen, worst_fitness_per_gen

# ---- Streamlit UI ----
st.set_page_config(page_title="Bit Pattern GA (80 bits, target ones = 50)", page_icon="🧬", layout="centered")

st.title("🧬 Genetic Algorithm: Evolve an 80-bit Pattern")
st.caption(
    "Requirements: Population = 300, Length = 80, Generations = 50.\n"
    "Target: 50 ones yields maximum fitness = 80."
)

with st.expander("ℹ️ Problem Setup (Lab Report 2 Specifications)", expanded=True):
    st.markdown(
        f"""
- **Population size**: `{POP_SIZE}`
- **Chromosome length**: `{CHROM_LEN}`
- **Target number of ones**: `{TARGET_ONES}`
- **Maximum fitness**: `{MAX_FITNESS}`
- **Generations**: `{N_GENERATIONS}`
        """
    )

col1, col2 = st.columns(2)
with col1:
    seed = st.number_input("Random seed (reproducibility)", min_value=0, value=42, step=1)
with col2:
    st.write("")
    st.write("")
    run_btn = st.button("Run Genetic Algorithm", type="primary")

if run_btn:
    random.seed(seed)
    np.random.seed(seed)

    population = init_population(POP_SIZE, CHROM_LEN)
    best_ind, best_fit, best_curve, avg_curve, worst_curve = evolve(population, N_GENERATIONS)

    ones_count = int(best_ind.sum())
    zeros_count = CHROM_LEN - ones_count
    bitstring = "".join(map(str, best_ind.tolist()))

    st.subheader("🏁 Best Individual Found")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Best Fitness", f"{best_fit:.0f} / {MAX_FITNESS}")
    col_b.metric("Total Ones", f"{ones_count} / {CHROM_LEN}")
    col_c.metric("Total Zeros", f"{zeros_count} / {CHROM_LEN}")

    st.code(bitstring, language="text")

    # Convergence plot showing Best, Average (Purple), and Worst (Red)
    st.subheader("📉 Convergence Curves")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    gens = range(1, len(best_curve) + 1)
    
    ax.plot(gens, best_curve, label="Best Fitness", color="#1f77b4", linewidth=2.5)
    ax.plot(gens, avg_curve, label="Average Fitness", color="#8A2BE2", linestyle="--", linewidth=2.0)
    ax.plot(gens, worst_curve, label="Worst Fitness", color="#D62728", linestyle="-.", linewidth=1.8)
    ax.axhline(y=MAX_FITNESS, color="green", linestyle=":", alpha=0.7, label=f"Max Target ({MAX_FITNESS})")
    
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness Score")
    ax.set_title("GA Convergence: Best vs Average vs Worst Fitness")
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(loc="lower right")
    st.pyplot(fig)

    if best_fit == MAX_FITNESS and ones_count == TARGET_ONES:
        st.success(f"Optimal pattern reached: exactly {TARGET_ONES} ones with fitness {MAX_FITNESS:.0f} ✅")
    else:
        st.warning(f"Optimization terminated below target ({ones_count} ones, fitness {best_fit:.0f}).")