// --- Code by Huyền: Định nghĩa cấu trúc Point để biểu diễn tọa độ trong mê cung ---
#ifndef POINT_H
#define POINT_H

#include <iostream>
using namespace std;

struct Point
{
  int x;
  int y;

  Point(int _x = 0, int _y = 0);
  bool operator==(const Point &p) const;
  friend ostream &operator<<(ostream &os, Point p);
};

inline Point::Point(int x_value, int y_value)
{
  x = x_value;
  y = y_value;
}

inline bool Point::operator==(const Point &point) const
{
  return (x == point.x) && (y == point.y);
}

inline ostream &operator<<(ostream &os, Point point)
{
  os << "(" << point.x << ", " << point.y << ")";
  return os;
}

#endif // POINT_H