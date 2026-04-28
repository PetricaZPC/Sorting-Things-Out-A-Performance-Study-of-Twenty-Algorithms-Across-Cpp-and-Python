// Merge Sort
#include <vector>
#include <fstream>
#include <iostream>
#ifdef _OPENMP
#include <omp.h>
#endif
void merge(std::vector<int>& arr, int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;
    std::vector<int> L(n1), R(n2);
    for (int i = 0; i < n1; ++i)
        L[i] = arr[l + i];
    for (int j = 0; j < n2; ++j)
        R[j] = arr[m + 1 + j];
    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k++] = L[i++];
        } else {
            arr[k++] = R[j++];
        }
    }
    while (i < n1)
        arr[k++] = L[i++];
    while (j < n2)
        arr[k++] = R[j++];
}
void mergeSort(std::vector<int>& arr, int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        #pragma omp task shared(arr) if (r - l > 20000)
        mergeSort(arr, l, m);
        #pragma omp task shared(arr) if (r - l > 20000)
        mergeSort(arr, m + 1, r);
        #pragma omp taskwait
        merge(arr, l, m, r);
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: merge_sort <input_file> <output_file>\n";
        return 1;
    }
    std::ifstream fin(argv[1]);
    std::vector<int> arr;
    int x;
    while (fin >> x) arr.push_back(x);
    fin.close();
#ifdef _OPENMP
    #pragma omp parallel
    {
        #pragma omp single nowait
        mergeSort(arr, 0, arr.size() - 1);
    }
#else
    mergeSort(arr, 0, arr.size() - 1);
#endif
    std::ofstream fout(argv[2]);
    for (int v : arr) fout << v << " ";
    fout.close();
    return 0;
}
