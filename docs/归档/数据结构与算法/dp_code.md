## 动态规划(Hard)

一种通过将复杂问题分解为简单问题从而对复杂问题求解的办法 
具体分为线性和非线性,其中非线性问题适合使用递归函数

***最优性原理***
最优性原理是指“多阶段决策过程的最优决策序列具有这样的性质：不论初始状态和初始决策如何，对于前面决策所造成的某一状态而言，其后各阶段的决策序列必须构成最优策略”。

- 问题抽象化
- 建立模型
- 寻找约束条件
- 判断是否满足最优性原理
- 找大问题与小问题的递推关系式
- 填表
- 寻找解

常见的dp分类

- 线性模型
- 区间dp
- 背包dp
- 数位dp
- 状态压缩dp
- 树状dp

常见的dp优化方法

- 滚动数组优化
- 矩阵乘法优化
- 斜率优化
- 四边形不等式优化
- 决策单调性优化
- 数据结构优化

动态规划问题的具体解决

阶段和阶段变量

- 把问题的全过程恰当的分成若干个相互联系的阶段
 - 阶段的划分一般要根据时间和空间的自然特征去划分
 - 阶段的划分要便于把问题转化为多阶段决策问题

状态和状态变量

- 通常一个阶段包含若干个状态
- 状态可以用变量来描述

决策，决策变量和决策允许集合

策略和最优策略



## 钢条切割问题

&gt; #### 题目描述
&gt;
&gt; Serling公司购买长钢条，将其切割为短钢条出售。切割工序本身没有成本支出。公司管理层希望知道最佳的切割方案。假定我们知道Serling公司出售一段长为i英寸的钢条的价格为pi(i=1,2,…，单位为美元)。钢条的长度均为整英寸。
&gt;
&gt; 给定一段长度为n英寸的钢条和一个价格表pi(i=1,2,…n)，求切割钢条方案，使得销售收益rn最大。
&gt;
&gt; #### 关于输入
&gt;
&gt; 第一行：n，表示购买的长钢条的长度。
&gt; 接下来一行包含 n 个数字，第 i 个数字出售长为 i 的钢条的价格，即 pi。
&gt;
&gt; 其中 0 &lt; n &lt;= 3000，0 &lt; pi &lt;= 10000。
&gt;
&gt; #### 关于输出
&gt;
&gt; 输出仅一行，为最大的销售收益值 rn。
&gt;
&gt; #### 例子输入
&gt;
&gt; ```
&gt; 7
&gt; 1 5 8 9 10 17 17
&gt; ```
&gt;
&gt; #### 例子输出
&gt;
&gt; ```
&gt; 18
&gt; ```
&gt;
&gt; #### 提示信息
&gt;
&gt; 注意，如果长度为n英寸的钢条的价格pn足够大，最优解可能就是完全不需要切割。

```c++
#include <iostream>
#include <vector>
using namespace std;
int main() {
  int n;
  cin &gt;&gt; n;
  vector<int> price(n + 1, 0);
  for (int i = 1; i &lt;= n; i++) {
    cin &gt;&gt; price[i];
  }
  vector<int> dp(n + 1, 0);
  dp[1] = price[1];
  for (int i = 2; i &lt;= n; i++) {
    for (int j = 1; j &lt; i; j++) {
      dp[i] = max(dp[i], dp[i - j] + price[j]);
    }
  }
  cout &lt;&lt; dp[n] &lt;&lt; endl;
  return 0;
}
```

## 木材切割

&gt; 描述
&gt;
&gt; 有一根长度为n的木材（n为不大于100的正整数），要将其切割为m（0 &lt; m &lt; n) 段出售，每段均为正整数长度。不同长度的木材具有不同的售价p（0 &lt; p &lt; 100)。求一个最优的切割方案，以尽可能卖出更多的钱。
&gt;
&gt;  
&gt;
&gt; 输入
&gt;
&gt; 第一行为n
&gt;
&gt; 第二行为m
&gt;
&gt; 第三行包含 n 个数字，第 i 个数字出售长为 i 的木材的价格，用空格隔开
&gt;
&gt; 输出
&gt;
&gt; 最大的总售价。
&gt;
&gt; 样例输入
&gt;
&gt; ```
&gt; 7
&gt; 2
&gt; 1 5 8 9 10 17 17
&gt; ```
&gt;
&gt; 样例输出
&gt;
&gt; ```
&gt; 18
&gt; ```

```c++
#include <iostream>
#include <vector>
using namespace std;
int main() {
  int n, m;
  cin &gt;&gt; n &gt;&gt; m;
  vector<int> price(n + 1, 0);
  for (int i = 1; i &lt;= n; i++) {
    cin &gt;&gt; price[i];
  }
  vector<vector<int>&gt; dp(m + 1, vector<int>(n + 1, 0));
  for (int i = 1; i &lt;= n; i++) {
    dp[1][i] = price[i];
  }
  for (int i = 2; i &lt;= m; i++) {
    for (int j = 1; j &lt;= n; j++) {
      for (int k = 0; k &lt; j; k++) {
        dp[i][j] = max(dp[i][j], dp[i - 1][k] + price[j - k]);
      }
    }
  }
  cout &lt;&lt; dp[m][n] &lt;&lt; endl;
  return 0;
}
```

## [最长递增子序列](https://leetcode.cn/problems/longest-increasing-subsequence/)

&gt; 给你一个整数数组 `nums` ，找到其中最长严格递增子序列的长度。
&gt;
&gt; **子序列** 是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。例如，`[3,6,2,7]` 是数组 `[0,3,1,6,2,2,7]` 的子序列。
&gt;
&gt; **示例 1：**
&gt;
&gt; ```
&gt; 输入：nums = [10,9,2,5,3,7,101,18]
&gt; 输出：4
&gt; 解释：最长递增子序列是 [2,3,7,101]，因此长度为 4 。
&gt; ```
&gt;
&gt; **示例 2：**
&gt;
&gt; ```
&gt; 输入：nums = [0,1,0,3,2,3]
&gt; 输出：4
&gt; ```
&gt;
&gt; **示例 3：**
&gt;
&gt; ```
&gt; 输入：nums = [7,7,7,7,7,7,7]
&gt; 输出：1
&gt; ```

```c++
class Solution {

public:
    int lengthOfLIS(vector<int>&amp; nums) {
        vector<int> dp(nums.size(), 1); // 记录以num[i]为结尾的最长子序列的长度
        for (int i = 1; i &lt; nums.size(); i++) {
            for (int j = 0; j &lt; i; j++) {
                if (nums[i] &gt; nums[j]) {
                    dp[i] = max(dp[i], dp[j] + 1);
                }
            }
        }
        return *(max_element(dp.begin(),dp.end()));
    }
};
```

