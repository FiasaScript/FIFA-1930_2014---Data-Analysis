# FIFA World Cup (1930-2014) - Exploratory Data Analysis (EDA)

<p align="center">
  <img width="25%" src="https://img.shields.io/badge/FiasaScript-057019.svg?style=for-the-badge&logo=adobe&logoColor=white" />
</p>

<p align="center">
  <a href="#about-the-project">About</a> •
  <a href="#analysis-stages">Analysis Stages</a> •
  <a href="#key-findings">Key Findings</a> 
</p>

---

## About the Project

This project conducts a comprehensive and rigorous **Exploratory Data Analysis (EDA)** on the historical match dataset of the FIFA World Cup, covering 20 editions from the pioneer tournament in 1930 (Uruguay) to 2014 (Brazil), totaling 850 match records. This study was developed as a practical component of the **Exploratory Data Analysis course at UNIFEI (2026.1)**.

The main objective is to extract historical insights and patterns of global soccer over nearly a century, analyzing the long-term evolution of goals per match, stadium attendance dynamics, the classic home-field advantage, and tactical transformations across different eras.

> **Data Integrity Disclaimer:** The analysis accounts for and actively corrects original dataset quality issues, such as duplicated match records in the 2014 tournament.

---

## Analysis Stages

The data processing and exploration pipeline structured in the Python code strictly follows these methodological phases:

* **Stage 1: Data Understanding:** Loading the `FIFA_World_Cup_1558_23.csv` dataset and mapping quantitative and qualitative variables (including the ordinal classification of tournament progression stages).
* **Stage 2: Data Audit:**
    * Identifying and removing **15 duplicate matches** (30 identical rows) concentrated entirely in the 2014 World Cup.
    * Validating logical consistency (ensuring halftime goals never exceed cumulative full-time goals).
    * Detecting stadium attendance outliers via the `1.5 * IQR` rule (revealing historic, high-capacity venues like Maracanã and Azteca) and legitimate historical blowouts (such as Hungary 10x1 El Salvador).
* **Stage 3: Univariate Analysis:** Computing descriptive statistics (mean, median, mode, standard deviation, variance, skewness, and coefficient of variation) accompanied by automated histograms and boxplots.
* **Stage 4: Bivariate Analysis:** Evaluating Pearson linear correlation and scatter plots to examine relationships such as home vs. away goals and stadium attendance growth trends across decades.
* **Stage 5: Multicollinearity:** Mapping redundant structural dependencies (like halftime goals vs. full-time goals) to protect future predictive models from data leakage[cite: 1, 2].
* **Stage 6: Multivariate Visualization:** Investigating the complex interplay between tournament year, total goals, decisive stages, and attendance, segmented into three major eras (1930-1966, 1970-1994, 1998-2014)[cite: 2].

---

## Key Findings

* **Soccer is a low-scoring sport:** Goal distributions are heavily right-skewed[cite: 1, 2]. Most matches end with a total of 1 to 3 goals[cite: 1].
* **The Home-Field Advantage:** Historically, teams designated as hosts score nearly twice as many goals as visitors (average of 1.81 vs. 1.02)[cite: 1, 2].
* **Tactical Balance and Parity:** Older World Cups (1930-1966 era) had higher-scoring, more dispersed games[cite: 1, 2]. Modern eras (1998-2014) show much more compact and defensive goal distributions, reflecting modern tactical parity[cite: 1, 2].
* **Stadium Attendance Saturation:** Crowd attendance grew steadily up to the 1980s and 1990s[cite: 1, 2], stabilizing thereafter as modern venues prioritize safety and comfort over raw, massive capacities[cite: 1, 2].
