import numpy as np
import locale

#ภาษาไทย
locale.setlocale(locale.LC_ALL, 'th_TH.UTF-8')

def create_sudoku():
    # สร้างตาราง 9x9
    sudoku = np.zeros((9, 9), dtype=int)
    fill_sudoku(sudoku)
    return sudoku

def fill_sudoku(sudoku):
    # สร้างตาราง Sudoku ด้วยเลขเริ่มต้น
    fill_diagonal_regions(sudoku)
    solve_sudoku(sudoku)
    remove_numbers(sudoku)

def fill_diagonal_regions(sudoku):
    # สร้างตาราง Sudoku ที่มีเลขเริ่มต้นในแต่ละพื้นที่ 3x3 แนวทะแยง
    for i in range(0, 9, 3):
        fill_region(sudoku, i, i)

def fill_region(sudoku, row, col):
    # สร้างตาราง 3x3 ที่ไม่มีเลขซ้ำกันในแต่ละแถวและคอลัมน์
    nums = list(range(1, 10))
    np.random.shuffle(nums)
    num_idx = 0
    for i in range(3):
        for j in range(3):
            sudoku[row + i, col + j] = nums[num_idx]
            num_idx += 1

def solve_sudoku(sudoku):
    # ใช้วิธี Backtracking ในการแก้ปัญหา Sudoku
    find_empty = find_empty_cell(sudoku)
    if not find_empty:
        return True  # ถ้าไม่มีช่องว่างแสดงว่าเราได้แก้ปัญหาแล้ว
    row, col = find_empty

    for num in range(1, 10):
        if is_valid_move(sudoku, row, col, num):
            sudoku[row, col] = num
            if solve_sudoku(sudoku):
                return True
            sudoku[row, col] = 0  # ถ้าไม่สามารถแก้ปัญหาในที่นี้ได้ให้รีเซ็ตเป็น 0

    return False

def find_empty_cell(sudoku):
    # ค้นหาช่องว่างใน Sudoku
    for row in range(9):
        for col in range(9):
            if sudoku[row, col] == 0:
                return (row, col)
    return None

def is_valid_move(sudoku, row, col, num):
    # ตรวจสอบว่าการเลือกเลข num ไปยังตำแหน่ง (row, col) เป็นที่ยอมรับหรือไม่
    # ต้องไม่มีเลข num ในแถวและคอลัมน์เดียวกันและในพื้นที่ 3x3 ที่เข้าข่ายเดียวกัน
    return (
        not in_row(sudoku, row, num)
        and not in_col(sudoku, col, num)
        and not in_region(sudoku, row - row % 3, col - col % 3, num)
    )

def in_row(sudoku, row, num):
    # ตรวจสอบว่ามีเลข num ในแถว row หรือไม่
    return num in sudoku[row, :]

def in_col(sudoku, col, num):
    # ตรวจสอบว่ามีเลข num ในคอลัมน์ col หรือไม่
    return num in sudoku[:, col]

def in_region(sudoku, row, col, num):
    # ตรวจสอบว่ามีเลข num ในพื้นที่ 3x3 ที่เข้าข่ายโดยการระบุตำแหน่ง row และ col หรือไม่
    return num in sudoku[row : row + 3, col : col + 3]

def remove_numbers(sudoku):
    # ลบบางตำแหน่งออกจาก Sudoku เพื่อสร้างเกม Sudoku แบบเริ่มต้น
    num_to_remove = np.random.randint(30, 50)
    for _ in range(num_to_remove):
        row, col = np.random.randint(9), np.random.randint(9)
        while sudoku[row, col] == 0:
            row, col = np.random.randint(9), np.random.randint(9)
        sudoku[row, col] = 0

def is_solved(sudoku):
    # ตรวจสอบว่า Sudoku ถูกแก้ครบถ้วนหรือไม่
    return not any(0 in row for row in sudoku)

if __name__ == "__main__":
    sudoku = create_sudoku()
    print(sudoku)
def check_solution(player_solution, solved_solution):
    return np.array_equal(player_solution, solved_solution)

def print_sudoku(sudoku):
    # ฟังก์ชันนี้ใช้สำหรับพิมพ์ Sudoku ในรูปแบบที่สะดวกต่อการเล่น
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)  # พิมพ์เส้นขีดแบ่งระหว่างพื้นที่ 3x3
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")  # พิมพ์เส้นแบ่งระหว่างคอลัมน์ 3
            if sudoku[i, j] == 0:
                print(".", end=" ")  # แสดงช่องว่างเมื่อตำแหน่งว่าง
            else:
                print(sudoku[i, j], end=" ")
        print()

def play_sudoku():
    num_attempts = 0  # รีเซ็ตค่า  เมื่อเริ่มเกมใหม่
    while True:
        sudoku = create_sudoku()  # สร้าง Sudoku ใหม่ทุกครั้งที่เริ่มเกมใหม่
        print("ยินดีต้อนรับสู่เกม Sudoku!")
        print("นี่คือ Sudoku ของคุณ:")
        print_sudoku(sudoku)

        while not is_solved(sudoku):
            row = int(input("ป้อนแถว (1-9): ")) - 1
            col = int(input("ป้อนคอลัมน์ (1-9): ")) - 1
            num = int(input("ป้อนตัวเลข (1-9): "))
            
            if 1 <= num <= 9:
                if is_valid_move(sudoku, row, col, num):
                    sudoku[row, col] = num
                else:
                    print("ไม่ถูกต้อง! ตัวเลขนี้ไม่สามารถใช้งานได้ในตำแหน่งนี้")
                    num_attempts += 1  # เพิ่มจำนวนครั้งที่ผิด
            else:
                print("ไม่ถูกต้อง! โปรดป้อนตัวเลขระหว่าง 1 ถึง 9.")
                num_attempts += 1  # เพิ่มจำนวนครั้งที่ผิด

            print_sudoku(sudoku)
                
            

            if num_attempts >= 5:
                print("คุณผิดเกม Sudoku เกิน 5 ครั้ง! เริ่มเกมใหม่\n")
                num_attempts = 0  # รีเซ็ตค่า num_attempts เมื่อเริ่มเกมใหม่

        if is_solved(sudoku):
            print("ยินดีด้วย! คุณชนะ Sudoku แล้ว!\n")
            

if __name__ == "__main__":
   
   
   
    play_sudoku()
    