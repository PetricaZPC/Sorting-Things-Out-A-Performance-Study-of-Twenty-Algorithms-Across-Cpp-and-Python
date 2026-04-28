// Gnome Sort
#include <vector>
#include <fstream>
#include <iostream>
void gnomeSort(std::vector<int>& arr) {
    int n = arr.size();
    int index = 0;
    while (index < n) {
        if (index == 0 || arr[index] >= arr[index - 1])
            ++index;
        else {
            std::swap(arr[index], arr[index - 1]);
            --index;
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: gnome_sort <input_file> <output_file>\n";
        return 1;
    }
    std::ifstream fin(argv[1]);
    std::vector<int> arr;
    int x;
    while (fin >> x) arr.push_back(x);
    fin.close();
    gnomeSort(arr);
    std::ofstream fout(argv[2]);
    for (int v : arr) fout << v << " ";
    fout.close();
    return 0;
}