## [32. 最长有效括号](https://leetcode.cn/problems/longest-valid-parentheses/)

&gt; 给你一个只包含 `'('` 和 `')'` 的字符串，找出最长有效（格式正确且连续）括号
&gt;
&gt; 子串的长度。 
&gt;
&gt; **示例 1：**
&gt;
&gt; ```
&gt; 输入：s = "(()"
&gt; 输出：2
&gt; 解释：最长有效括号子串是 "()"
&gt; ```
&gt;
&gt; **示例 2：**
&gt;
&gt; ```
&gt; 输入：s = ")()())"
&gt; 输出：4
&gt; 解释：最长有效括号子串是 "()()"
&gt; ```
&gt;
&gt; **示例 3：**
&gt;
&gt; ```
&gt; 输入：s = ""
&gt; 输出：0
&gt; ```
&gt;
&gt; 
&gt;
&gt; **提示：**
&gt;
&gt; - `0 &lt;= s.length &lt;= 3 * 104`
&gt; - `s[i]` 为 `'('` 或 `')'`
&gt; - ==转化为容易解决的形式==

```c++
class Solution {

public:
    int longestValidParentheses(string s) {
        stack<pair<char, int="">&gt; space;
        vector<int> count(s.size(), 0);
        for (int i = 0; i &lt; s.size(); i++) {
            if (space.empty()) {
                space.push(make_pair(s[i], i));
            } else {
                if (s[i] == ')' &amp;&amp; space.top().first == '(') {
                    count[i] = 1;
                    count[space.top().second] = 1;
                    space.pop();
                } else {
                    space.push(make_pair(s[i], i));
                }
            }
        }
        int max_count = 0, current_count = 0;
        for (int i = 0; i &lt; s.size(); i++) {
            if (count[i] == 0) {
                max_count = max(max_count, current_count);
                current_count = 0;
            } else {
                current_count++;
            }
        }
        return max(max_count, current_count);
    }
};
```

## [AcWing 01背包问题](https://www.acwing.com/problem/content/2/)

&gt; 有 N𝑁 件物品和一个容量是 V𝑉 的背包。每件物品只能使用一次。
&gt;
&gt; 第 i𝑖 件物品的体积是 vi𝑣𝑖，价值是 wi𝑤𝑖。
&gt;
&gt; 求解将哪些物品装入背包，可使这些物品的总体积不超过背包容量，且总价值最大。
&gt; 输出最大价值。
&gt;
&gt; #### 输入格式
&gt;
&gt; 第一行两个整数，N，V𝑁，𝑉，用空格隔开，分别表示物品数量和背包容积。
&gt;
&gt; 接下来有 N𝑁 行，每行两个整数 vi,wi𝑣𝑖,𝑤𝑖，用空格隔开，分别表示第 i𝑖 件物品的体积和价值。
&gt;
&gt; #### 输出格式
&gt;
&gt; 输出一个整数，表示最大价值。
&gt;
&gt; #### 数据范围
&gt;
&gt; 0<n,v≤10000<𝑁,𝑉≤1000> 0<vi,wi≤10000<𝑣𝑖,𝑤𝑖≤1000>
&gt; #### 输入样例
&gt;
&gt; ```
&gt; 4 5
&gt; 1 2
&gt; 2 4
&gt; 3 4
&gt; 4 5
&gt; ```
&gt;
&gt; #### 输出样例：
&gt;
&gt; ```
&gt; 8
&gt; ```

```c++
```

## [Luogu P2925干草出售](https://www.luogu.org/problemnew/show/P2925)

&gt; 农民 John 面临一个很可怕的事，因为防范力度不大所以他存储的所有稻草都被蟑螂吃光了，他将面临没有稻草喂养奶牛的局面。在奶牛断粮之前，John 拉着他的马车到农民 Don 的农场中买一些稻草给奶牛过冬。已知 John 的马车可以装的下 𝐶(1≤𝐶≤5×104)*C*(1≤*C*≤5×104) 立方的稻草。
&gt;
&gt; 农民 Don 有 𝐻(1≤𝐻≤5×103)*H*(1≤*H*≤5×103) 捆体积不同的稻草可供购买，每一捆稻草有它自己的体积 𝑉𝑖(1≤𝑉𝑖≤𝐶)*V**i*(1≤*V**i*≤*C*)。面对这些稻草 John 认真的计算如何充分利用马车的空间购买尽量多的稻草给他的奶牛过冬。
&gt;
&gt; 现在给定马车的最大容积 𝐶*C* 和每一捆稻草的体积 𝑉𝑖*V**i*，John 如何在不超过马车最大容积的情况下买到最大体积的稻草？他不可以把一捆稻草分开来买。

```c++
#include <iostream>
#include <vector>
using namespace std;
int main() {
  int c, h;
  cin &gt;&gt; c &gt;&gt; h;
  vector<int> v(h, 0);
  for (int i = 0; i &lt; h; i++) {
    cin &gt;&gt; v[i];
  }
  vector<int> dp(c + 1, 0);
  for (int i = 0; i &lt; h; i++) {
    for (int j = c; j &gt;= v[i]; j--) {
      dp[j] = max(dp[j], dp[j - v[i]] + v[i]);
    }
  }
  cout &lt;&lt; dp[c] &lt;&lt; endl;
  return 0;
}
```

## [Luogu P1048 采药](https://www.luogu.org/problemnew/show/P1048)

