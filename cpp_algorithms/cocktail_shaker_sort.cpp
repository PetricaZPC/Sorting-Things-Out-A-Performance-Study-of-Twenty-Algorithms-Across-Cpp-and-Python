// Cocktail Shaker Sort
#include <vector>
#include <fstream>
#include <iostream>
void cocktailShakerSort(std::vector<int>& arr) {
    int n = arr.size();
    bool swapped = true;
    int start = 0, end = n - 1;
    while (swapped) {
        swapped = false;
        for (int i = start; i < end; ++i) {
            if (arr[i] > arr[i + 1]) {
                std::swap(arr[i], arr[i + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;
        swapped = false;
        --end;
        for (int i = end - 1; i >= start; --i) {
            if (arr[i] > arr[i + 1]) {
                std::swap(arr[i], arr[i + 1]);
                swapped = true;
            }
        }
        ++start;
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: cocktail_shaker_sort <input_file> <output_file>\n";
        return 1;
    }
    std::ifstream fin(argv[1]);
    std::vector<int> arr;
    int x;
    while (fin >> x) arr.push_back(x);
    fin.close();
    cocktailShakerSort(arr);
    std::ofstream fout(argv[2]);
    for (int v : arr) fout << v << " ";
    fout.close();
    return 0;
}
