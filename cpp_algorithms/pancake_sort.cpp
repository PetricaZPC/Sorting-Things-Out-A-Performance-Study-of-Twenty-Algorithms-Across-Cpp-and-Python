// Pancake Sort
#include <vector>
#include <fstream>
#include <iostream>
int findMax(const std::vector<int>& arr, int n) {
    int mi = 0;
    for (int i = 1; i < n; ++i)
        if (arr[i] > arr[mi]) mi = i;
    return mi;
}
void flip(std::vector<int>& arr, int i) {
    int start = 0;
    while (start < i) {
        std::swap(arr[start], arr[i]);
        ++start;
        --i;
    }
}
void pancakeSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int curr_size = n; curr_size > 1; --curr_size) {
        int mi = findMax(arr, curr_size);
        if (mi != curr_size - 1) {
            flip(arr, mi);
            flip(arr, curr_size - 1);
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: pancake_sort <input_file> <output_file>\n";
        return 1;
    }
    std::ifstream fin(argv[1]);
    std::vector<int> arr;
    int x;
    while (fin >> x) arr.push_back(x);
    fin.close();
    pancakeSort(arr);
    std::ofstream fout(argv[2]);
    for (int v : arr) fout << v << " ";
    fout.close();
    return 0;
}