&gt; ## 题目描述
&gt;
&gt; 辰辰是个天资聪颖的孩子，他的梦想是成为世界上最伟大的医师。为此，他想拜附近最有威望的医师为师。医师为了判断他的资质，给他出了一个难题。医师把他带到一个到处都是草药的山洞里对他说：“孩子，这个山洞里有一些不同的草药，采每一株都需要一些时间，每一株也有它自身的价值。我会给你一段时间，在这段时间里，你可以采到一些草药。如果你是一个聪明的孩子，你应该可以让采到的草药的总价值最大。”
&gt;
&gt; 如果你是辰辰，你能完成这个任务吗？
&gt;
&gt; ## 输入格式
&gt;
&gt; 第一行有 22 个整数 𝑇*T*（1≤𝑇≤10001≤*T*≤1000）和 𝑀*M*（1≤𝑀≤1001≤*M*≤100），用一个空格隔开，𝑇*T* 代表总共能够用来采药的时间，𝑀*M* 代表山洞里的草药的数目。
&gt;
&gt; 接下来的 𝑀*M* 行每行包括两个在 11 到 100100 之间（包括 11 和 100100）的整数，分别表示采摘某株草药的时间和这株草药的价值。
&gt;
&gt; ## 输出格式
&gt;
&gt; 输出在规定的时间内可以采到的草药的最大总价值。
&gt;
&gt; ## 输入输出样例
&gt;
&gt; **输入 #1**复制
&gt;
&gt; ```
&gt; 70 3
&gt; 71 100
&gt; 69 1
&gt; 1 2
&gt; ```
&gt;
&gt; **输出 #1**复制
&gt;
&gt; ```
&gt; 3
&gt; ```
&gt;
&gt; ## 说明/提示
&gt;
&gt; **【数据范围】**
&gt;
&gt; - 对于 30%30% 的数据，𝑀≤10*M*≤10；
&gt; - 对于全部的数据，𝑀≤100*M*≤100。

```c++
```

## [AcWing 完全背包问题](https://www.acwing.com/problem/content/3/)

&gt; 有 N种物品和一个容量是 V的背包，每种物品都有无限件可用。
&gt;
&gt; 第 i种物品的体积是 vi，价值是 wi。
&gt;
&gt; 求解将哪些物品装入背包，可使这些物品的总体积不超过背包容量，且总价值最大。
&gt; 输出最大价值。
&gt;
&gt; #### 输入格式
&gt;
&gt; 第一行两个整数，N，V，用空格隔开，分别表示物品种数和背包容积。
&gt;
&gt; 接下来有 N 行，每行两个整数 vi,wi用空格隔开，分别表示第 i种物品的体积和价值。
&gt;
&gt; #### 输出格式
&gt;
&gt; 输出一个整数，表示最大价值。
&gt;
&gt; #### 数据范围
&gt;
&gt; 0<n,v≤1000> 0<vi,wi≤1000>
&gt; #### 输入样例
&gt;
&gt; ```
&gt; 4 5
&gt; 1 2
&gt; 2 4
&gt; 3 4
&gt; 4 5
&gt; ```
&gt;
&gt; #### 输出样例：
&gt;
&gt; ```
&gt; 10
&gt; ```

```c++
#include <algorithm>
#include <cmath>
#include <iostream>
#include <vector>

using namespace std;

int main() {
  int n, av;
  cin &gt;&gt; n &gt;&gt; av;
  vector<int> v(n, 0);
  vector<int> w(n, 0);
  for (int i = 0; i &lt; n; i++) {
    cin &gt;&gt; v[i] &gt;&gt; w[i];
  }
  vector<int> dp(av + 1, 0);
  for (int i = 0; i &lt; n; i++) {
    for (int j = v[i]; j &lt;= av; j++) {
      dp[j] = max(dp[j], dp[j - v[i]] + w[i]);
    }
  }
  cout &lt;&lt; dp[av] &lt;&lt; endl;
  return 0;
}
```

## [Luogu P1853投资的最大效益](https://www.luogu.org/problemnew/show/P1853#sub)

==TLE==

&gt; ## 题目背景
&gt;
&gt; 约翰先生获得了一大笔遗产，他暂时还用不上这一笔钱，他决定进行投资以获得更大的效益。银行工作人员向他提供了多种债券，每一种债券都能在固定的投资后，提供稳定的年利息。当然，每一种债券的投资额是不同的，一般来说，投资越大，收益也越大，而且，每一年还可以根据资金总额的增加，更换收益更大的债券。
&gt;
&gt; ## 题目描述
&gt;
&gt; 例如：有如下两种不同的债券：
&gt;
&gt; 1. 投资额 $4000$4000，年利息 $400$400；
&gt; 2. 投资额 $3000$3000，年利息 $250$250。
&gt;
&gt; 初始时，有 $10000$10000 的总资产，可以投资两份债券 1 债券，一年获得 $800$800 的利息；而投资一份债券 1 和两份债券 2，一年可获得 $900$900 的利息，两年后，可获得 $1800$1800 的利息；而所有的资产达到 $11800$11800，然后将卖掉一份债券 2，换购债券 1，年利息可达到 $1050$1050；第三年后，总资产达到 $12850$12850，可以购买三份债券 1，年利息可达到 $1200$1200，第四年后，总资产可达到 $14050$14050。
&gt;
&gt; 现给定若干种债券、最初的总资产，帮助约翰先生计算，经过 𝑛*n* 年的投资，总资产的最大值。
&gt;
&gt; ## 输入格式
&gt;
&gt; 第一行为三个正整数 𝑠,𝑛,𝑑*s*,*n*,*d*，分别表示最初的总资产、年数和债券的种类。
&gt;
&gt; 接下来 𝑑*d* 行，每行表示一种债券，两个正整数 𝑎,𝑏*a*,*b* 分别表示债券的投资额和年利息。
&gt;
&gt; ## 输出格式
&gt;
&gt; 仅一个整数，表示 𝑛*n* 年后的最大总资产。
&gt;
&gt; ## 输入输出样例
&gt;
&gt; **输入 #1**复制
&gt;
&gt; ```
&gt; 10000 4 2
&gt; 4000 400
&gt; 3000 250
&gt; ```
&gt;
&gt; **输出 #1**复制
&gt;
&gt; ```
&gt; 14050
&gt; ```
&gt;
&gt; ## 说明/提示
&gt;
&gt; 对于 100%100% 的数据，1≤𝑠≤1061≤*s*≤106，2≤𝑛≤402≤*n*≤40，1≤𝑑≤101≤*d*≤10，1≤𝑎≤1041≤*a*≤104，且 𝑎*a* 是 10001000 的倍数，𝑏*b* 不超过 𝑎*a* 的 10%10%。

```c++
#include <algorithm>
#include <cmath>
#include <iostream>
#include <vector>

using namespace std;

int main() {
  int amount, year, kind;
  cin &gt;&gt; amount &gt;&gt; year &gt;&gt; kind;

  vector<int> cost(kind, 0);
  vector<int> reward(kind, 0);

  for (int i = 0; i &lt; kind; i++) {
    cin &gt;&gt; cost[i] &gt;&gt; reward[i];
  }
  while (year--) {
    vector<int> dp(amount + 1, 0);
    for (int i = 0; i &lt; kind; i++) {
      for (int j = cost[i]; j &lt;= amount; j++) {
        dp[j] = max(dp[j], dp[j - cost[i]] + reward[i]);
      }
    }
    amount += dp[amount];
  }
  cout &lt;&lt; amount &lt;&lt; endl;
  return 0;
}
```

