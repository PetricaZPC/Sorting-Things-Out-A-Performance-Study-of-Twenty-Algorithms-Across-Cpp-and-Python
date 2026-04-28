// Bucket Sort (integer range-aware)
#include <algorithm>
#include <vector>
#include <fstream>
#include <iostream>
void bucketSort(std::vector<int>& arr) {
    int n = arr.size();
    if (n == 0) return;
    int min_val = arr[0];
    int max_val = arr[0];
    for (int i = 1; i < n; ++i) {
        min_val = std::min(min_val, arr[i]);
        max_val = std::max(max_val, arr[i]);
    }
    if (min_val == max_val) return;
    std::vector<std::vector<int>> buckets(n);
    long long range = static_cast<long long>(max_val) - min_val + 1;
    for (int i = 0; i < n; ++i) {
        int idx = static_cast<int>((static_cast<long long>(arr[i]) - min_val) * (n - 1) / range);
        buckets[idx].push_back(arr[i]);
    }
    for (int i = 0; i < n; ++i)
        std::sort(buckets[i].begin(), buckets[i].end());
    int idx = 0;
    for (int i = 0; i < n; ++i)
        for (int val : buckets[i])
            arr[idx++] = val;
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: bucket_sort <input_file> <output_file>\n";
        return 1;
    }
    std::ifstream fin(argv[1]);
    std::vector<int> arr;
    int x;
    while (fin >> x) arr.push_back(x);
    fin.close();
    bucketSort(arr);
    std::ofstream fout(argv[2]);
    for (int v : arr) fout << v << " ";
    fout.close();
    return 0;
}
