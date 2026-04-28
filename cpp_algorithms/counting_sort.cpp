// Counting Sort (handles negative integers)
#include <vector>
#include <fstream>
#include <iostream>
void countingSort(std::vector<int>& arr) {
    int n = arr.size();
    if (n == 0) return;
    int min_val = arr[0];
    int max_val = arr[0];
    for (int i = 1; i < n; ++i) {
        if (arr[i] < min_val) min_val = arr[i];
        if (arr[i] > max_val) max_val = arr[i];
    }
    int range = max_val - min_val + 1;
    if (range <= 0) return;
    std::vector<int> count(range, 0);
    for (int i = 0; i < n; ++i)
        count[arr[i] - min_val]++;
    int idx = 0;
    for (int i = 0; i < range; ++i)
        while (count[i]-- > 0)
            arr[idx++] = i + min_val;
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: counting_sort <input_file> <output_file>\n";
        return 1;
    }
    std::ifstream fin(argv[1]);
    std::vector<int> arr;
    int x;
    while (fin >> x) arr.push_back(x);
    fin.close();
    countingSort(arr);
    std::ofstream fout(argv[2]);
    for (int v : arr) fout << v << " ";
    fout.close();
    return 0;
}