## [Luogu P1776宝物筛选](https://www.luogu.org/problemnew/show/P1776)

&gt; ## 题目描述
&gt;
&gt; 终于，破解了千年的难题。小 FF 找到了王室的宝物室，里面堆满了无数价值连城的宝物。
&gt;
&gt; 这下小 FF 可发财了，嘎嘎。但是这里的宝物实在是太多了，小 FF 的采集车似乎装不下那么多宝物。看来小 FF 只能含泪舍弃其中的一部分宝物了。
&gt;
&gt; 小 FF 对洞穴里的宝物进行了整理，他发现每样宝物都有一件或者多件。他粗略估算了下每样宝物的价值，之后开始了宝物筛选工作：小 FF 有一个最大载重为 𝑊*W* 的采集车，洞穴里总共有 𝑛*n* 种宝物，每种宝物的价值为 𝑣𝑖*v**i*，重量为 𝑤𝑖*w**i*，每种宝物有 𝑚𝑖*m**i* 件。小 FF 希望在采集车不超载的前提下，选择一些宝物装进采集车，使得它们的价值和最大。
&gt;
&gt; ## 输入格式
&gt;
&gt; 第一行为一个整数 𝑛*n* 和 𝑊*W*，分别表示宝物种数和采集车的最大载重。
&gt;
&gt; 接下来 𝑛*n* 行每行三个整数 𝑣𝑖,𝑤𝑖,𝑚𝑖*v**i*,*w**i*,*m**i*。
&gt;
&gt; ## 输出格式
&gt;
&gt; 输出仅一个整数，表示在采集车不超载的情况下收集的宝物的最大价值。
&gt;
&gt; ## 输入输出样例
&gt;
&gt; **输入**
&gt;
&gt; ```
&gt; 4 20
&gt; 3 9 3
&gt; 5 9 1
&gt; 9 4 2
&gt; 8 1 3
&gt; ```
&gt;
&gt; **输出**
&gt;
&gt; ```
&gt; 47
&gt; ```
&gt;
&gt; ## 说明/提示
&gt;
&gt; 对于 30%30% 的数据，𝑛≤∑𝑚𝑖≤104*n*≤∑*m**i*≤104，0≤𝑊≤1030≤*W*≤103。
&gt;
&gt; 对于 100%100% 的数据，𝑛≤∑𝑚𝑖≤105*n*≤∑*m**i*≤105，0≤𝑊≤4×1040≤*W*≤4×104，1≤𝑛≤1001≤*n*≤100。

```c++
#include <iostream>
#include <vector>
using namespace std;
int main() {
  int w, n;
  cin &gt;&gt; n &gt;&gt; w;
  vector<int> weight(n, 0);
  vector<int> value(n, 0);
  vector<int> number(n, 0);
  vector<int> dp(w + 1, 0);
  for (int i = 0; i &lt; n; i++) {
    cin &gt;&gt; value[i] &gt;&gt; weight[i] &gt;&gt; number[i];
  }
  for (int i = 0; i &lt; n; i++) {
    int k = 1, an = number[i];
    int t_weight = k * weight[i], t_value = k * value[i];
    while (k &lt; an) { // 二进制逼近
      t_weight = k * weight[i], t_value = k * value[i];
      for (int l = w; l &gt;= t_weight; l--) {
        dp[l] = max(dp[l], dp[l - t_weight] + t_value);
      }
      an = an - k;
      k *= 2;
    }
    t_weight = an * weight[i], t_value = an * value[i];
    for (int l = w; l &gt;= t_weight; l--) {
      dp[l] = max(dp[l], dp[l - t_weight] + t_value);
    }
  }
  cout &lt;&lt; dp[w] &lt;&lt; endl;
  return 0;
}
```

## [Ⅰ（普通多重背包）](https://www.acwing.com/problem/content/4/)

&gt; 有 N种物品和一个容量是 V 的背包。
&gt;
&gt; 第 i𝑖 种物品最多有 si件，每件体积是 vi，价值是 wi。
&gt;
&gt; 求解将哪些物品装入背包，可使物品体积总和不超过背包容量，且价值总和最大。
&gt; 输出最大价值。
&gt;
&gt; #### 输入格式
&gt;
&gt; 第一行两个整数，N，V，𝑉，用空格隔开，分别表示物品种数和背包容积。
&gt;
&gt; 接下来有 N 行，每行三个整数 vi,wi,si用空格隔开，分别表示第 i𝑖 种物品的体积、价值和数量。
&gt;
&gt; #### 输出格式
&gt;
&gt; 输出一个整数，表示最大价值。
&gt;
&gt; #### 数据范围
&gt;
&gt; 0<n,v≤100> 0<vi,wi,si≤100>
&gt; #### 输入样例
&gt;
&gt; ```
&gt; 4 5
&gt; 1 2 3
&gt; 2 4 1
&gt; 3 4 3
&gt; 4 5 2
&gt; ```
&gt;
&gt; #### 输出样例：
&gt;
&gt; ```
&gt; 10
&gt; ```

```c++
```

## [Ⅱ（二进制优化）](https://www.acwing.com/problem/content/5/)

&gt; 有 N𝑁 种物品和一个容量是 V𝑉 的背包。
&gt;
&gt; 第 i𝑖 种物品最多有 si件，每件体积是 vi，价值是 wi。
&gt;
&gt; 求解将哪些物品装入背包，可使物品体积总和不超过背包容量，且价值总和最大。
&gt; 输出最大价值。
&gt;
&gt; #### 输入格式
&gt;
&gt; 第一行两个整数，N，V，𝑉，用空格隔开，分别表示物品种数和背包容积。
&gt;
&gt; 接下来有 N 行，每行三个整数 $vi,wi,si$用空格隔开，分别表示第 i 种物品的体积、价值和数量。
&gt;
&gt; #### 输出格式
&gt;
&gt; 输出一个整数，表示最大价值。
&gt;
&gt; #### 数据范围
&gt;
&gt; $0<n≤1000$> $0<v≤2000$> $0<vi,wi,si≤20000$>
&gt; ##### 提示：
&gt;
&gt; 本题考查多重背包的二进制优化方法。
&gt;
&gt; #### 输入样例
&gt;
&gt; ```
&gt; 4 5
&gt; 1 2 3
&gt; 2 4 1
&gt; 3 4 3
&gt; 4 5 2
&gt; ```
&gt;
&gt; #### 输出样例：
&gt;
&gt; ```
&gt; 10
&gt; ```

