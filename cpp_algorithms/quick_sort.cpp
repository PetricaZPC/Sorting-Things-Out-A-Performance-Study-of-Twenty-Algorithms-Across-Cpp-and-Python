// Quick Sort
#include <vector>
#include <fstream>
#include <iostream>
#ifdef _OPENMP
#include <omp.h>
#endif
int partition(std::vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; ++j) {
        if (arr[j] < pivot) {
            ++i;
            std::swap(arr[i], arr[j]);
        }
    }
    std::swap(arr[i + 1], arr[high]);
    return i + 1;
}
void quickSort(std::vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        #pragma omp task shared(arr) if (high - low > 10000)
        quickSort(arr, low, pi - 1);
        #pragma omp task shared(arr) if (high - low > 10000)
        quickSort(arr, pi + 1, high);
        #pragma omp taskwait
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: quick_sort <input_file> <output_file>\n";
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
        quickSort(arr, 0, arr.size() - 1);
    }
#else
    quickSort(arr, 0, arr.size() - 1);
#endif
    std::ofstream fout(argv[2]);
    for (int v : arr) fout << v << " ";
    fout.close();
    return 0;
}
