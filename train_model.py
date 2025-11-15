import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
import shap
import os

# 读取最优参数
print("读取最优参数...")
params_path = r"Final result终版\最优模型RF参数.xlsx"
params_df = pd.read_excel(params_path)
print("参数文件内容:")
print(params_df)

# 读取训练集
print("\n读取训练集...")
train_path = r"spesis and pi\parameters\smote_nc_mimiciv_train.csv"
train_df = pd.read_csv(train_path)
print(f"训练集形状: {train_df.shape}")
print(f"列名: {train_df.columns.tolist()}")

# 读取测试集
print("\n读取测试集...")
test_path = r"spesis and pi\parameters\mimiciii_test1.xlsx"
test_df = pd.read_excel(test_path)
print(f"测试集形状: {test_df.shape}")
print(f"列名: {test_df.columns.tolist()}")

# 提取特征和目标变量
feature_cols = ['ANION_GAP', 'BALANCE', 'BS', 'BUN', 'CHLORIDE', 'CR', 'CRRT', 
                'GCS', 'HGB', 'INRPT', 'MV', 'NBPS', 'NOR', 'OASIS', 'RR', 
                'SAPSII', 'SODIUM', 'SOFA', 'T', 'WBC']

# 检查列名（可能大小写不同）
train_cols = train_df.columns.tolist()
target_col = None
for col in train_cols:
    if 'SPESIS' in col.upper() or 'SEPSIS' in col.upper():
        target_col = col
        break

if target_col is None:
    target_col = train_cols[0]  # 假设第一列是目标变量

print(f"\n目标变量列: {target_col}")

# 准备训练数据
X_train = train_df[feature_cols].copy()
y_train = train_df[target_col].copy()

# 准备测试数据
X_test = test_df[feature_cols].copy()
y_test = test_df[target_col].copy() if target_col in test_df.columns else None

print(f"\n训练集特征形状: {X_train.shape}")
print(f"训练集目标形状: {y_train.shape}")
print(f"测试集特征形状: {X_test.shape}")

# 从参数文件中提取最优参数
# 参数文件使用R语言格式，需要转换为Python格式
try:
    # 创建参数字典
    params_dict = {}
    for idx, row in params_df.iterrows():
        charater = str(row['Charater']).strip()
        value = row['Value']
        if pd.notna(value):
            params_dict[charater] = value
    
    # 转换R参数到Python参数
    # num.trees -> n_estimators
    n_estimators = int(params_dict.get('num.trees', 2500))
    
    # max.depth -> max_depth
    max_depth = int(params_dict.get('max.depth', 50)) if 'max.depth' in params_dict else None
    
    # min.node.size -> min_samples_leaf
    min_samples_leaf = int(params_dict.get('min.node.size', 50))
    
    # min.bucket -> min_samples_split
    min_samples_split = int(params_dict.get('min.bucket', 30))
    
    # mtry -> max_features (可以是整数或'sqrt')
    mtry_val = params_dict.get('mtry', 6)
    try:
        max_features = int(float(mtry_val))
    except (ValueError, TypeError):
        max_features = 'sqrt'
        
    print(f"从参数文件读取的参数:")
    print(f"  num.trees: {n_estimators}")
    print(f"  max.depth: {max_depth}")
    print(f"  min.node.size: {min_samples_leaf}")
    print(f"  min.bucket: {min_samples_split}")
    print(f"  mtry: {max_features}")
        
except Exception as e:
    print(f"读取参数时出错，使用默认参数: {e}")
    n_estimators = 2500
    max_depth = 50
    min_samples_split = 30
    min_samples_leaf = 50
    max_features = 6

print(f"\n模型参数:")
print(f"  n_estimators: {n_estimators}")
print(f"  max_depth: {max_depth}")
print(f"  min_samples_split: {min_samples_split}")
print(f"  min_samples_leaf: {min_samples_leaf}")
print(f"  max_features: {max_features}")

# 训练模型
print("\n训练随机森林模型...")
rf_model = RandomForestClassifier(
    n_estimators=n_estimators,
    max_depth=max_depth,
    min_samples_split=min_samples_split,
    min_samples_leaf=min_samples_leaf,
    max_features=max_features,
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)
print("模型训练完成!")

# 保存模型
model_path = "rf_model.pkl"
with open(model_path, 'wb') as f:
    pickle.dump(rf_model, f)
print(f"模型已保存到: {model_path}")

# 保存特征列名
feature_info = {
    'feature_cols': feature_cols,
    'target_col': target_col
}
with open("feature_info.pkl", 'wb') as f:
    pickle.dump(feature_info, f)

# 创建SHAP解释器
print("\n创建SHAP解释器...")
# 使用TreeExplainer（适用于树模型，速度快）
explainer = shap.TreeExplainer(rf_model)
shap_values = explainer.shap_values(X_train[:100])  # 使用前100个样本作为背景

# 保存SHAP解释器
with open("shap_explainer.pkl", 'wb') as f:
    pickle.dump(explainer, f)
print("SHAP解释器已保存!")

print("\n完成!")