```c++

```

## [Ⅲ（单调队列优化）](https://www.acwing.com/problem/content/6/)

&gt; 有 N𝑁 种物品和一个容量是 V𝑉 的背包。
&gt;
&gt; 第 i𝑖 种物品最多有 si𝑠𝑖 件，每件体积是 vi𝑣𝑖，价值是 wi𝑤𝑖。
&gt;
&gt; 求解将哪些物品装入背包，可使物品体积总和不超过背包容量，且价值总和最大。
&gt; 输出最大价值。
&gt;
&gt; #### 输入格式
&gt;
&gt; 第一行两个整数，N，V(0<n≤1000, 0<v≤20000)，用空格隔开，分别表示物品种数和背包容积。="">
&gt; 接下来有 N𝑁 行，每行三个整数 vi,wi,si，用空格隔开，分别表示第 i 种物品的体积、价值和数量。
&gt;
&gt; #### 输出格式
&gt;
&gt; 输出一个整数，表示最大价值。
&gt;
&gt; #### 数据范围
&gt;
&gt; 0<n≤1000> 0<v≤20000> 0<vi,wi,si≤20000>
&gt; ##### 提示
&gt;
&gt; 本题考查多重背包的单调队列优化方法。
&gt;
&gt; #### 输入样例
&gt;
&gt; ```
&gt; 4 5
&gt; 1 2 3
&gt; 2 4 1
&gt; 3 4 3
&gt; 4 5 2
&gt; ```
&gt;
&gt; #### 输出样例：
&gt;
&gt; ```
&gt; 10
&gt; ```

```c++

```

## [AcWing 混合背包问题](https://www.acwing.com/problem/content/7/)

&gt; 有 N𝑁 种物品和一个容量是 V𝑉 的背包。
&gt;
&gt; 物品一共有三类：
&gt;
&gt; - 第一类物品只能用1次（01背包）；
&gt; - 第二类物品可以用无限次（完全背包）；
&gt; - 第三类物品最多只能用 si 次（多重背包）；
&gt;
&gt; 每种体积是 vi，价值是 wi。
&gt;
&gt; 求解将哪些物品装入背包，可使物品体积总和不超过背包容量，且价值总和最大。
&gt; 输出最大价值。
&gt;
&gt; #### 输入格式
&gt;
&gt; 第一行两个整数，N，V用空格隔开，分别表示物品种数和背包容积。
&gt;
&gt; 接下来有 N𝑁 行，每行三个整数 vi,wi,si用空格隔开，分别表示第 i𝑖 种物品的体积、价值和数量。
&gt;
&gt; - si=−1 表示第 i种物品只能用1次；
&gt; - si=0 表示第 i种物品可以用无限次；
&gt; - si&gt;0 表示第 i 种物品可以使用 si 次；
&gt;
&gt; #### 输出格式
&gt;
&gt; 输出一个整数，表示最大价值。
&gt;
&gt; #### 数据范围
&gt;
&gt; 0<n,v≤1000> 0<vi,wi≤1000> −1≤si≤1000
&gt;
&gt; #### 输入样例
&gt;
&gt; ```
&gt; 4 5
&gt; 1 2 -1
&gt; 2 4 1
&gt; 3 4 0
&gt; 4 5 2
&gt; ```
&gt;
&gt; #### 输出样例：
&gt;
&gt; ```
&gt; 8
&gt; ```

```c++
#include <iostream>
#include <vector>
using namespace std;

int main() {
  int n, v;
  cin &gt;&gt; n &gt;&gt; v;
  vector<int> cost(n, 0);
  vector<int> value(n, 0);
  vector<int> number(n, 0);
  vector<int> dp(v + 1, 0);

  for (int i = 0; i &lt; n; i++) {
    cin &gt;&gt; cost[i] &gt;&gt; value[i] &gt;&gt; number[i];
  }

  for (int i = 0; i &lt; n; i++) {
    if (number[i] == -1) { // 01背包
      for (int j = v; j &gt;= cost[i]; j--) {
        dp[j] = max(dp[j], dp[j - cost[i]] + value[i]);
      }
    } else if (number[i] == 0) { // 完全背包
      for (int j = cost[i]; j &lt;= v; j++) {
        dp[j] = max(dp[j], dp[j - cost[i]] + value[i]);
      }
    } else { // 多重背包
      int k = 1, an = number[i];
      int t_cost = k * cost[i], t_value = k * value[i];
      while (k &lt; an) {
        t_cost = k * cost[i], t_value = k * value[i];
        for (int l = v; l &gt;= t_cost; l--) {
          dp[l] = max(dp[l], dp[l - t_cost] + t_value);
        }
        an = an - k;
        k *= 2;
      }
      t_cost = an * cost[i], t_value = an * value[i];
      for (int l = v; l &gt;= t_cost; l--) {
        dp[l] = max(dp[l], dp[l - t_cost] + t_value);
      }
    }
  }

  cout &lt;&lt; dp[v] &lt;&lt; endl;
  return 0;
}
```

## [Luogu P1833樱花](https://www.luogu.org/problemnew/show/P1833)

