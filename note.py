import os
import shutil
import json
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD

# 使用者輸入的文字儲存為txt檔的功能
def save_text_to_file(text, filename):
    with open(filename, 'w') as file:
        file.write(text)

# 從本地檔案複製圖片到指定的資料夾
def save_image_from_local(image_path, destination_folder):
    if not os.path.isfile(image_path):
        print("檔案不存在。請確認檔案路徑正確")
        return
    
    file_extension = os.path.splitext(image_path)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png']
    
    if file_extension not in valid_extensions:
        print("不支援的檔案格式。只支援.jpg, .jpeg, .png檔案")
        return

    destination_path = os.path.join(destination_folder, os.path.basename(image_path))
    shutil.copy(image_path, destination_path)

def drop(event):
    image_path = event.data
    save_image_from_local(image_path, '.')
    # 儲存圖片路徑
    with open('history.json', 'r+') as file:
        history = json.load(file)
        history['image_path'] = image_path
        file.seek(0)
        json.dump(history, file)

def main():
    # 讀取歷史紀錄
    if not os.path.isfile('history.json'):
        with open('history.json', 'w') as file:
            json.dump({'text': '', 'image_path': ''}, file)
    with open('history.json', 'r') as file:
        history = json.load(file)
        print("Previous text: ", history['text'])
        print("Previous image path: ", history['image_path'])

    # 使用者輸入文字
    text = input("請輸入要保存的文字：")
    # 儲存為txt檔，並更新歷史紀錄
    save_text_to_file(text, 'notes.txt')
    with open('history.json', 'r+') as file:
        history = json.load(file)
        history['text'] = text
        file.seek(0)
        json.dump(history, file)

    root = TkinterDnD.Tk()
    button = tk.Button(root, text='Drag and drop your image file here...')
    button.pack(fill=tk.BOTH, expand=tk.YES)
    button.drop_target_register(DND_FILES)
    button.dnd_bind('<<Drop>>', drop)

    root.mainloop()

if __name__ == "__main__":
    main()
