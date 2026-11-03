# BSD3513 / BSD2513 Artificial Intelligence — Lab Report 2

## Chapter 2: Search Algorithms (Genetic Algorithm Implementation)

---

## 📌 Project Overview

This repository contains the source code, optimization engine, and Streamlit deployment for **Question 2 (Python: Search Algorithms - Genetic Algorithm)** of Lab Report 2 in **BSD3513 Introduction to Artificial Intelligence** at Universiti Malaysia Pahang Al-Sultan Abdullah (UMPSA).

The application demonstrates heuristic search by evolving an initial population of binary chromosomes over successive generations using tournament selection, single-point crossover, bit-flip mutation, and elitism to converge toward a predefined target pattern.

---

### 🌐 Live Deployment & Repository Links

* **Live Streamlit Web App:** `[Insert your Streamlit App URL here, e.g., https://your-app-name.streamlit.app]`
* **GitHub Repository:** `[Insert your GitHub Repo URL here, e.g., https://github.com/your-username/your-repo-name]`

---

## 📋 Problem Specifications & Conditions

The optimization problem strictly satisfies the following five predefined conditions:

1. **Population Size ($N$):** $300$ individuals
2. **Optimal Peak Condition:** Reaches its global maximum value when the number of ones equals $50$.
3. **Chromosome Length ($L$):** $80$ bits per individual
4. **Maximum Return Value:** When the number of ones equals $50$, the return value (fitness) is exactly $80$.
5. **Generations:** $50$ evolutionary cycles

---

### Mathematical Formulation

Let $\mathbf{x} = [x_1, x_2, \dots, x_{80}] \in \{0, 1\}^{80}$ denote an individual chromosome, and let $k = \sum_{i=1}^{80} x_i$ be the total count of set bits (ones). The fitness function $f(\mathbf{x})$ is defined as:

$$f(\mathbf{x}) = 80 - |k - 50|$$

* **Global Optimum ($k = 50$):**
  $$f(\mathbf{x}) = 80 - |50 - 50| = 80$$
* **Boundary Case — Minimum ($k = 0$):**
  $$f(\mathbf{x}) = 80 - |0 - 50| = 30$$
* **Boundary Case — All Ones ($k = 80$):**
  $$f(\mathbf{x}) = 80 - |80 - 50| = 50$$

---

## ⚙️ Genetic Algorithm Architecture

| Component | Mechanism | Details |
| :--- | :--- | :--- |
| **Representation** | Binary Array | 1D NumPy array of length 80 (`dtype=np.int8`) |
| **Selection** | Tournament Selection | Tournament size $k = 3$ |
| **Crossover** | Single-Point Crossover | Crossover probability $p_c = 0.90$ |
| **Mutation** | Bit-Flip Mutation | Per-bit mutation probability $p_m = \frac{1}{L} = 0.0125$ |
| **Elitism** | Direct Survival | Top 2 individuals preserved per generation |
| **Tracking** | Statistical Convergence | Records Best, Average, and Worst fitness per generation |

---

## 📂 Repository File Structure

```text
.
├── app.py              # Main Streamlit web application & GA engine
├── requirements.txt    # Python library dependencies
└── README.md           # Documentation and problem specifications
```

---

## 🚀 Local Installation & Execution

### 1. Clone the Repository

```bash
git clone https://github.com/[your-username]/[your-repo-name].git
cd [your-repo-name]
```

### 2. Configure Virtual Environment (Optional)

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the Streamlit App

```bash
streamlit run app.py
```

---

## 📦 Required Dependencies (`requirements.txt`)

```text
streamlit>=1.30.0
numpy>=1.24.0
matplotlib>=3.8.0
```
