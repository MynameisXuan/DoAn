#include <iostream>
#include <string>
#include <vector>
#include <utility>
#include <fstream>
#include "maze.h"
#include "dijkstra.h"
using namespace std;

int main()
{
  Maze maze;

  string filename;
  cin >> filename;

  if (!maze.loadFromFile(filename))
  {
    cout << "Không thể mở file " << filename << endl;
    return 0;
  }

  // Kiểm tra S và E
  if (!maze.findStartEnd())
  {
    cout << "Mê cung không hợp lệ (không tồn tại lối vào hoặc lối ra)!";
    return 0;
  }

  // Chạy Dijkstra
  vector<pair<int, int>> path = dijkstra(maze);

  if (path.empty())
  {
    cout << "Mê cung không có không có đường thoát!" << endl;
    return 0;
  }

  ofstream fout("path.txt");
  if (fout.is_open())
  {
    for (auto &p : path)
    {
      fout << "(" << p.first << "," << p.second << ")\n";
    }
    fout.close();
  }
  else
  {
    cout << "Không thể tạo file path.txt" << endl;
  }

  return 0;
}
// g++ -o main main.cpp maze.cpp dijkstra.cpp
