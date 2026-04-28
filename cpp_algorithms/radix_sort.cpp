// Radix Sort (for non-negative integers)
#include <vector>
#include <fstream>
#include <iostream>
int getMax(const std::vector<int>& arr) {
    int mx = arr[0];
    for (int i = 1; i < arr.size(); ++i)
        if (arr[i] > mx)
            mx = arr[i];
    return mx;
}
void countSort(std::vector<int>& arr, int exp) {
    int n = arr.size();
    std::vector<int> output(n);
    int count[10] = {0};
    for (int i = 0; i < n; ++i)
        count[(arr[i] / exp) % 10]++;
    for (int i = 1; i < 10; ++i)
        count[i] += count[i - 1];
    for (int i = n - 1; i >= 0; --i) {
        output[count[(arr[i] / exp) % 10] - 1] = arr[i];
        count[(arr[i] / exp) % 10]--;
    }
    for (int i = 0; i < n; ++i)
        arr[i] = output[i];
}
void radixSort(std::vector<int>& arr) {
    int m = getMax(arr);
    for (int exp = 1; m / exp > 0; exp *= 10)
        countSort(arr, exp);
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: radix_sort <input_file> <output_file>\n";
        return 1;
    }
    std::ifstream fin(argv[1]);
    std::vector<int> arr;
    int x;
    while (fin >> x) arr.push_back(x);
    fin.close();
    radixSort(arr);
    std::ofstream fout(argv[2]);
    for (int v : arr) fout << v << " ";
    fout.close();
    return 0;
}
