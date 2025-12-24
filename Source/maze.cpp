// --- Code by Huyền: Cài đặt các hàm xử lý mê cung ---
// Yêu cầu ngày 6/11: chỉnh sửa loadFromFile, in mê cung, getCell, findStartEnd(), isWall, cellWeight, buildAdjMatrix
#include "maze.h"
#include <fstream>
using namespace std;

// Hàm khởi tạo
Maze::Maze()
{
  num_rows = 0;
  num_cols = 0;
  start_point = Point(-1, -1);
  end_point = Point(-1, -1);
}

// Đọc dữ liệu mê cung từ file
bool Maze::loadFromFile(const string &filename)
{
  ifstream file_in(filename);
  if (!file_in.is_open())
  {
    cout << "Không thể mở file: " << filename << endl;
    return false;
  }

  // Đọc hàng và cột
  file_in >> num_rows >> num_cols;

  // Bỏ phần còn lại của dòng đầu
  string dummy;
  getline(file_in, dummy);

  maze_data.clear();
  maze_data.push_back(vector<int>());

  // Khởi tạo mê cung rỗng
  for (int i = 1; i <= num_rows; i++)
  {
    vector<int> row(num_cols + 1, 1);
    maze_data.push_back(row);
  }

  // Đọc từng dòng ký tự của mê cung
  for (int i = 1; i <= num_rows; i++)
  {
    for (int j = 1; j <= num_cols; j++)
    {
      int val;
      if (!(file_in >> val)) // nếu đọc thất bại (thiếu dữ liệu, EOF, lỗi định dạng)
      {
        file_in.clear(); // xóa cờ lỗi
        val = 1;         // tự động điền tường
      }

      maze_data[i][j] = val;

      if (val == 2)
        start_point = Point(i, j);
      else if (val == 3)
        end_point = Point(i, j);
    }
  }
  file_in.close();
  return true;
}

// Tìm Start & End
bool Maze::findStartEnd()
{
  bool found_start = false;
  bool found_end = false;

  for (int i = 1; i <= num_rows; i++)
  {
    for (int j = 1; j <= num_cols; j++)
    {
      int cell = maze_data[i][j];
      if (cell == 2)
      {
        start_point = Point(i, j);
        found_start = true;
      }
      if (cell == 3)
      {
        end_point = Point(i, j);
        found_end = true;
      }
    }
  }

  if (!found_start)
  {
    cout << "Không tìm thấy điểm bắt đầu (S) trong mê cung!\n";
  }
  if (!found_end)
  {
    cout << "Không tìm thấy điểm kết thúc (E) trong mê cung!\n";
  }
  return found_start && found_end;
}

// Truy cập dữ liệu
int Maze::getRows() const
{
  return num_rows;
}
int Maze::getCols() const
{
  return num_cols;
}
Point Maze::getStart() const
{
  return start_point;
}
Point Maze::getEnd() const
{
  return end_point;
}

int Maze::getCell(int x, int y) const
{
  if (x < 1 || x > num_rows || y < 1 || y > num_cols)
  {
    cout << "(" << x << "," << y << ") ngoài phạm vi mê cung!\n";
    return 1;
  }
  return maze_data[x][y];
}

int Maze::cellWeight(int x, int y) const
{
  if (isWall(x, y))
  {
    return 0;
  }
  return 1;
}

bool Maze::isWall(int x, int y) const
{
  if (x < 1 || x > num_rows || y < 1 || y > num_cols)
  {
    return true;
  }
  return maze_data[x][y] == 1;
}

// BIỂU DIỄN ĐỒ THỊ: MA TRẬN KỀ

vector<vector<int>> Maze::buildAdjMatrix() const
{
  int total_cells = num_rows * num_cols;
  vector<vector<int>> adj_matrix(total_cells + 1, vector<int>(total_cells + 1, 0));

  // Hướng di chuyển: lên, xuống, trái, phải
  const int delta_x[4] = {-1, 1, 0, 0};
  const int delta_y[4] = {0, 0, -1, 1};

  for (int i = 1; i <= num_rows; i++)
  {
    for (int j = 1; j <= num_cols; j++)
    {
      if (isWall(i, j))
      {
        continue;
      }

      int u = (i - 1) * num_cols + j; // chuyển tọa độ đỉnh (i,j) thành chỉ số u
      for (int k = 0; k < 4; k++)
      {
        int neighbor_x = i + delta_x[k];
        int neighbor_y = j + delta_y[k];

        if (neighbor_x >= 1 && neighbor_x <= num_rows && neighbor_y >= 1 && neighbor_y <= num_cols && !isWall(neighbor_x, neighbor_y))
        {
          int v = (neighbor_x - 1) * num_cols + neighbor_y;
          adj_matrix[u][v] = 1;
        }
      }
    }
  }

  return adj_matrix;
}