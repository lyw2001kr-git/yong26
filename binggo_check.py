import tkinter as tk
from tkinter import messagebox
import json

# cards.json 파일 읽기 (같은 폴더에 있어야 함)
try:
    with open('cards.json', 'r', encoding='utf-8') as f:
        EXISTING_CARDS = json.load(f)
    print(f"카드 로드 성공: {len(EXISTING_CARDS)}장")  # cmd에 로그
except Exception as e:
    messagebox.showerror("파일 오류", f"cards.json 읽기 실패:\n{e}")
    exit()

def normalize_grid_for_compare(grid):
    """중앙 값 완전 무시하고 나머지 24개 숫자만 비교"""
    normalized = []
    for i, row in enumerate(grid):
        new_row = []
        for j, cell in enumerate(row):
            if i == 2 and j == 2:  # 중앙 무시 (값 무관)
                continue
            new_row.append(cell if isinstance(cell, int) else 0)
        normalized.append(tuple(new_row))
    return tuple(normalized)

existing_grids = {normalize_grid_for_compare(card["grid"]) for card in EXISTING_CARDS}

def check_card():
    grid = []
    
    for i in range(5):
        row = []
        for j in range(5):
            value = entries[i][j].get().strip()
            if value == "":
                messagebox.showerror("오류", "모든 칸을 채워주세요!")
                return
            try:
                num = int(value)
                row.append(num)
            except ValueError:
                messagebox.showerror("오류", f"행{i+1} 열{j+1}에 숫자만 입력하세요!")
                return
        grid.append(row)
    
    # 비교용 grid 생성 (중앙 무시)
    grid_tuple = normalize_grid_for_compare(grid)
    
    matched = False
    matched_id = None
    
    for card in EXISTING_CARDS:
        if normalize_grid_for_compare(card["grid"]) == grid_tuple:
            matched = True
            matched_id = card["card_id"]
            break
    
    if matched:
        messagebox.showinfo("결과", f"중복입니다!\ncard_id: {matched_id}")
    else:
        messagebox.showinfo("결과", "새로운 카드입니다!")
    
    clear_entries()

def clear_entries():
    for i in range(5):
        for j in range(5):
            entries[i][j].delete(0, tk.END)

# 메인 창
root = tk.Tk()
root.title("5x5 빙고 카드 입력 & 중복 체크")
root.geometry("600x600")
root.resizable(False, False)

tk.Label(root, text="5x5 빙고 카드 입력 (중앙 포함)", font=("맑은 고딕", 14, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=20)

entries = []
for i in range(5):
    row = []
    for j in range(5):
        entry = tk.Entry(frame, width=6, font=("맑은 고딕", 18), justify="center")
        entry.grid(row=i, column=j, padx=5, pady=5)
        row.append(entry)
    entries.append(row)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="중복 확인", font=("맑은 고딕", 14), bg="#4CAF50", fg="white",
          command=check_card, width=12).pack(side=tk.LEFT, padx=10)

tk.Button(btn_frame, text="지우기", font=("맑은 고딕", 14), bg="#2196F3", fg="white",
          command=clear_entries, width=10).pack(side=tk.LEFT, padx=10)

tk.Button(btn_frame, text="종료", font=("맑은 고딕", 14), bg="#f44336", fg="white",
          command=root.quit, width=10).pack(side=tk.LEFT, padx=10)

root.mainloop()