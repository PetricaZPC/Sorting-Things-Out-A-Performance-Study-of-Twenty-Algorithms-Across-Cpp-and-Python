// Bitonic Sort (for powers of 2, parallelizable)
#include <vector>
#include <fstream>
#include <iostream>
#ifdef _OPENMP
#include <omp.h>
#endif
void bitonicMerge(std::vector<int>& arr, int low, int cnt, bool dir) {
    if (cnt > 1) {
        int k = cnt / 2;
        for (int i = low; i < low + k; ++i) {
            if (dir == (arr[i] > arr[i + k]))
                std::swap(arr[i], arr[i + k]);
        }
        bitonicMerge(arr, low, k, dir);
        bitonicMerge(arr, low + k, k, dir);
    }
}
void bitonicSort(std::vector<int>& arr, int low, int cnt, bool dir) {
    if (cnt > 1) {
        int k = cnt / 2;
        #pragma omp task shared(arr) if (cnt > 2048)
        bitonicSort(arr, low, k, true);
        #pragma omp task shared(arr) if (cnt > 2048)
        bitonicSort(arr, low + k, k, false);
        #pragma omp taskwait
        bitonicMerge(arr, low, cnt, dir);
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: bitonic_sort <input_file> <output_file>\n";
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
        bitonicSort(arr, 0, arr.size(), true);
    }
#else
    bitonicSort(arr, 0, arr.size(), true);
#endif
    std::ofstream fout(argv[2]);
    for (int v : arr) fout << v << " ";
    fout.close();
    return 0;
}
