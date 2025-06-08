# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 10:33:16 2024

@author: Antonio
"""

import mikeio
import pandas as pd

# 定义DFSU文件路径
dfsu_file_path = r"C:\Users\Antonio\Desktop\desk\poyang_lake\Temperature 20230303\Comprehensive_model.m21fm - Result Files\wet area.dfsu"

# 创建DFSU对象
dfsu = mikeio.Dfsu(dfsu_file_path)

# # Assuming dfsu is your Dfsu2DH object
# print(dir(dfsu))


# 读取DFSU文件中的数据
data = dfsu.read(items=['Total water depth'])

# 获取元素的面积，单位是平方米
element_areas = dfsu.get_element_area()

# 初始化一个字典用于存储每一天的有水面积（平方千米）
daily_water_area_km2 = {}

for timestep, time in enumerate(data.time):
    # 提取对应时间步的"Total water depth"数据
    water_depth_values = data[0][timestep].values
    
    # 识别有水的元素（这里假设水深大于0.0099的元素被认为是有水的）
    wet_elements_mask = water_depth_values > 0.1
    
    # 计算有水的元素的总面积，并转换为平方千米
    wet_area_m2 = element_areas[wet_elements_mask].sum()
    wet_area_km2 = wet_area_m2 / 1_000_000  # 转换为平方千米
    
    # 将计算得到的面积与对应的日期存储在字典中
    daily_water_area_km2[time] = wet_area_km2

# 创建DataFrame来存储每一天的有水面积
water_area_df = pd.DataFrame(list(daily_water_area_km2.items()), columns=['Date', 'Water Area (km^2)'])

# 导出数据到CSV文件
output_csv_path = r"C:\Users\Antonio\Desktop\desk\poyang_lake\Temperature 20230303\Comprehensive_model.m21fm - Result Files\2016-2018water_area_daily.csv"
water_area_df.to_csv(output_csv_path, index=False)

print("Water area extraction complete. The data has been saved to:", output_csv_path)
