// Hash Sort (conceptual, uses hash map and sorted keys)
#include <algorithm>
#include <vector>
#include <fstream>
#include <iostream>
#include <unordered_map>
void hashSort(std::vector<int>& arr) {
    std::unordered_map<int, int> hash;
    for (int num : arr)
        hash[num]++;
    std::vector<int> keys;
    keys.reserve(hash.size());
    for (auto& kv : hash)
        keys.push_back(kv.first);
    std::sort(keys.begin(), keys.end());
    int idx = 0;
    for (int key : keys) {
        int count = hash[key];
        for (int i = 0; i < count; ++i)
            arr[idx++] = key;
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: hash_sort <input_file> <output_file>\n";
        return 1;
    }
    std::ifstream fin(argv[1]);
    std::vector<int> arr;
    int x;
    while (fin >> x) arr.push_back(x);
    fin.close();
    hashSort(arr);
    std::ofstream fout(argv[2]);
    for (int v : arr) fout << v << " ";
    fout.close();
    return 0;
}
