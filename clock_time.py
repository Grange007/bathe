import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy import stats

# ==========================================
# 1. 学术风格全局设置 (Academic Style Config)
# ==========================================
# 使用 Times New Roman 字体，公式使用类似 LaTeX 的 STIX 字体
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True

# ==========================================
# 2. 生成伪造的观测数据 (Generate Dummy Data)
# ==========================================
np.random.seed(518) # 致敬你们寝室号 518A

# 假设一个学期有 120 天，我们随机记录了其中 75 天的真实停水时间
total_days = 120
sampled_days = np.sort(np.random.choice(np.arange(1, total_days + 1), 75, replace=False))

# 时钟漂移参数：假设每天慢 2.8 秒 (beta)，以及 15 秒的随机环境噪声波动 (sigma)
beta_true = 2.8 
sigma_noise = 15.0

# 生成延迟数据 (单位：秒)
delays_seconds = beta_true * sampled_days + np.random.normal(0, sigma_noise, len(sampled_days))
# 模拟个别极端异常值（比如某天机器可能被重启了，或者网络波动）
delays_seconds[15] -= 40
delays_seconds[50] += 55

# ==========================================
# 3. 数据拟合与置信区间计算 (Data Fitting & CI)
# ==========================================
# 线性回归拟合
slope, intercept, r_value, p_value, std_err = stats.linregress(sampled_days, delays_seconds)
fit_line = slope * sampled_days + intercept

# 计算 95% 置信区间 (95% Confidence Interval)
# 简单近似：拟合线 +/- 1.96 * 残差标准差
residuals = delays_seconds - fit_line
std_residuals = np.std(residuals)
ci_upper = fit_line + 1.96 * std_residuals
ci_lower = fit_line - 1.96 * std_residuals

# ==========================================
# 4. 绘制图表 (Plotting)
# ==========================================
fig, ax = plt.subplots(figsize=(7, 5), dpi=300)

# 绘制散点图 (空心圆圈，经典学术风)
ax.scatter(sampled_days, delays_seconds, facecolors='none', edgecolors='#1f77b4', 
           marker='o', s=40, label='Observation Data', zorder=2)

# 绘制拟合直线
ax.plot(sampled_days, fit_line, color='#d62728', linewidth=2, 
        label=rf'Linear Fit ($\beta={slope:.2f}$ s/day)', zorder=3)

# 绘制置信区间阴影
ax.fill_between(sampled_days, ci_lower, ci_upper, color='#d62728', alpha=0.15, 
                label='95\% Confidence Interval', zorder=1)

# ==========================================
# 5. 坐标轴与标签美化 (Axis & Labels formatting)
# ==========================================
ax.set_xlabel('Days Since Semester Initialization ($d$)', fontsize=14)
ax.set_ylabel(r'Actual Cutoff Delay $\Delta t$ (Seconds)', fontsize=14)

# 将 Y 轴刻度格式化为 "+ 分:秒" 的形式，更直观
def time_formatter(x, pos):
    if x < 0:
        return f"-00:{-int(x):02d}"
    mins = int(x // 60)
    secs = int(x % 60)
    return f"+{mins:02d}:{secs:02d}"

ax.yaxis.set_major_formatter(ticker.FuncFormatter(time_formatter))
ax.tick_params(axis='both', which='major', labelsize=12)

# 设置坐标轴范围
ax.set_xlim(0, 125)
ax.set_ylim(bottom=-30) 

# 添加图例
ax.legend(loc='upper left', frameon=True, edgecolor='black', fancybox=False, fontsize=11)

# 添加网格线 (可选，学术图表推荐使用虚线且颜色较浅)
ax.grid(True, linestyle='--', alpha=0.5, zorder=0)

# 紧凑布局并保存
plt.tight_layout()
plt.savefig('fig1_clock_drift.pdf', format='pdf', bbox_inches='tight') # 保存为矢量图，适合插入LaTeX
plt.savefig('fig1_clock_drift.png', format='png', dpi=300, bbox_inches='tight')
plt.show()