// Comb Sort
#include <vector>
#include <fstream>
#include <iostream>
void combSort(std::vector<int>& arr) {
    int n = arr.size();
    int gap = n;
    bool swapped = true;
    while (gap != 1 || swapped) {
        gap = (gap * 10) / 13;
        if (gap < 1) gap = 1;
        swapped = false;
        for (int i = 0; i < n - gap; ++i) {
            if (arr[i] > arr[i + gap]) {
                std::swap(arr[i], arr[i + gap]);
                swapped = true;
            }
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: comb_sort <input_file> <output_file>\n";
        return 1;
    }
    std::ifstream fin(argv[1]);
    std::vector<int> arr;
    int x;
    while (fin >> x) arr.push_back(x);
    fin.close();
    combSort(arr);
    std::ofstream fout(argv[2]);
    for (int v : arr) fout << v << " ";
    fout.close();
    return 0;
}