&gt; ## 题目背景
&gt;
&gt; 《爱与愁的故事第四弹·plant》第一章。
&gt;
&gt; ## 题目描述
&gt;
&gt; 爱与愁大神后院里种了 𝑛*n* 棵樱花树，每棵都有美学值 𝐶𝑖(0≤𝐶𝑖≤200)*C**i*(0≤*C**i*≤200)。爱与愁大神在每天上学前都会来赏花。爱与愁大神可是生物学霸，他懂得如何欣赏樱花：一种樱花树看一遍过，一种樱花树最多看 𝑃𝑖(0≤𝑃𝑖≤100)*P**i*(0≤*P**i*≤100) 遍，一种樱花树可以看无数遍。但是看每棵樱花树都有一定的时间 𝑇𝑖(0≤𝑇𝑖≤100)*T**i*(0≤*T**i*≤100)。爱与愁大神离去上学的时间只剩下一小会儿了。求解看哪几棵樱花树能使美学值最高且爱与愁大神能准时（或提早）去上学。
&gt;
&gt; ## 输入格式
&gt;
&gt; 共 𝑛+1*n*+1行：
&gt;
&gt; 第 11 行：现在时间 𝑇𝑠*T**s*（几时：几分），去上学的时间 𝑇𝑒*T**e*（几时：几分），爱与愁大神院子里有几棵樱花树 𝑛*n*。这里的 𝑇𝑠*T**s*，𝑇𝑒*T**e* 格式为：`hh:mm`，其中 0≤ℎℎ≤230≤*h**h*≤23，0≤𝑚𝑚≤590≤*m**m*≤59，且 ℎℎ,𝑚𝑚,𝑛*h**h*,*m**m*,*n* 均为正整数。
&gt;
&gt; 第 22 行到第 𝑛+1*n*+1 行，每行三个正整数：看完第 𝑖*i* 棵树的耗费时间 𝑇𝑖*T**i*，第 𝑖*i* 棵树的美学值 𝐶𝑖*C**i*，看第 𝑖*i* 棵树的次数 𝑃𝑖*P**i*（𝑃𝑖=0*P**i*=0 表示无数次，𝑃𝑖*P**i* 是其他数字表示最多可看的次数 𝑃𝑖*P**i*）。
&gt;
&gt; ## 输出格式
&gt;
&gt; 只有一个整数，表示最大美学值。
&gt;
&gt; ## 输入输出样例
&gt;
&gt; **输入 #1**复制
&gt;
&gt; ```
&gt; 6:50 7:00 3
&gt; 2 1 0
&gt; 3 3 1
&gt; 4 5 4
&gt; ```
&gt;
&gt; **输出 #1**复制
&gt;
&gt; ```
&gt; 11
&gt; ```
&gt;
&gt; ## 说明/提示
&gt;
&gt; 100%100% 数据：𝑇𝑒−𝑇𝑠≤1000*T**e*−*T**s*≤1000（即开始时间距离结束时间不超过 10001000 分钟），𝑛≤10000*n*≤10000。保证 𝑇𝑒,𝑇𝑠*T**e*,*T**s* 为同一天内的时间。
&gt;
&gt; 样例解释：赏第一棵樱花树一次，赏第三棵樱花树 22 次。

```c++
#include <iostream>
#include <sstream>
#include <vector>
using namespace std;

int main() {
  int h1, h2, m1, m2, t;
  char a1, a2;
  cin &gt;&gt; h1 &gt;&gt; a1 &gt;&gt; m1;
  cin &gt;&gt; h2 &gt;&gt; a2 &gt;&gt; m2;
  t = h2 * 60 + m2 - (h1 * 60 + m1);

  int n;
  cin &gt;&gt; n;
  vector<int> cost(n, 0);
  vector<int> value(n, 0);
  vector<int> number(n, 0);
  vector<int> dp(t + 1, 0);

  for (int i = 0; i &lt; n; i++) {
    cin &gt;&gt; cost[i] &gt;&gt; value[i] &gt;&gt; number[i];
  }

  for (int i = 0; i &lt; n; i++) {
    if (number[i]) {
      for (int j = t; j &gt;= 0; j--) {
        for (int k = 0; k &lt;= number[i]; k++) {
          if (j &gt;= k * cost[i]) {
            dp[j] = max(dp[j], dp[j - k * cost[i]] + value[i] * k);
          }
        }
      }
    } else {
      for (int j = t; j &gt;= 0; j--) {
        for (int k = 0; k &lt;= j / cost[i]; k++) {
          if (j &gt;= k * cost[i]) {
            dp[j] = max(dp[j], dp[j - k * cost[i]] + value[i] * k);
          }
        }
      }
    }
  }

  cout &lt;&lt; dp[t] &lt;&lt; endl; // 输出最终最大美学值
  return 0;
}
```

## [AcWing二维费用的背包问题](https://www.acwing.com/problem/content/8/)

&gt; 有 N𝑁 件物品和一个容量是 V𝑉 的背包，背包能承受的最大重量是 M𝑀。
&gt;
&gt; 每件物品只能用一次。体积是 vi𝑣𝑖，重量是 mi𝑚𝑖，价值是 wi𝑤𝑖。
&gt;
&gt; 求解将哪些物品装入背包，可使物品总体积不超过背包容量，总重量不超过背包可承受的最大重量，且价值总和最大。
&gt; 输出最大价值。
&gt;
&gt; #### 输入格式
&gt;
&gt; 第一行三个整数，N,V,M𝑁,𝑉,𝑀，用空格隔开，分别表示物品件数、背包容积和背包可承受的最大重量。
&gt;
&gt; 接下来有 N𝑁 行，每行三个整数 vi,mi,wi𝑣𝑖,𝑚𝑖,𝑤𝑖，用空格隔开，分别表示第 i𝑖 件物品的体积、重量和价值。
&gt;
&gt; #### 输出格式
&gt;
&gt; 输出一个整数，表示最大价值。
&gt;
&gt; #### 数据范围
&gt;
&gt; 0<n≤10000<𝑁≤1000> 0<v,m≤1000<𝑉,𝑀≤100> 0<vi,mi≤1000<𝑣𝑖,𝑚𝑖≤100> 0<wi≤10000<𝑤𝑖≤1000>
&gt; #### 输入样例
&gt;
&gt; ```
&gt; 4 5 6
&gt; 1 2 3
&gt; 2 4 4
&gt; 3 4 5
&gt; 4 5 6
&gt; ```
&gt;
&gt; #### 输出样例：
&gt;
&gt; ```
&gt; 8
&gt; ```

```c++
#include <iostream>
#include <vector>
using namespace std;

int main() {
  int n, av, am;
  cin &gt;&gt; n &gt;&gt; av &gt;&gt; am;
  vector<int> v(n, 0), m(n, 0), w(n, 0);
  for (int i = 0; i &lt; n; i++) {
    cin &gt;&gt; v[i] &gt;&gt; m[i] &gt;&gt; w[i];
  }
  vector<vector<int>&gt; dp(av + 1, vector<int>(am + 1, 0));
  for (int i = 0; i &lt; n; i++) {
    for (int j = av; j &gt;= v[i]; j--) {
      for (int k = am; k &gt;= m[i]; k--) {
        dp[j][k] = max(dp[j][k], dp[j - v[i]][k - m[i]] + w[i]);
      }
    }
  }
  cout &lt;&lt; dp[av][am] &lt;&lt; endl;
  return 0;
}
```



## [Luogu 1507 NASA的食物计划](https://www.luogu.org/problemnew/show/P1507)

