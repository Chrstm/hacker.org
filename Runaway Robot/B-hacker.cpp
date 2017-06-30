/*
* Author: JHSN
* Website: blog.chrstm.com
* Algorithm: 
* ����˼·�ǣ���ö�ٴ𰸳��� ans����ö��һ������֮����������
* �������Ϊ (X, Y)���� ans = X + Y - 2������������γ�һ�� 
* X*Y �ľ������򣬵�һ�������ھ�����·���������У�ͬ��
* �еڶ������ڵ����򣬵����������ĸ�������Щ����ȫ����֮ȷ����
* ���ѿ����� i ����������½Ǻ͵� i+1 ����������Ͻ����غϣ� 
* ��Ϊ������Щ�����ϵ�·������ͬ���������ǲ�������Щ������кϲ���
* ���������������ڵ�һ��������ߵ��ҽ�������������������Ҳ�����ߣ�
* �ݴ�ԭ��ϲ���������Ȼ������� X*Y ������������ BFS Ѱ��һ��
* �����Ͻǵ����½ǵ�·������·����Ϊ���н⡣ 
* �ó���Ѱ�ҵ�����С�ֵ���� 
*/

#include<cstdio>
#include<algorithm>
#include<cstring>
using namespace std;

const int fx[2] = {1, 0};
const int fy[2] = {0, 1};
const int N=2010;
bool a[N][N], b[N][N], dire[N<<2], res[N<<2];
int n, m, L, R, i, j, times;
int sx, sy, ans, endx, endy, tot, xx, yy, x, y;
int s, t, qx[N*N], qy[N*N], pre[N*N];
bool jc[N*N], g[N][N];
bool hasfind, flag;
char ch;

void print_a(bool (*a)[N], int n, int m)
{
    for (int i = 0; i <= n; i++)
    {
        for (int j = 0; j <= m; j++)
            printf(a[i][j] ? "_" : "8");
        puts("");
    }
}

void goback(int now)
{
    if (pre[now] > 1) goback(pre[now]);
    res[++tot] = jc[now];
}

void generate_ans(int t, int len)
{
    tot = 0;
    goback(t);
    bool lt = 0;
    for (int i = 1; i <= len; i++)
    {
        if (dire[i] < res[i]) break;
        if (res[i] < dire[i]) { lt = 1; break; }
    }
    if (1) // (lt)
    {
        for (int i = 1; i <= len; i++)
            dire[i] = res[i];
        //print_a(b, endx, endy);
    }
        
    flag = 1;
}

void print_dire(int ans)
{
    for (int i = 1; i <= ans; i++)
        printf(dire[i] ? "R" : "D");
    puts("");
}

int main()
{
    //freopen("in.txt", "r", stdin);
        scanf("%d%d%d%d", &n, &m, &L, &R);
        // read_map
        for (i = 1; i <= n; i++)
        {
            for (j = 1; j <= m; j++)
            {
                ch = getchar();
                while (ch != '.' && ch != 'X') ch = getchar();
                a[i][j] = (ch == '.') ? 1 : 0;
            }
            a[i][m + 1] = 1;
        }
        for (i = 1; i <= m; i++) a[n + 1][i] = 1;
        a[n + 1][m + 1] = 1;
        n++; m++;
        for (i = 1; i <= n; i++) a[i][m + 1] = 0;
        for (i = 1; i <= m; i++) a[n + 1][i] = 0;
        a[n + 1][m + 1] = 0;
        
        // pre_scan_map
        a[n + 1][m] = 1;
        for (i = n; i; i--)
            for (j = m; j; j--)
                a[i][j] = a[i][j] & (a[i + 1][j] | a[i][j + 1]);
        a[n + 1][m] = 0;
        a[0][1] = 1;
        for (i = 1; i <= n; i++)
            for (j = 1; j <= n; j++)
                a[i][j] = a[i][j] & (a[i - 1][j] | a[i][j - 1]);
        a[0][1] = 0;
        
        //print_a();// continue;
        for (ans = L; ans <= R; ans++)
        {
            flag = 0;
            for (i = 1; i <= ans; i++) dire[i] = 1;
            
            int sxlimit = min(n - 1, ans);
            for (sx = 0; sx <= sxlimit; sx++)
            // for (sx = min(n - 1, ans); sx >= 0; sx--)
            {
                // +sx +sy  [x..xx, y..yy]  [1..sx+1, 1..sy+1]
                
                sy = ans - sx;
                xx = yy = 1;
                endx = sx + 1;
                endy = sy + 1;
                if (sx > 0) times = (n + sx - 2) / sx;
                        else times = 1000000000;
                if (sy > 0) times = min(times, (m + sy - 2) / sy);
                if (!a[endx][endy] ||
                    !a[min(n, 1 + sx * times)][min(m, 1 + sy * times)]) continue;
                
                // combine map
                for (i = 1; i <= endx; i++)
                    for (j = 1; j <= endy; j++) b[i][j] = 1;
                while (xx < n && yy < m)
                {
                    x = xx; y = yy;
                    xx = min(n, x + sx);
                    yy = min(m, y + sy);
                    for (i = 0; x + i <= xx; i++)
                        for (j = 0; y + j <= yy; j++)
                            b[i + 1][j + 1] &= a[x + i][y + j];
                }
                
                if (!b[1][1] || !b[endx][endy]) continue;
                
                // bfs
                qx[1] = 1;
                qy[1] = 1;
                s = 0; t = 1;
                hasfind = 0;
                int size = sizeof(g[i][0]) * (endy + 3);
                for (i = 1; i <= endx; i++)
                    memset(&(g[i]), 0, size);
                for (i = 1; i <= endx; i++) g[i][endy + 1] = 1;
                for (i = 1; i <= endy; i++) g[endx + 1][i] = 1;
                while (s < t && !hasfind)
                {
                    x = qx[++s]; y = qy[s];
                    for (i = 0; i < 2; i++)
                    {
                        xx = x + fx[i]; yy = y + fy[i];
                        if (!b[xx][yy] || g[xx][yy]) continue;
                        
                        g[xx][yy] = 1;
                        qx[++t] = xx;
                        qy[t] = yy;
                        pre[t] = s;
                        jc[t] = i;
                        if (xx == endx && yy == endy)
                        {
                            hasfind = 1;
                            generate_ans(t, ans);
                            break;
                        }
                    }
                }
            }
            if (flag)
            {
                int cnt = 0;
                x = 1; y = 1;
                i = 0;
                while (x < n && y < m)
                {
                    i++;
                    cnt++;
                    if (i > ans) i = 1;
                    if (dire[i]) y++;
                            else x++;
                }
                if (cnt < ans)
                    for (i++; i <= ans; i++) dire[i] = 0;
                print_dire(ans);
                break;
            }
        }
        if (!flag) puts("NOT FOUND!!!!!!!!");
    return 0;
}
