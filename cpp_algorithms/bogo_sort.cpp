// Bogo Sort (inefficient, for demonstration only)
#include <vector>
#include <algorithm>
#include <random>
#include <fstream>
#include <iostream>
bool isSorted(const std::vector<int>& arr) {
    for (int i = 1; i < arr.size(); ++i)
        if (arr[i] < arr[i - 1]) return false;
    return true;
}
void bogoSort(std::vector<int>& arr) {
    std::random_device rd;
    std::mt19937 g(rd());
    while (!isSorted(arr)) {
        std::shuffle(arr.begin(), arr.end(), g);
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: bogo_sort <input_file> <output_file>\n";
        return 1;
    }
    std::ifstream fin(argv[1]);
    std::vector<int> arr;
    int x;
    while (fin >> x) arr.push_back(x);
    fin.close();
    bogoSort(arr);
    std::ofstream fout(argv[2]);
    for (int v : arr) fout << v << " ";
    fout.close();
    return 0;
}
