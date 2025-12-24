// --- Code by Huyền: Xây dựng các hàm xử lý mê cung ---
// Yêu cầu ngày 6/11: chỉnh sửa thuộc tính maze_data, getCell
#ifndef MAZE_H
#define MAZE_H

#include <iostream>
#include <vector>
#include <string>
#include "point.h"
using namespace std;

class Maze
{
  vector<vector<int>> maze_data; // ma trận số nguyên
  int num_rows, num_cols;        // kích thước mê cung
  Point start_point, end_point;  // điểm bắt đầu & kết thúc

public:
  // Hàm khởi tạo
  Maze();

  // Xử lý dữ liệu
  bool loadFromFile(const string &filename); // đọc dữ liệu từ file
  void print() const;                        // in mê cung ra màn hình ở dạng ma trận ký tự
  bool findStartEnd();                       // tìm điểm bắt đầu (S) và kết thúc (E)

  // Truy cập dữ liệu
  int getRows() const;                // trả về số hàng
  int getCols() const;                // trả về số cột
  Point getStart() const;             // trả về điểm bắt đầu
  Point getEnd() const;               // trả về điểm kết thúc
  int getCell(int x, int y) const;    // trả về ký tự tại vị trí (x, y)
  int cellWeight(int x, int y) const; // trả về trọng số của ô (x, y)
  bool isWall(int x, int y) const;    // trả về true nếu là tường ('#'), false nếu là đường đi

  // Biểu diễn đồ thị
  vector<vector<int>> buildAdjMatrix() const; // Ma trận kề
                                              // vector<vector<pair<int,int>>> buildAdjList(bool weighted=false) const;      // Danh sách kề
};

#endif