import os


def process_tdump_fixed_format(input_file, output_file):
    """
    讀取 HYSPLIT tdump 檔案，從第 68 行開始，
    將 Latitude (緯度) 和 Longitude (經度) 各減去 0.06。
    輸出時嚴格保持原始的固定欄寬格式。
    """

    # 設定目標行數 (從第 68 行開始處理，程式內部 index 從 0 開始，所以是 67)
    TARGET_START_LINE = 68

    try:
        with open(input_file, 'r', encoding='utf-8') as f_in, \
                open(output_file, 'w', encoding='utf-8', newline='') as f_out:

            print(f"正在處理檔案: {input_file} ...")

            for line_idx, line in enumerate(f_in, 1):
                # 1. 如果未達到目標行數，直接寫入原始內容 (保留 Header)
                if line_idx < TARGET_START_LINE:
                    f_out.write(line)
                    continue

                parts = line.split()

                # 2. 判斷是否為標準軌跡資料行 (通常大於 11 個欄位)
                # HYSPLIT 標準格式：
                # Col 1-8: Integers (軌跡編號, 網格, 年, 月, 日, 時, 分, 預報時)
                # Col 9: Float (Age)
                # Col 10: Float (Lat) -> 目標
                # Col 11: Float (Lon) -> 目標
                # Col 12+: Floats (Height, Pressure, etc.)
                if len(parts) >= 12:
                    try:
                        # 抓取原始數值
                        # 注意：parts 是以空白分割的 list，index 9 是緯度，10 是經度
                        raw_lat = float(parts[9])
                        raw_lon = float(parts[10])

                        # 執行運算
                        new_lat = raw_lat - 0.08
                        new_lon = raw_lon - 0.07

                        # 3. 建構格式化字串 (嚴格模仿原檔案的欄寬)
                        # 參考原始數據: "     1     1    25    12..."
                        # Integers: 寬度 6
                        # Age: 寬度 8, 小數 1
                        # Lat/Lon: 寬度 9, 小數 3
                        # Height/Meteo: 寬度 9, 小數 1

                        # 處理前 8 個整數欄位
                        formatted_line = ""
                        for i in range(8):
                            formatted_line += f"{int(parts[i]):6d}"

                        # 處理 Age (Index 8)
                        formatted_line += f"{float(parts[8]):8.1f}"

                        # 處理 Lat (Index 9) - 修改後
                        formatted_line += f"{new_lat:9.3f}"

                        # 處理 Lon (Index 10) - 修改後
                        formatted_line += f"{new_lon:9.3f}"

                        # 處理其餘欄位 (Height + Meteo data)
                        # 這些通常是寬度 9，小數點 1 位
                        for p in parts[11:]:
                            formatted_line += f"{float(p):9.1f}"

                        # 加上換行符號寫入
                        f_out.write(formatted_line + "\n")

                    except ValueError:
                        # 如果轉換數字失敗，寫入原行以防萬一
                        f_out.write(line)
                else:
                    # 如果欄位不足 (可能是空行或異常結構)，保持原樣
                    f_out.write(line)

        print(f"處理完成！")
        print(f"新檔案已儲存為: {output_file}")

    except FileNotFoundError:
        print(f"錯誤：找不到檔案 '{input_file}'。請確認檔案名稱是否正確。")
    except Exception as e:
        print(f"發生未預期的錯誤: {e}")


# ==========================================
# 執行區塊
# ==========================================
if __name__ == "__main__":
    # 設定檔案名稱
    input_filename = 'C:/Users/ex-al/OneDrive/桌面/Work/Pycharm/data/tdump.2025-11-24-1800.Backward.txt'
    output_filename = 'C:/Users/ex-al/OneDrive/桌面/Work/Pycharm/AP-Monitor/database/tdump.2025-11-24-1800.Backward.txt'

    process_tdump_fixed_format(input_filename, output_filename)


