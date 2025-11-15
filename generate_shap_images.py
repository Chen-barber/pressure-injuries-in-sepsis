import pandas as pd
import numpy as np
import pickle
import shap
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

print("加载模型和解释器...")
try:
    # 加载模型
    with open('rf_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✓ 模型加载成功")
    
    # 加载SHAP解释器
    with open('shap_explainer.pkl', 'rb') as f:
        explainer = pickle.load(f)
    print("✓ SHAP解释器加载成功")
    
    # 加载特征信息
    with open('feature_info.pkl', 'rb') as f:
        feature_info = pickle.load(f)
    print("✓ 特征信息加载成功")
except Exception as e:
    print(f"✗ 加载失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

feature_cols = feature_info['feature_cols']
print(f"特征列: {feature_cols}")

# 读取测试集的一个样本作为示例
print("\n读取测试集样本...")
test_path = r"spesis and pi\parameters\mimiciii_test1.xlsx"
test_df = pd.read_excel(test_path)
print(f"测试集形状: {test_df.shape}")

# 选择一个样本（可以选择第一个，或者随机选择一个）
sample_idx = 0
sample_data = test_df[feature_cols].iloc[[sample_idx]].copy()
print(f"\n使用样本索引: {sample_idx}")
print(f"样本特征值:\n{sample_data.iloc[0]}")

# 计算SHAP值
print("\n计算SHAP值...")
shap_values = explainer.shap_values(sample_data)

# 处理SHAP值
if isinstance(shap_values, list):
    shap_values_array = shap_values[1]  # 正类的SHAP值
    expected_value = explainer.expected_value[1] if isinstance(explainer.expected_value, (list, np.ndarray)) else explainer.expected_value
else:
    shap_values_array = shap_values
    expected_value = explainer.expected_value

# 确保是1维数组，并且长度与特征数量匹配
if shap_values_array.ndim > 1:
    # 如果是2维，取第一行
    shap_values_1d = shap_values_array[0].flatten()
else:
    shap_values_1d = shap_values_array.flatten()

# 如果长度不匹配，只取前len(feature_cols)个
if len(shap_values_1d) != len(feature_cols):
    print(f"警告: SHAP值长度({len(shap_values_1d)})与特征数量({len(feature_cols)})不匹配，将截取或填充")
    if len(shap_values_1d) > len(feature_cols):
        shap_values_1d = shap_values_1d[:len(feature_cols)]
    else:
        # 如果SHAP值太少，用0填充
        shap_values_1d = np.pad(shap_values_1d, (0, len(feature_cols) - len(shap_values_1d)), 'constant')

# 确保expected_value是标量
if isinstance(expected_value, (list, np.ndarray)):
    expected_value = float(expected_value[0] if len(expected_value) > 0 else expected_value)
else:
    expected_value = float(expected_value)

print(f"SHAP值形状: {shap_values_1d.shape}")
print(f"特征数量: {len(feature_cols)}")
print(f"基准值: {expected_value:.4f}")
print(f"SHAP值范围: [{shap_values_1d.min():.4f}, {shap_values_1d.max():.4f}]")

# 创建Explanation对象
explanation = shap.Explanation(
    values=shap_values_1d,
    base_values=expected_value,
    data=sample_data.iloc[0].values,
    feature_names=feature_cols
)

# 生成SHAP力图
print("\n生成SHAP力图...")
try:
    # 确保长度匹配
    if len(shap_values_1d) != len(feature_cols):
        raise ValueError(f"长度不匹配: {len(shap_values_1d)} vs {len(feature_cols)}")
    
    # 尝试使用新API
    try:
        plt.figure(figsize=(14, 6))
        shap.plots.force(explanation, matplotlib=True, show=False)
        plt.tight_layout()
        plt.savefig('shap_force_plot.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ SHAP力图已保存: shap_force_plot.png")
    except (AttributeError, TypeError):
        # 使用旧API
        plt.figure(figsize=(14, 6))
        shap.force_plot(
            expected_value,
            shap_values_1d,
            sample_data.iloc[0],
            matplotlib=True,
            show=False
        )
        plt.savefig('shap_force_plot.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ SHAP力图已保存: shap_force_plot.png")
except Exception as e:
    print(f"SHAP力图生成失败: {e}")
    # 使用条形图替代
    min_len = min(len(feature_cols), len(shap_values_1d))
    shap_df_temp = pd.DataFrame({
        '特征': feature_cols[:min_len],
        'SHAP值': shap_values_1d[:min_len]
    })
    shap_df_temp = shap_df_temp.sort_values('SHAP值', key=abs, ascending=False)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    colors = ['red' if x < 0 else 'blue' for x in shap_df_temp['SHAP值']]
    ax.barh(shap_df_temp['特征'], shap_df_temp['SHAP值'], color=colors)
    ax.set_xlabel('SHAP值', fontsize=14)
    ax.set_title('SHAP力图 - 特征贡献度', fontsize=16, fontweight='bold')
    ax.axvline(x=0, color='black', linestyle='--', linewidth=0.5)
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig('shap_force_plot.png', dpi=300, bbox_inches='tight')
    print("✓ SHAP力图（替代版本）已保存: shap_force_plot.png")
    plt.close()

# 生成SHAP瀑布图
print("\n生成SHAP瀑布图...")
try:
    # 确保长度匹配
    if len(shap_values_1d) != len(feature_cols):
        raise ValueError(f"长度不匹配: {len(shap_values_1d)} vs {len(feature_cols)}")
    
    plt.figure(figsize=(14, 10))
    try:
        shap.plots.waterfall(explanation, show=False)
    except AttributeError:
        shap.waterfall_plot(explanation, show=False)
    plt.tight_layout()
    plt.savefig('shap_waterfall_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ SHAP瀑布图已保存: shap_waterfall_plot.png")
except Exception as e:
    print(f"SHAP瀑布图生成失败: {e}")
    # 使用累积条形图替代
    min_len = min(len(feature_cols), len(shap_values_1d))
    shap_df_temp = pd.DataFrame({
        '特征': feature_cols[:min_len],
        'SHAP值': shap_values_1d[:min_len]
    })
    shap_df_temp = shap_df_temp.sort_values('SHAP值', ascending=False)
    shap_df_temp['累积值'] = shap_df_temp['SHAP值'].cumsum() + expected_value
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
    
    # 上：SHAP值条形图
    colors = ['red' if x < 0 else 'blue' for x in shap_df_temp['SHAP值']]
    ax1.bar(range(len(shap_df_temp)), shap_df_temp['SHAP值'], color=colors)
    ax1.set_xticks(range(len(shap_df_temp)))
    ax1.set_xticklabels(shap_df_temp['特征'], rotation=45, ha='right', fontsize=10)
    ax1.set_ylabel('SHAP值', fontsize=12)
    ax1.set_title('SHAP瀑布图 - 特征贡献度', fontsize=16, fontweight='bold')
    ax1.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
    ax1.grid(axis='y', alpha=0.3)
    
    # 下：累积值
    ax2.plot(range(len(shap_df_temp)), shap_df_temp['累积值'], marker='o', linewidth=2, markersize=6)
    ax2.axhline(y=expected_value, color='green', linestyle='--', linewidth=1, label=f'基准值: {expected_value:.4f}')
    ax2.set_xticks(range(len(shap_df_temp)))
    ax2.set_xticklabels(shap_df_temp['特征'], rotation=45, ha='right', fontsize=10)
    ax2.set_ylabel('累积SHAP值', fontsize=12)
    ax2.set_title('累积SHAP值变化', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('shap_waterfall_plot.png', dpi=300, bbox_inches='tight')
    print("✓ SHAP瀑布图（替代版本）已保存: shap_waterfall_plot.png")
    plt.close()

# 生成特征贡献度条形图（额外）
print("\n生成特征贡献度条形图...")
shap_df = pd.DataFrame({
    '特征': feature_cols,
    'SHAP值': shap_values_1d
})
shap_df = shap_df.sort_values('SHAP值', key=abs, ascending=False)

fig, ax = plt.subplots(figsize=(12, 10))
colors = ['red' if x < 0 else 'blue' for x in shap_df['SHAP值']]
bars = ax.barh(shap_df['特征'], shap_df['SHAP值'], color=colors)
ax.set_xlabel('SHAP值', fontsize=14, fontweight='bold')
ax.set_title('SHAP特征贡献度排序', fontsize=16, fontweight='bold')
ax.axvline(x=0, color='black', linestyle='--', linewidth=1)
ax.grid(axis='x', alpha=0.3)

# 添加数值标签
for i, (idx, row) in enumerate(shap_df.iterrows()):
    value = row['SHAP值']
    ax.text(value + (0.01 if value >= 0 else -0.01), i, f'{value:.4f}', 
            va='center', ha='left' if value >= 0 else 'right', fontsize=9)

plt.tight_layout()
plt.savefig('shap_feature_importance.png', dpi=300, bbox_inches='tight')
print("✓ 特征贡献度条形图已保存: shap_feature_importance.png")
plt.close()

print("\n" + "="*50)
print("所有图表已生成完成！")
print("="*50)
print("\n生成的文件:")
print("  1. shap_force_plot.png - SHAP力图")
print("  2. shap_waterfall_plot.png - SHAP瀑布图")
print("  3. shap_feature_importance.png - 特征贡献度条形图")
print("\n所有图片分辨率: 300 DPI")
print("保存位置: 当前目录")

