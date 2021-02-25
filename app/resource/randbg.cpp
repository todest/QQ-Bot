#include"svpng.inc"
#include<stdlib.h>
#include<time.h>
#include<vector>
#include<queue>
#define ZOOM(X) ((X * PIXEL) + (X + 1) * WALL)
const int COLS = 1920;
const int ROWS = 1080;
const int PIXEL = 1;
const int WALL = 1;
using namespace std;
int M[ROWS][COLS][5];
int Image[ROWS][COLS];
int Depth[ROWS][COLS];
int Max_Depth = 0;
void Generate_Map() {
	srand(time(NULL));
	int r = 0, c = 0;
	vector<pair<int, int>> history;
	history.push_back(make_pair(r, c));
	while (!history.empty()) {
		M[r][c][4] = 1;
		vector<char> check;
		if (c > 0 && !M[r][c - 1][4]) {
			check.push_back('L');
		}
		if (r > 0 && !M[r - 1][c][4]) {
			check.push_back('U');
		}
		if (c < COLS - 1 && !M[r][c + 1][4]) {
			check.push_back('R');
		}
		if (r < ROWS - 1 && !M[r + 1][c][4]) {
			check.push_back('D');
		}
		if (!check.empty()) {
			history.push_back(make_pair(r, c));
			char move_direction = check[(rand() % check.size())];
			if (move_direction == 'L') {
				M[r][c][0] = 1;
				c = c - 1;
				M[r][c][2] = 1;
			}
			if (move_direction == 'U') {
				M[r][c][1] = 1;
				r = r - 1;
				M[r][c][3] = 1;
			}
			if (move_direction == 'R') {
				M[r][c][2] = 1;
				c = c + 1;
				M[r][c][0] = 1;
			}
			if (move_direction == 'D') {
				M[r][c][3] = 1;
				r = r + 1;
				M[r][c][1] = 1;
			}
		}
		else {
			pair<int, int> p = history.back();
			r = p.first;
			c = p.second;
			history.pop_back();
		}
	}
}
void DFS(int r, int c, int depth) {
	int dir[4][2] = { 0, -1, -1, 0, 0, 1, 1, 0 };
	Depth[r][c] = depth;
	M[r][c][4] = 0;
	for (int i = 0; i < 4; i++) {
		if (!M[r][c][i]) {
			continue;
		}
		int nx = r + dir[i][0];
		int ny = c + dir[i][1];
		if (nx >= 0 && nx < ROWS && ny >= 0 && ny < COLS && M[nx][ny][4]) {
			DFS(nx, ny, depth + 1);
		}
	}
	if (depth > Max_Depth) {
		Max_Depth = depth;
	}
}
void HSVtoRGB(float* r, float* g, float* b, int h, int s, int v)
{
	int i;
	float RGB_min, RGB_max;
	RGB_max = v * 2.55f;
	RGB_min = RGB_max * (100 - s) / 100.0f;

	i = h / 60;
	int difs = h % 60;

	float RGB_Adj = (RGB_max - RGB_min) * difs / 60.0f;

	switch (i) {
	case 0:
		*r = RGB_max;
		*g = RGB_min + RGB_Adj;
		*b = RGB_min;
		break;
	case 1:
		*r = RGB_max - RGB_Adj;
		*g = RGB_max;
		*b = RGB_min;
		break;
	case 2:
		*r = RGB_min;
		*g = RGB_max;
		*b = RGB_min + RGB_Adj;
		break;
	case 3:
		*r = RGB_min;
		*g = RGB_max - RGB_Adj;
		*b = RGB_max;
		break;
	case 4:
		*r = RGB_min + RGB_Adj;
		*g = RGB_min;
		*b = RGB_max;
		break;
	default:
		*r = RGB_max;
		*g = RGB_min;
		*b = RGB_max - RGB_Adj;
		break;
	}
}
void Print_Image() {
	unsigned char rgb[ROWS * COLS * 3], * p = rgb;
	float r, g, b;
	FILE* fp = fopen("rgb.png", "wb");
	for (int i = 0; i < ROWS; i++) {
		for (int j = 0; j < COLS; j++) {
			int Color = Depth[i][j] * 360 / Max_Depth;
			HSVtoRGB(&r, &g, &b, Color, 100, 100);
			*p++ = (unsigned char)r;
			*p++ = (unsigned char)g;
			*p++ = (unsigned char)b;
		}
	}
	svpng(fp, COLS, ROWS, rgb, 0);
	fclose(fp);
}
int main()
{
	Generate_Map();
	DFS(rand() % (ROWS / 2) + ROWS / 4, rand() % (COLS / 2) + COLS / 4, 0);
	Print_Image();
	return 0;
}