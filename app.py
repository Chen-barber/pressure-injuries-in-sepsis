import streamlit as st
import pandas as pd
import numpy as np
import pickle
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier

# 设置页面配置
st.set_page_config(
    page_title="Pressure Injuries in Sepsis",
    page_icon="🏥",
    layout="wide"
)

# 加载模型和SHAP解释器
@st.cache_resource
def load_model():
    """加载训练好的模型"""
    with open('rf_model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

@st.cache_resource
def load_explainer():
    """加载SHAP解释器"""
    with open('shap_explainer.pkl', 'rb') as f:
        explainer = pickle.load(f)
    return explainer

@st.cache_resource
def load_feature_info():
    """加载特征信息"""
    with open('feature_info.pkl', 'rb') as f:
        feature_info = pickle.load(f)
    return feature_info

# 加载模型和解释器
try:
    model = load_model()
    explainer = load_explainer()
    feature_info = load_feature_info()
    feature_cols = feature_info['feature_cols']
except FileNotFoundError as e:
    st.error(f"Model file not found: {e}")
    st.info("Please run train_model.py first to train the model")
    st.stop()

# 标题
st.title("🏥 Pressure Injuries in Sepsis")
st.markdown("### Sepsis Risk Score Calculator")
st.markdown("---")

# 创建两列布局
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📊 Input Features")
    
    # 特征变量输入
    inputs = {}
    
    # 第一组特征
    st.subheader("Vital Signs")
    inputs['GCS'] = st.number_input("GCS (Glasgow Coma Scale)", min_value=3.0, max_value=15.0, value=15.0, step=0.1)
    inputs['RR'] = st.number_input("RR (Respiratory Rate, /min)", min_value=0.0, max_value=60.0, value=20.0, step=0.1)
    inputs['T'] = st.number_input("T (Temperature, °C)", min_value=30.0, max_value=45.0, value=37.0, step=0.1)
    inputs['NBPS'] = st.number_input("NBPS (Systolic Blood Pressure, mmHg)", min_value=0.0, max_value=300.0, value=120.0, step=0.1)
    
    st.subheader("Laboratory Tests")
    inputs['WBC'] = st.number_input("WBC (White Blood Cell Count, ×10⁹/L)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
    inputs['HGB'] = st.number_input("HGB (Hemoglobin, g/dL)", min_value=0.0, max_value=30.0, value=12.0, step=0.1)
    inputs['ANION_GAP'] = st.number_input("ANION_GAP (Anion Gap, mEq/L)", min_value=0.0, max_value=50.0, value=12.0, step=0.1)
    inputs['CHLORIDE'] = st.number_input("CHLORIDE (Chloride, mEq/L)", min_value=0.0, max_value=200.0, value=105.0, step=0.1)
    inputs['SODIUM'] = st.number_input("SODIUM (Sodium, mEq/L)", min_value=0.0, max_value=200.0, value=140.0, step=0.1)
    inputs['BUN'] = st.number_input("BUN (Blood Urea Nitrogen, mg/dL)", min_value=0.0, max_value=200.0, value=20.0, step=0.1)
    inputs['CR'] = st.number_input("CR (Creatinine, mg/dL)", min_value=0.0, max_value=20.0, value=1.0, step=0.1)
    inputs['INRPT'] = st.number_input("INRPT (International Normalized Ratio)", min_value=0.5, max_value=10.0, value=1.0, step=0.1)
    inputs['BS'] = st.number_input("BS (Blood Sugar, mg/dL)", min_value=0.0, max_value=500.0, value=100.0, step=0.1)
    
    st.subheader("Scoring Systems")
    inputs['SOFA'] = st.number_input("SOFA (Sequential Organ Failure Assessment)", min_value=0.0, max_value=24.0, value=0.0, step=0.1)
    inputs['SAPSII'] = st.number_input("SAPSII (Simplified Acute Physiology Score II)", min_value=0.0, max_value=200.0, value=30.0, step=0.1)
    inputs['OASIS'] = st.number_input("OASIS (Oxford Acute Severity of Illness Score)", min_value=0.0, max_value=100.0, value=20.0, step=0.1)
    
    st.subheader("Treatment Measures")
    inputs['BALANCE'] = st.number_input("BALANCE (Fluid Balance, mL)", min_value=-50000.0, max_value=50000.0, value=0.0, step=100.0)
    inputs['MV'] = st.selectbox("MV (Mechanical Ventilation)", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    inputs['CRRT'] = st.selectbox("CRRT (Continuous Renal Replacement Therapy)", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    inputs['NOR'] = st.selectbox("NOR (Norepinephrine)", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

with col2:
    st.header("📈 Prediction Results")
    
    # 计算按钮
    if st.button("🔍 Calculate Sepsis Risk", type="primary", use_container_width=True):
        # 准备输入数据
        input_data = pd.DataFrame([inputs])
        
        # 确保列顺序正确
        input_data = input_data[feature_cols]
        
        # 预测
        prediction_proba = model.predict_proba(input_data)[0]
        risk_score = prediction_proba[1] * 100  # 转换为百分比
        
        # 显示风险评分
        st.markdown("---")
        st.metric("Sepsis Risk Score", f"{risk_score:.2f}%")
        
        # 风险等级
        if risk_score < 30:
            risk_level = "Low Risk"
            risk_color = "🟢"
        elif risk_score < 60:
            risk_level = "Medium Risk"
            risk_color = "🟡"
        else:
            risk_level = "High Risk"
            risk_color = "🔴"
        
        st.markdown(f"### {risk_color} Risk Level: **{risk_level}**")
        
        # 进度条
        st.progress(risk_score / 100)
        
        # 计算SHAP值
        st.markdown("---")
        st.subheader("🔬 SHAP Explanation")
        
        with st.spinner("Calculating SHAP values..."):
            try:
                shap_values = explainer.shap_values(input_data)
                
                # 如果是多类输出，取正类的SHAP值
                if isinstance(shap_values, list):
                    shap_values_array = shap_values[1]  # 正类的SHAP值
                    expected_value = explainer.expected_value[1] if isinstance(explainer.expected_value, (list, np.ndarray)) else explainer.expected_value
                else:
                    shap_values_array = shap_values
                    expected_value = explainer.expected_value
                
                # 确保shap_values_array是1维数组
                if shap_values_array.ndim > 1:
                    shap_values_1d = shap_values_array[0].flatten()
                else:
                    shap_values_1d = shap_values_array.flatten()
                
                # 如果长度不匹配，只取前len(feature_cols)个
                if len(shap_values_1d) != len(feature_cols):
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
                
                # 创建SHAP力图
                st.markdown("#### SHAP Force Plot")
                try:
                    # 使用新版本的SHAP API
                    # 创建Explanation对象用于force plot
                    explanation_force = shap.Explanation(
                        values=shap_values_1d,
                        base_values=expected_value,
                        data=input_data.iloc[0].values,
                        feature_names=feature_cols
                    )
                    
                    # 尝试使用shap.plots.force (新API v0.20+)
                    try:
                        plt.figure(figsize=(12, 4))
                        shap.plots.force(explanation_force, matplotlib=True, show=False)
                        st.pyplot(plt)
                        plt.close()
                    except AttributeError:
                        # 如果shap.plots不存在，尝试旧API
                        try:
                            plt.figure(figsize=(12, 4))
                            shap.force_plot(
                                expected_value,
                                shap_values_1d,
                                input_data.iloc[0],
                                matplotlib=True,
                                show=False
                            )
                            st.pyplot(plt)
                            plt.close()
                        except:
                            raise Exception("使用替代可视化")
                    except Exception:
                        raise Exception("使用替代可视化")
                        
                except Exception as e:
                    # 使用条形图替代
                    min_len = min(len(feature_cols), len(shap_values_1d))
                    shap_df_temp = pd.DataFrame({
                        'Feature': feature_cols[:min_len],
                        'SHAP Value': shap_values_1d[:min_len]
                    })
                    shap_df_temp = shap_df_temp.sort_values('SHAP Value', key=abs, ascending=False)
                    fig, ax = plt.subplots(figsize=(10, 8))
                    colors = ['red' if x < 0 else 'blue' for x in shap_df_temp['SHAP Value']]
                    ax.barh(shap_df_temp['Feature'], shap_df_temp['SHAP Value'], color=colors)
                    ax.set_xlabel('SHAP Value', fontsize=12)
                    ax.set_title('SHAP Force Plot - Feature Contribution', fontsize=14, fontweight='bold')
                    ax.axvline(x=0, color='black', linestyle='--', linewidth=0.5)
                    ax.grid(axis='x', alpha=0.3)
                    st.pyplot(fig)
                    plt.close()
                
                # 创建SHAP瀑布图
                st.markdown("#### SHAP Waterfall Plot")
                try:
                    # 创建Explanation对象
                    explanation = shap.Explanation(
                        values=shap_values_1d,
                        base_values=expected_value,
                        data=input_data.iloc[0].values,
                        feature_names=feature_cols
                    )
                    plt.figure(figsize=(12, 8))
                    # 尝试新API
                    try:
                        shap.plots.waterfall(explanation, show=False)
                    except AttributeError:
                        # 如果新API不存在，使用旧API
                        shap.waterfall_plot(explanation, show=False)
                    st.pyplot(plt)
                    plt.close()
                except Exception as e:
                    # 使用累积条形图替代瀑布图
                    min_len = min(len(feature_cols), len(shap_values_1d))
                    shap_df_temp = pd.DataFrame({
                        'Feature': feature_cols[:min_len],
                        'SHAP Value': shap_values_1d[:min_len]
                    })
                    shap_df_temp = shap_df_temp.sort_values('SHAP Value', ascending=False)
                    shap_df_temp['Cumulative'] = shap_df_temp['SHAP Value'].cumsum() + expected_value
                    
                    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
                    
                    # 上：SHAP值条形图
                    colors = ['red' if x < 0 else 'blue' for x in shap_df_temp['SHAP Value']]
                    ax1.bar(range(len(shap_df_temp)), shap_df_temp['SHAP Value'], color=colors)
                    ax1.set_xticks(range(len(shap_df_temp)))
                    ax1.set_xticklabels(shap_df_temp['Feature'], rotation=45, ha='right')
                    ax1.set_ylabel('SHAP Value', fontsize=12)
                    ax1.set_title('SHAP Waterfall Plot - Feature Contribution', fontsize=14, fontweight='bold')
                    ax1.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
                    ax1.grid(axis='y', alpha=0.3)
                    
                    # 下：累积值
                    ax2.plot(range(len(shap_df_temp)), shap_df_temp['Cumulative'], marker='o', linewidth=2, markersize=6)
                    ax2.axhline(y=expected_value, color='green', linestyle='--', linewidth=1, label=f'Base Value: {expected_value:.4f}')
                    ax2.set_xticks(range(len(shap_df_temp)))
                    ax2.set_xticklabels(shap_df_temp['Feature'], rotation=45, ha='right')
                    ax2.set_ylabel('Cumulative SHAP Value', fontsize=12)
                    ax2.set_title('Cumulative SHAP Value Change', fontsize=14, fontweight='bold')
                    ax2.legend()
                    ax2.grid(alpha=0.3)
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close()
                
                # 特征重要性表格
                st.markdown("#### Feature Contribution")
                min_len = min(len(feature_cols), len(shap_values_1d), len(input_data.iloc[0].values))
                shap_df = pd.DataFrame({
                    'Feature': feature_cols[:min_len],
                    'SHAP Value': shap_values_1d[:min_len],
                    'Feature Value': input_data.iloc[0].values[:min_len]
                })
                shap_df = shap_df.sort_values('SHAP Value', key=abs, ascending=False)
                shap_df['SHAP Value'] = shap_df['SHAP Value'].round(4)
                shap_df['Feature Value'] = shap_df['Feature Value'].round(2)
                st.dataframe(shap_df, use_container_width=True, hide_index=True)
                
            except Exception as e:
                st.error(f"SHAP calculation failed: {e}")
                import traceback
                st.code(traceback.format_exc())

# 侧边栏信息
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    ### Pressure Injuries in Sepsis
    #### Sepsis Risk Score Calculator
    
    This calculator uses a Random Forest model with 20 features to predict Sepsis risk.
    
    **Model Information:**
    - Training Set: MIMIC-IV (after SMOTE-NC processing)
    - Test Set: MIMIC-III
    - Model: Random Forest
    - Features: 20
    
    **How to Use:**
    1. Enter patient features on the left
    2. Click "Calculate Sepsis Risk" button
    3. View risk score and SHAP visualizations
    
    **Disclaimer:**
    - This tool is for research purposes only
    - Not a substitute for clinical judgment
    - Please input accurate values based on actual conditions
    """)
    
    st.markdown("---")
    st.markdown("**Development Info**")
    st.caption("Trained with optimal Random Forest parameters")

# 页脚
st.markdown("---")
st.caption("© 2024 Pressure Injuries in Sepsis | For Research Use Only")

