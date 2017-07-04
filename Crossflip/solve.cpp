#include<cstdio>
#include<cstdlib>
#include<cstring>
using namespace std;

typedef unsigned long long ull;
const int INF=1e9+10;
const int N=400;

char a[N][N];
bool ans[N*N], b[N*N];
ull *f[N*N], *ptr, *ptr2;
ull **limp, **p;
int xl, xr, yl[N], yr[N], g[N*N], g_[N*N], c[N*N];
int i, j, k, n, m, tot, l, r, size, cnt, sum01, size6, lim;

inline ull m2(int x) {return 1ull << x;}
inline bool get_(int x, int y)
{
	return f[x][y >> 6] & m2(y & 63);
}

int main()
{
	freopen("in.txt", "r", stdin);
	freopen("ans.txt", "w", stdout);
	
	// read map
	scanf("%d%d", &n, &m);getchar();
	for (i = 0; i < n; ++i)
	{
		for (j = 0; j < m; ++j)
		{
			a[i][j] = getchar();
			if (a[i][j] != '2') ++sum01;
		}
		getchar();
		a[i][m] = '2';
	}
	for (i = 0; i < m; ++i)
	{
		a[n][i] = '2';
		yl[i] = yr[i] = INF;
	}
	
	// malloc equation f
	size = n * m;
	size6 = ((size + 64) >> 6) * sizeof(ull);
	limp = f + sum01;
	for (p = f; p != limp; ++p)
	{
		*p = (ull *)malloc(size6);
		memset(*p, 0, size6);
	}
	size6 /= sizeof(ull);
	
	// generate equation
	for (i = 0; i < n; ++i)
	{
		// xl - the leftest reachable grid
		// yl[j] - the upperest reachable grid
		xl = xr = INF;
		for (j = 0; j < m; ++j)
			if (a[i][j] == '2')
				xl = yl[j] = xr = yr[j] = INF;
			else
			{
				if (xl == INF)
				{
					 xl = xr = j;
					 while (a[i][xr] != '2') ++xr;
				}
				if (yl[j] == INF)
				{
					 yl[j] = yr[j] = i;
					 while (a[yr[j]][j] != '2') ++yr[j];
				}
				
				ptr = f[tot];
				lim = i * m + xr;
				for (k = i * m + xl; k != lim; ++k)
					ptr[k >> 6] |= m2(k & 63);
				lim = yr[j] * m + j;
				for (k = yl[j] * m + j; k != lim; k += m) // (k, j)
					ptr[k >> 6] |= m2(k & 63);
				
				b[tot] = a[i][j] == '1';
				++tot;
			}
	}
	
	// simplify equations
	for (int x = 0; x < size; ++x)
	{
		for (i = 0; i < tot; ++i)
			if (!g[i] && get_(i, x)) break;
		
		if (i == tot) continue;
		g[i] = x + 1;
		g_[x] = i + 1;
		cnt = 0;
		for (l = x >> 6; l < size6; ++l)
			if (f[i][l]) c[cnt++] = l;
		
		ptr = f[i];
		for (j = 0; j < tot; ++j)
			if (!g[j] && get_(j, x))
			{
				ptr2 = f[j];
				for (k = 0; k < cnt; ++k) ptr2[c[k]] ^= ptr[c[k]];
				b[j] ^= b[i];
			}
	}
	
	// calculate answer
	for (i = size - 1; i >= 0; --i)
		if (g_[i])
		{
			j = g_[i] - 1;
			ans[i] = b[j];
			k = ((i + 1) >> 6) << 6;
			ptr = f[j];
			while (k < size)
			{
				if (!ptr[k >> 6]) k += 64;
				else
				{
					ull tmp = 1;
					for (int T = 0; T < 64; ++T, ++k)
					{
						if ((ptr[k >> 6] & tmp) && k != i)
							ans[i] ^= ans[k];
						tmp <<= 1;
					}
				}
			}
		}
	for (p = f + sum01; p != f; --p)
		free(*p);
	for (i = 0; i < size; ++i)
		printf("%d", ans[i]);
	fclose(stdin);
	fclose(stdout);
	return 0;
}