&gt; ## 题目背景
&gt;
&gt; NASA（美国航空航天局）因为航天飞机的隔热瓦等其他安全技术问题一直大伤脑筋，因此在各方压力下终止了航天飞机的历史，但是此类事情会不会在以后发生，谁也无法保证。所以，在遇到这类航天问题时，也许只能让航天员出仓维修。但是过多的维修会消耗航天员大量的能量，因此 NASA 便想设计一种食品方案，使体积和承重有限的条件下多装载一些高卡路里的食物。
&gt;
&gt; ## 题目描述
&gt;
&gt; 航天飞机的体积有限，当然如果载过重的物品，燃料会浪费很多钱，每件食品都有各自的体积、质量以及所含卡路里。在告诉你体积和质量的最大值的情况下，请输出能达到的食品方案所含卡路里的最大值，当然每个食品只能使用一次。
&gt;
&gt; ## 输入格式
&gt;
&gt; 第一行 22 个整数，分别代表体积最大值 ℎ*h* 和质量最大值 𝑡*t*。
&gt;
&gt; 第二行 11 个整数代表食品总数 𝑛*n*。
&gt;
&gt; 接下来 𝑛*n* 行每行 33 个数 体积 ℎ𝑖*h**i*，质量 𝑡𝑖*t**i*，所含卡路里 𝑘𝑖*k**i*。
&gt;
&gt; ## 输出格式
&gt;
&gt; 一个数，表示所能达到的最大卡路里（`int` 范围内）
&gt;
&gt; ## 输入输出样例
&gt;
&gt; **输入 #1**复制
&gt;
&gt; ```
&gt; 320 350
&gt; 4
&gt; 160 40 120
&gt; 80 110 240
&gt; 220 70 310
&gt; 40 400 220
&gt; ```
&gt;
&gt; **输出 #1**复制
&gt;
&gt; ```
&gt; 550
&gt; ```
&gt;
&gt; ## 说明/提示
&gt;
&gt; 对于 100%100% 的数据，ℎ,𝑡,ℎ𝑖,𝑡𝑖≤400*h*,*t*,*h**i*,*t**i*≤400，𝑛≤50*n*≤50，𝑘𝑖≤500*k**i*≤500。

```c++
#include <iostream>
#include <vector>
using namespace std;

int main() {
  int n, av, am;
  cin &gt;&gt; av &gt;&gt; am;
  cin &gt;&gt; n;
  vector<int> v(n, 0), m(n, 0), w(n, 0);
  for (int i = 0; i &lt; n; i++) {
    cin &gt;&gt; v[i] &gt;&gt; m[i] &gt;&gt; w[i];
  }
  vector<vector<int>&gt; dp(av + 1, vector<int>(am + 1, 0));
  for (int i = 0; i &lt; n; i++) {
    for (int j = av; j &gt;= v[i]; j--) {
      for (int k = am; k &gt;= m[i]; k--) {
        dp[j][k] = max(dp[j][k], dp[j - v[i]][k - m[i]] + w[i]);
      }
    }
  }
  cout &lt;&lt; dp[av][am] &lt;&lt; endl;
  return 0;
}
```

## [AcWing分组背包问题](https://www.acwing.com/problem/content/description/9/)

&gt; 有 N𝑁 组物品和一个容量是 V𝑉 的背包。
&gt;
&gt; 每组物品有若干个，同一组内的物品最多只能选一个。
&gt; 每件物品的体积是 vij𝑣𝑖𝑗，价值是 wij𝑤𝑖𝑗，其中 i𝑖 是组号，j𝑗 是组内编号。
&gt;
&gt; 求解将哪些物品装入背包，可使物品总体积不超过背包容量，且总价值最大。
&gt;
&gt; 输出最大价值。
&gt;
&gt; #### 输入格式
&gt;
&gt; 第一行有两个整数 N，V𝑁，𝑉，用空格隔开，分别表示物品组数和背包容量。
&gt;
&gt; 接下来有 N𝑁 组数据：
&gt;
&gt; - 每组数据第一行有一个整数 Si𝑆𝑖，表示第 i𝑖 个物品组的物品数量；
&gt; - 每组数据接下来有 Si𝑆𝑖 行，每行有两个整数 vij,wij𝑣𝑖𝑗,𝑤𝑖𝑗，用空格隔开，分别表示第 i𝑖 个物品组的第 j𝑗 个物品的体积和价值；
&gt;
&gt; #### 输出格式
&gt;
&gt; 输出一个整数，表示最大价值。
&gt;
&gt; #### 数据范围
&gt;
&gt; 0<n,v≤1000<𝑁,𝑉≤100> 0<si≤1000<𝑆𝑖≤100> 0<vij,wij≤1000<𝑣𝑖𝑗,𝑤𝑖𝑗≤100>
&gt; #### 输入样例
&gt;
&gt; ```
&gt; 3 5
&gt; 2
&gt; 1 2
&gt; 2 4
&gt; 1
&gt; 3 4
&gt; 1
&gt; 4 5
&gt; ```
&gt;
&gt; #### 输出样例：
&gt;
&gt; ```
&gt; 8
&gt; ```

```c++
#include <iostream>
#include <vector>
using namespace std;
int main() {
  int m, n;
  cin &gt;&gt; n &gt;&gt; m;
  vector<int> weight;
  vector<int> value;
  vector<int> group;
  vector<vector<int>&gt; index(101, vector<int>());
  vector<int> dp(m + 1, 0);
  for (int i = 1; i &lt;= n; i++) {
    int temp;
    cin &gt;&gt; temp;
    for (int j = 0; j &lt; temp; j++) {
      int a, b;
      cin &gt;&gt; a &gt;&gt; b;
      weight.push_back(a);
      value.push_back(b);
      group.push_back(i);
      index[i].push_back(group.size() - 1);
    }
  }
  for (int i = 1; i &lt;= 100; i++) {
    for (int j = m; j &gt;= 0; j--) {
      for (int k = 0; k &lt; index[i].size(); k++) {
        if (j &gt;= weight[index[i][k]]) {
          dp[j] = max(dp[j], dp[j - weight[index[i][k]]] + value[index[i][k]]);
        }
      }
    }
  }
  cout &lt;&lt; dp[m] &lt;&lt; endl;
  return 0;
}
```

## [Luogu P1757通天之分组背包](https://www.luogu.org/problemnew/show/P1757#sub)

