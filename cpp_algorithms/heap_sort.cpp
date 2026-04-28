// Heap Sort
#include <vector>
#include <fstream>
#include <iostream>
void heapify(std::vector<int>& arr, int n, int i) {
    int largest = i;
    int l = 2 * i + 1;
    int r = 2 * i + 2;
    if (l < n && arr[l] > arr[largest])
        largest = l;
    if (r < n && arr[r] > arr[largest])
        largest = r;
    if (largest != i) {
        std::swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}
void heapSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = n / 2 - 1; i >= 0; --i)
        heapify(arr, n, i);
    for (int i = n - 1; i > 0; --i) {
        std::swap(arr[0], arr[i]);
        heapify(arr, i, 0);
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: heap_sort <input_file> <output_file>\n";
        return 1;
    }
    std::ifstream fin(argv[1]);
    std::vector<int> arr;
    int x;
    while (fin >> x) arr.push_back(x);
    fin.close();
    heapSort(arr);
    std::ofstream fout(argv[2]);
    for (int v : arr) fout << v << " ";
    fout.close();
    return 0;
}
