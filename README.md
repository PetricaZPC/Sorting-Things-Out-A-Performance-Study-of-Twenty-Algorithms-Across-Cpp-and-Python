# 📊 Sorting Things Out: Studiul Performanței a 20 de Algoritmi în C++ și Python

<br>

<p align="center">
  O analiză experimentală a 20 de algoritmi de sortare, explorând raportul dintre complexitatea teoretică și performanța reală, implementați de la zero în C++17 și Python 3.11.
</p>

---

## 💡 Motivația Proiectului: De ce sortarea?

Cu mult înainte ca primul computer să fie pornit, omenirea a avut o obsesie pentru ordine. De la scribii mesopotamieni care organizau tăblițele de lut pentru taxe, până la bibliotecarii din Alexandria, capacitatea de a găsi informația rapid a fost mereu o formă de putere.

**Motivul acestui proiect:** În programarea modernă, sortarea este adesea tratată ca o "cutie neagră" (un simplu `.sort()`). Am creat acest studiu pentru a demonstra că alegerea algoritmului nu este doar o discuție academică, ci o decizie de inginerie care influențează costurile serverelor, timpul de răspuns și experiența utilizatorului. Am vrut să văd unde se rupe bariera limbajului (C++ vs Python) și unde contează exclusiv matematica din spatele codului.

---

## 📖 Povestea din spatele algoritmilor

Proiectul nu este doar o înșiruire de cod, ci o explorare a unor strategii fundamentale de rezolvare a problemelor, ilustrate prin analogii din lumea reală:

* **Mașina care a sortat o națiune (1890):** Herman Hollerith a procesat recensământul SUA în 2 ani (față de 8 ani anterior) nu inventând un numărător mai rapid, ci un sistem de sortare pe cartele perforate. Compania lui a devenit ulterior **IBM**.
* **Analogia Rețetei:** Un algoritm este ca o rețetă de prăjituri. Ordinea contează, precizia contează, iar rezultatul trebuie să fie predictibil indiferent de cine "gătește" (CPU-ul).
* **Poveștile Vizuale:** * **Bubble Sort** este ca o coadă la cinema unde oamenii își compară biletele doi câte doi.
    * **Cocktail Shaker** este mișcarea unui barman care balansează shaker-ul pentru a așeza elementele la ambele capete.
    * **Quick Sort** este ca un profesor care împarte clasa în funcție de o notă pivot.

---

## 🔬 Metodologie și Experiment

Am implementat **20 de algoritmi** organizați pe familii (Elementary, Gap-based, Divide-and-Conquer, Non-comparison și Exotic) pentru a măsura:

1.  **Timpul de execuție (Wall-clock runtime)**
2.  **Consumul maxim de memorie (Peak memory usage)**
3.  **Numărul de operații (Comparații și Swaps)**

### Configurația Testelor:
* **Scări de date:** De la $n=100$ la $n=1.000.000$.
* **Distribuții:** Random (haos), Sorted (deja ordonat), Reverse Sorted (cel mai greu caz).
* **Limbaje:** C++17 (compilat cu -O2) vs Python 3.11 (CPython).

---

## 🚀 Rezultate și Concluzii Cheie

* **Bariera O(n log n):** Algoritmii de non-comparație (Counting Sort, Hash Sort) sunt de **5-100x mai rapizi** decât Quick Sort la volume mari de date, deoarece "trișează" matematica prin numărarea valorilor în loc de compararea lor.
* **Alegerea bate Limbajul:** La $n \geq 100.000$, alegerea algoritmului devine mai importantă decât limbajul de programare. Un algoritm eficient în Python va bate un algoritm ineficient în C++.
* **Zidul O(n²):** Algoritmi precum Insertion Sort devin complet inutilizabili peste $n=10.000$ în limbaje interpretate (Python), transformând conceptele teoretice în limitări fizice reale.
* **Independența de Distribuție:** Heap Sort și Bitonic Sort sunt cei mai "imparțiali" algoritmi — nu le pasă dacă datele sunt deja sortate sau nu, oferind un timp constant.

---

## 🛠️ Tech Stack

* **C++:** `g++ 12.3.0` (Flags: `-O2 -std=c++17`)
* **Python:** CPython 3.11.4
* **Analiză Memorie:** Valgrind Massif (C++) și `tracemalloc` (Python)
* **Documentație:** LaTeX (format EasyChair)

---

> *"Sortarea este cea mai fundamentală operațiune în computere — și încă una dintre cele mai interesante."*