## H:The Sierpinski Fractal

&gt; 描述
&gt;
&gt; Consider a regular triangular area, divide it into four equal triangles of half height and remove the one in the middle. Apply the same operation recursively to each of the three remaining triangles. If we repeated this procedure infinite times, we'd obtain something with an area of zero. The fractal that evolves this way is called the Sierpinski Triangle. Although its topological dimension is 2, its Hausdorff-Besicovitch dimension is log(3)/log(2)~1.58, a fractional value (that's why it is called a fractal). By the way, the Hausdorff-Besicovitch dimension of the Norwegian coast is approximately 1.52, its topological dimension being 1.
&gt;
&gt; For this problem, you are to outline the Sierpinski Triangle up to a certain recursion depth, using just ASCII characters. Since the drawing resolution is thus fixed, you'll need to grow the picture appropriately. Draw the smallest triangle (that is not divided any further) with two slashes, to backslashes and two underscores like this:
&gt;
&gt; ```
>  /\
> /__\
> ```
&gt;
&gt; To see how to draw larger triangles, take a look at the sample output.
&gt;
&gt; 输入
&gt;
&gt; The input contains several testcases. Each is specified by an integer n. Input is terminated by n=0. Otherwise 1&lt;=n&lt;=10 indicates the recursion depth.
&gt;
&gt; 输出
&gt;
&gt; For each test case draw an outline of the Sierpinski Triangle with a side's total length of 2n characters. Align your output to the left, that is, print the bottom leftmost slash into the first column. The output must not contain any trailing blanks. Print an empty line after each test case.
&gt;
&gt; 样例输入
&gt;
&gt; ```
> 3
> 2
> 1
> 0
> ```
&gt;
&gt; 样例输出
&gt;
&gt;    ```
>           /\
>          /__\
>         /\  /\
>        /__\/__\
>       /\      /\
>      /__\    /__\
>     /\  /\  /\  /\
>    /__\/__\/__\/__\
>    
>       /\
>      /__\
>     /\  /\
>    /__\/__\
>    
>    
>     /\
>    /__\
>    ```
&gt;
&gt; 
&gt;
&gt; 提示
&gt;
&gt; The Sierpinski-Triangle up to recursion depth 7
&gt;
&gt; 来源
&gt;
&gt; Ulm Local 2002l

```c++
#include <cstring>
#include <iostream>

using namespace std;
char picture[2048][2048]{' '};
void draw(int i, int j, int n) {
  if (n == 1) {
    picture[i][j] = '/';
    picture[i][j + 1] = '_';
    picture[i][j + 2] = '_';
    picture[i][j + 3] = '\\';
    picture[i - 1][j + 1] = '/';
    picture[i - 1][j + 2] = '\\';
  } else {
    int pos = (1 << n);
    draw(i, j, n - 1);
    draw(i, j + pos, n - 1);
    draw(i - pos / 2, j + pos / 2, n - 1);
  }
}
int main() {
  int n;
  while (cin >> n) {
    if (n == 0) {
      break;
    }
    memset(picture, ' ', sizeof(picture));
    int pos = (1 << n);
    draw(pos, 1, n);
    for (int i = 1; i <= pos; i++) {
      for (int j = 1; j <= pos * 2; j++) {
        cout << picture[i][j];
      }
      cout << endl;
    }
  }

  return 0;
}
```
