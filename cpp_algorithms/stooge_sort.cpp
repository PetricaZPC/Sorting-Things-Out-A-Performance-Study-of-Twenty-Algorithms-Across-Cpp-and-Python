// Stooge Sort
#include <vector>
#include <fstream>
#include <iostream>
void stoogeSort(std::vector<int>& arr, int l, int h) {
    if (l >= h) return;
    if (arr[l] > arr[h]) std::swap(arr[l], arr[h]);
    if (h - l + 1 > 2) {
        int t = (h - l + 1) / 3;
        stoogeSort(arr, l, h - t);
        stoogeSort(arr, l + t, h);
        stoogeSort(arr, l, h - t);
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: stooge_sort <input_file> <output_file>\n";
        return 1;
    }
    std::ifstream fin(argv[1]);
    std::vector<int> arr;
    int x;
    while (fin >> x) arr.push_back(x);
    fin.close();
    stoogeSort(arr, 0, arr.size() - 1);
    std::ofstream fout(argv[2]);
    for (int v : arr) fout << v << " ";
    fout.close();
    return 0;
}
