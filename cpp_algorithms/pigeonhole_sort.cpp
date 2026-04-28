// Pigeonhole Sort
#include <vector>
#include <fstream>
#include <iostream>
void pigeonholeSort(std::vector<int>& arr) {
    int n = arr.size();
    int min = arr[0], max = arr[0];
    for (int i = 1; i < n; ++i) {
        if (arr[i] < min) min = arr[i];
        if (arr[i] > max) max = arr[i];
    }
    int range = max - min + 1;
    std::vector<int> holes(range, 0);
    for (int i = 0; i < n; ++i)
        holes[arr[i] - min]++;
    int idx = 0;
    for (int i = 0; i < range; ++i)
        while (holes[i]-- > 0)
            arr[idx++] = i + min;
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: pigeonhole_sort <input_file> <output_file>\n";
        return 1;
    }
    std::ifstream fin(argv[1]);
    std::vector<int> arr;
    int x;
    while (fin >> x) arr.push_back(x);
    fin.close();
    pigeonholeSort(arr);
    std::ofstream fout(argv[2]);
    for (int v : arr) fout << v << " ";
    fout.close();
    return 0;
}
