import os

# 設定目錄路徑
dir_path = "向下甩手//手在上"

# 取得目錄下所有檔案名稱
file_names = os.listdir(dir_path)

# 逐一更改檔名
count = 1
for file_name in file_names:
    if file_name.endswith(".jpg"):
        if count < 10: 
            new_file_name = "image_00" + str(count) + ".jpg"
        elif count >= 10 and count < 100:
            new_file_name = "image_0" + str(count) + ".jpg"
        else:
            new_file_name = "image_" + str(count) + ".jpg"

        print("第" + str(count) + "張")
        count += 1
        os.rename(os.path.join(dir_path, file_name), os.path.join(dir_path, new_file_name))

print("Done!")