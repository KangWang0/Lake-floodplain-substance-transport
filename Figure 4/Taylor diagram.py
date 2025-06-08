import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import skill_metrics as sm

# 文件路径
file_path = r'C:\Users\Antonio\Desktop\desk\论文\拟建水利工程对鄱阳湖水文动态与污染物扩散的影响研究\插图\其它\wlwfdata.xlsx'

# 四个季节及站点名称
seasons = ['spring', 'summer', 'autumn', 'winter']
station_names = ['Xingzi', 'Duchang', 'Tangyin', 'Kangshan']

def compute_metrics(obs_array, sim_array):
    """
    计算观测与模拟数据的相关系数、模拟数据标准差、观测数据标准差以及中心化 RMS 误差。
    
    参数：
      obs_array, sim_array: 一维 numpy 数组
    返回：
      cc     : 相关系数（Pearson）
      sd_sim : 模拟序列的标准差
      sd_obs : 观测序列的标准差
      crmsd  : 去除均值后的 RMS 误差
    """
    cc = np.corrcoef(obs_array, sim_array)[0, 1]
    sd_sim = np.std(sim_array, ddof=1)
    sd_obs = np.std(obs_array, ddof=1)
    # 计算中心化 RMS 误差（去除均值）
    sim_c = sim_array - np.mean(sim_array)
    obs_c = obs_array - np.mean(obs_array)
    crmsd = np.sqrt(np.mean((sim_c - obs_c)**2))
    return cc, sd_sim, sd_obs, crmsd

# 建立 2x2 的子图布局
fig, axes = plt.subplots(2, 2, figsize=(12, 11))

for i, season in enumerate(seasons):
    # 读取对应季节的工作表
    df = pd.read_excel(file_path, sheet_name=season)
    
    sd_norm_list = []      # 模拟标准差归一化后列表
    crmsd_norm_list = []   # 模拟中心化 RMS 归一化后列表
    cc_list = []           # 相关系数列表
    
    for st in station_names:
        # 读取观测值与模拟值
        obs = df[f"{st}_obs"].to_numpy()
        sim = df[f"{st}_sim"].to_numpy()
        
        # 计算指标
        cc, sd_sim, sd_obs, crmsd = compute_metrics(obs, sim)
        
        # 归一化：除以观测数据的标准差，使得观测值统一为 1
        sd_norm = sd_sim / sd_obs if sd_obs != 0 else np.nan
        crmsd_norm = crmsd / sd_obs if sd_obs != 0 else np.nan
        
        sd_norm_list.append(sd_norm)
        crmsd_norm_list.append(crmsd_norm)
        cc_list.append(cc)
    
    # 将观测值（归一化后：标准差=1，RMS=0，相关系数=1）添加为第一个点
    sd_all = np.array([1.0] + sd_norm_list)
    crmsd_all = np.array([0.0] + crmsd_norm_list)
    cc_all = np.array([1.0] + cc_list)
    labels = ['Obs'] + station_names
    
    # 切换到当前子图
    ax = axes.flatten()[i]
    plt.sca(ax)
    
    # 调用 taylor_diagram 绘制泰勒图
    sm.taylor_diagram(
        sd_all,
        crmsd_all,
        cc_all,
        markerLabel=labels,
        markercolor="k",
        markerSize=8,
        markerLegend='on',
        colCOR="gray", titleCOR="off", styleCOR="--", widthCOR=0.5,
        colSTD="k", widthSTD=1.5, styleSTD="-", axismax=1.5,
        widthRMS=1.0, labelRMS='',
        colRMS='red', styleRMS='--',
        colOBS="purple", styleOBS="--", widthOBS=1.5,
        markerObs="o", titleOBS="Observation"
    )
    
    ax.set_title(season.capitalize(), fontsize=14)
    # 去除图例外框
    ax.get_legend().set_frame_on(False)

plt.tight_layout()
plt.savefig('taylor_diagram.png', dpi=600, bbox_inches='tight')
plt.savefig('taylor_diagram.pdf', dpi=600, bbox_inches='tight')
plt.show()
