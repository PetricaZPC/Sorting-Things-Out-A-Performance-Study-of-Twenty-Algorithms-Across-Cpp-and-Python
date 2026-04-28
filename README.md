# 📊 Sorting Things Out: A Performance Study of 20 Algorithms in C++ and Python

<br>

<p align="center">
  An experimental analysis of 20 sorting algorithms, exploring the gap between theoretical complexity and real-world performance. Implemented from scratch in C++17 and Python 3.11.
</p>

---

## 💡 The Motivation: Why Sorting?

Long before the first computer was ever switched on, humanity had a deep obsession with order. From ancient Mesopotamian scribes organizing clay tax tablets to librarians in the Library of Alexandria, the ability to find information quickly has always been a form of power.

**The "Why" behind this project:** In modern programming, sorting is often treated as a black box (a simple `.sort()`). I created this study to demonstrate that choosing the right algorithm is not just an academic exercise—it is a critical engineering decision that directly impacts server costs, response times, and energy consumption. I wanted to see where the language barrier breaks (C++ vs. Python) and where the underlying math is the only thing that matters.

---

## 📖 The Stories Behind the Code

This project isn't just about raw code; it's an exploration of fundamental problem-solving strategies, illustrated through real-world analogies:

* **1890: The Machine That Sorted a Nation:** Herman Hollerith processed the US Census in under 2 years (down from 8) not by inventing a faster counter, but by inventing a punch-card *sorting* system. His company later became **IBM**.
* **The Recipe Analogy:** An algorithm is just like a recipe. Order matters, precision matters, and the output must be predictable regardless of who (or what CPU) executes it.
* **Visualizing the Sorts:** * *Bubble Sort* is like a cinema queue where an usher compares people two by two and swaps them if needed.
  * *Cocktail Shaker Sort* is a bartender tilting a shaker back and forth so elements settle at both ends simultaneously.
  * *Quick Sort* is a teacher splitting a class into two distinct groups based on a pivot grade.

---

## 🔬 Methodology and Experiment

I implemented **20 algorithms** across 5 distinct families (Elementary, Gap-based, Divide-and-Conquer, Non-comparison, and Exotic) to measure:

1. **Wall-clock runtime**
2. **Peak memory usage**
3. **Operation counts (Comparisons and Swaps)**

### Testing Configuration:
* **Scales:** From N = 100 to N = 1,000,000.
* **Distributions:** Random (chaos), Already Sorted (best case), Reverse Sorted (the ultimate stress test).
* **Languages:** C++17 (compiled with `-O2`) vs. Python 3.11 (CPython).

---

## 🚀 Key Results and Conclusions

* **Bypassing the O(n log n) Barrier:** Non-comparison sorts (Counting Sort, Hash Sort) are **5x to 100x faster** than Quick Sort on large integer datasets because they "cheat" the math by counting values instead of directly comparing them.
* **Algorithm > Language:** At N >= 100,000, algorithm choice heavily dominates the language choice. An efficient algorithm running in Python will easily outperform an inefficient one compiled in C++.
* **The O(n²) Wall:** Algorithms like Insertion Sort become completely unusable beyond N = 10,000 in interpreted languages (Python), proving that theoretical complexities are hard physical limits, not just concepts.
* **Distribution Independence:** Heap Sort and Bitonic Sort are the most "unbiased" algorithms—they don't care if the data is already sorted or completely reversed, offering highly predictable execution times.

---

## 🛠️ Tech Stack

* **C++:** `g++ 12.3.0` (Flags: `-O2 -std=c++17`)
* **Python:** CPython 3.11.4
* **Memory Profiling:** Valgrind Massif (C++) & `tracemalloc` (Python)
* **Documentation:** LaTeX (EasyChair format)

---

> *"Sorting is the most fundamental operation in computing — and still one of the most interesting."*