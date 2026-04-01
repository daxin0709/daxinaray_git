import os
import sys
import pandas as pd

# 自動切換到檔案所在資料夾，避免 [Errno 2]
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    from pysor import SOR
    print("✅ 成功載入 pysor 模組")
except ImportError:
    print("❌ 依舊找不到 pysor，請確認終端機左側是否有 (venv) 字樣")
    sys.exit()

def convert_sor(file_path):
    try:
        sor = SOR(file_path)
        
        # 獲取波形數據
        y_values = sor.get_data_points()
        
        # 獲取解析度 (如果屬性名不對，pysor 通常是用以下方式存取)
        # 注意：若執行失敗，請檢查 sor.fixed_parameters 的屬性
        res = sor.fixed_parameters.resolution
        x_values = [i * res / 10**4 for i in range(len(y_values))]

        df = pd.DataFrame({
            'Distance_km': x_values,
            'Power_dB': y_values
        })

        output_path = file_path.replace('.sor', '.csv')
        df.to_csv(output_path, index=False)
        print(f"📊 轉換成功！產出檔案: {output_path}")
        
    except Exception as e:
        print(f"❌ 解析出錯: {e}")

# 請確保 test.sor 檔案放在同一個資料夾
target_file = "test.sor" 
if os.path.exists(target_file):
    convert_sor(target_file)
else:
    # 這裡會印出目前資料夾有哪些檔案，方便你除錯
    print(f"❌ 找不到檔案 '{target_file}'。目前資料夾下的檔案有: {os.listdir('.')}")