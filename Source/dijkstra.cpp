#include "dijkstra.h"
#include "maze.h"
#include <fstream>

vector<pair<int, int>> dijkstra(const Maze &maze)
{
  int rows = maze.getRows(), cols = maze.getCols();
  Point start = maze.getStart();
  Point end = maze.getEnd();
  const int INF = 1e9;

  vector<vector<int>> dist(rows + 1, vector<int>(cols + 1, INF));
  vector<vector<pair<int, int>>> parent(rows + 1, vector<pair<int, int>>(cols + 1, {-1, -1}));

  priority_queue<HD, vector<HD>, greater<HD>> pq;
  dist[start.x][start.y] = 0;
  pq.push({start.x, start.y, 0});

  int dx[4] = {-1, 1, 0, 0};
  int dy[4] = {0, 0, -1, 1};

  while (!pq.empty())
  {
    HD curr = pq.top();
    pq.pop();

    int r = curr.row;
    int c = curr.col;
    int d = curr.dist;

    if (r == end.x && c == end.y)
      break;
    if (d > dist[r][c])
      continue;

    for (int i = 0; i < 4; i++)
    {
      int num_row = r + dx[i];
      int num_col = c + dy[i];
      if (!maze.isWall(num_row, num_col))
      {
        int num_dist = dist[r][c] + 1;
        if (num_dist < dist[num_row][num_col])
        {
          dist[num_row][num_col] = num_dist;
          parent[num_row][num_col] = {r, c};
          pq.push({num_row, num_col, num_dist});
        }
      }
    }
  }

  ofstream out("path.txt");

  if (dist[end.x][end.y] == INF)
  {
    out << "Khong ton tai duong di!\n";
    out.close();
    return {};
  }

  vector<pair<int, int>> path;
  pair<int, int> cur = {end.x, end.y};

  while (cur.first != -1 && cur.second != -1)
  {
    path.push_back(cur);
    cur = parent[cur.first][cur.second];
  }
  reverse(path.begin(), path.end());

  for (int i = 0; i < path.size(); i++)
  {
    pair<int, int> p = path[i];
    out << "(" << p.first << "," << p.second << ")\n";
  }
  out.close();
  return path;
}
