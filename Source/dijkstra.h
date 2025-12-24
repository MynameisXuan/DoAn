#ifndef DIJKSTRA_H
#define DIJKSTRA_H

#include <iostream>
#include <vector>
#include <queue>
#include <fstream>
#include <algorithm>

using namespace std;
class Maze;
struct Point;

struct HD
{
  int row, col, dist;
  bool operator>(const HD &other) const { return dist > other.dist; }
};

std::vector<std::pair<int, int>> dijkstra(const Maze &maze);

void Dijkstra(const Maze &maze);
#endif