&gt; ## 题目背景
&gt;
&gt; 直达通天路·小 A 历险记第二篇
&gt;
&gt; ## 题目描述
&gt;
&gt; 自 0101 背包问世之后，小 A 对此深感兴趣。一天，小 A 去远游，却发现他的背包不同于 0101 背包，他的物品大致可分为 𝑘*k* 组，每组中的物品相互冲突，现在，他想知道最大的利用价值是多少。
&gt;
&gt; ## 输入格式
&gt;
&gt; 两个数 𝑚,𝑛*m*,*n*，表示一共有 𝑛*n* 件物品，总重量为 𝑚*m*。
&gt;
&gt; 接下来 𝑛*n* 行，每行 33 个数 𝑎𝑖,𝑏𝑖,𝑐𝑖*a**i*,*b**i*,*c**i*，表示物品的重量，利用价值，所属组数。
&gt;
&gt; ## 输出格式
&gt;
&gt; 一个数，最大的利用价值。
&gt;
&gt; ## 输入输出样例
&gt;
&gt; **输入 #1**
&gt;
&gt; ```
&gt; 45 3
&gt; 10 10 1
&gt; 10 5 1
&gt; 50 400 2
&gt; ```
&gt;
&gt; **输出 #1**
&gt;
&gt; ```
&gt; 10
&gt; ```
&gt;
&gt; ## 说明/提示
&gt;
&gt; 0≤𝑚≤10000≤*m*≤1000，1≤𝑛≤10001≤*n*≤1000，1≤𝑘≤1001≤*k*≤100，𝑎𝑖,𝑏𝑖,𝑐𝑖*a**i*,*b**i*,*c**i* 在 `int` 范围内。

```c++
#include <iostream>
#include <vector>
using namespace std;
int main() {
  int m, n;
  cin &gt;&gt; m &gt;&gt; n;
  vector<int> weight(n, 0);
  vector<int> value(n, 0);
  vector<int> group(n, 0);
  vector<vector<int>&gt; index(101, vector<int>());
  vector<int> dp(m + 1, 0);
  for (int i = 0; i &lt; n; i++) {
    cin &gt;&gt; weight[i] &gt;&gt; value[i] &gt;&gt; group[i];
    index[group[i]].push_back(i);
  }
  for (int i = 1; i &lt;= 100; i++) {
    for (int j = m; j &gt;= 0; j--) {
      for (int k = 0; k &lt; index[i].size(); k++) {
        if (j &gt;= weight[index[i][k]]) {
          dp[j] = max(dp[j], dp[j - weight[index[i][k]]] + value[index[i][k]]);
        }
      }
    }
  }
  cout &lt;&lt; dp[m] &lt;&lt; endl;
  return 0;
}
```

## [OpenJudge - 2806:公共子序列](http://bailian.openjudge.cn/practice/2806)

&gt; - 总时间限制: 
&gt;
&gt;   1000ms
&gt;
&gt; - 内存限制: 
&gt;
&gt;   65536kB
&gt;
&gt; - 描述
&gt;
&gt;   我们称序列Z = &lt; z1, z2, ..., zk &gt;是序列X = &lt; x1, x2, ..., xm &gt;的子序列当且仅当存在 **严格上升** 的序列&lt; i1, i2, ..., ik &gt;，使得对j = 1, 2, ... ,k, 有xij = zj。比如Z = &lt; a, b, f, c &gt; 是X = &lt; a, b, c, f, b, c &gt;的子序列。  现在给出两个序列X和Y，你的任务是找到X和Y的最大公共子序列，也就是说要找到一个最长的序列Z，使得Z既是X的子序列也是Y的子序列。 
&gt;
&gt; - 输入
&gt;
&gt;   输入包括多组测试数据。每组数据包括一行，给出两个长度不超过200的字符串，表示两个序列。两个字符串之间由若干个空格隔开。
&gt;
&gt; - 输出
&gt;
&gt;   对每组输入数据，输出一行，给出两个序列的最大公共子序列的长度。
&gt;
&gt; - 样例输入
&gt;
&gt;   `abcfbc         abfcab`
&gt;
&gt;   ` programming    contest` 
&gt;
&gt;    `abcd           mnp `
&gt;
&gt; - 样例输出
&gt;
&gt;   `4 2 0 `
&gt;
&gt; - 来源
&gt;
&gt;   翻译自Southeastern Europe 2003的试题

```c++
#include <stdio.h>
#include <string.h>
#define MAX_LEN 1000
char sz1[MAX_LEN];
char sz2[MAX_LEN];
int aMaxLen[MAX_LEN][MAX_LEN];

int main() {
  while (scanf("%s%s", sz1 + 1, sz2 + 1) &gt; 0) {
    int nLength1 = strlen(sz1 + 1);
    int nLength2 = strlen(sz2 + 1);
    int nTmp;
    int i, j;
    for (i = 0; i &lt;= nLength1; i++)
      aMaxLen[i][0] = 0;
    for (j = 0; j &lt;= nLength2; j++)
      aMaxLen[0][j] = 0;
    for (i = 1; i &lt;= nLength1; i++) {
      for (j = 1; j &lt;= nLength2; j++) {
        if (sz1[i] == sz2[j])
          aMaxLen[i][j] = aMaxLen[i - 1][j - 1] + 1;
        else {
          int nLen1 = aMaxLen[i][j - 1];
          int nLen2 = aMaxLen[i - 1][j];
          if (nLen1 &gt; nLen2)
            aMaxLen[i][j] = nLen1;
          else
            aMaxLen[i][j] = nLen2;
        }
      }
    }
    printf("%d\n", aMaxLen[nLength1][nLength2]);
  }
  return 0;
}
```

</string.h></stdio.h></int></int></vector<int></int></int></int></vector></iostream></int></int></vector<int></int></int></int></vector></iostream></vij,wij≤1000<𝑣𝑖𝑗,𝑤𝑖𝑗≤100></si≤1000<𝑆𝑖≤100></n,v≤1000<𝑁,𝑉≤100></int></vector<int></int></vector></iostream></int></vector<int></int></vector></iostream></wi≤10000<𝑤𝑖≤1000></vi,mi≤1000<𝑣𝑖,𝑚𝑖≤100></v,m≤1000<𝑉,𝑀≤100></n≤10000<𝑁≤1000></int></int></int></int></vector></sstream></iostream></int></int></int></int></vector></iostream></vi,wi≤1000></n,v≤1000></vi,wi,si≤20000></v≤20000></n≤1000></n≤1000,></vi,wi,si≤20000$></v≤2000$></n≤1000$></vi,wi,si≤100></n,v≤100></int></int></int></int></vector></iostream></int></int></int></vector></iostream></cmath></algorithm></int></int></int></vector></iostream></cmath></algorithm></vi,wi≤1000></n,v≤1000></int></int></vector></iostream></vi,wi≤10000<𝑣𝑖,𝑤𝑖≤1000></n,v≤10000<𝑁,𝑉≤1000></int></pair<char,></int></int></int></vector<int></int></vector></iostream></int></int></vector></iostream>