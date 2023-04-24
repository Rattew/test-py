import sys
import random
from prettytable import PrettyTable

print('''Добро пожаловать в игру "Быки и коровы"! Правила простые: необходимо
придумать 4-значное число без повторяющихся цифр и угадать число соперника
первым. При каждой попытке игра будет вам сообщать, насколько вы близки
к успеху. "Бык" - цифра присутствует в числе и стоит на своем месте, "корова" -
цифра есть, но она не на своем месте. Удачи!''')

#функция проверяет ввод(пока не получит 4-значное число без повторов)
def user_data():    
    check = 'False'
    while check != 'True':
        print('Введите число:')
        user_number = input()
        if user_number.isdigit() and len(user_number) == 4:
            user_number = list(map(int, user_number))
            if len(set(user_number)) == 4:
                check = 'True'
                return user_number
            else:
                print('Ошибка ввода, введите 4-значное число без повторов:')
        else:
            print('Ошибка ввода, введите 4-значное число без повторов:')

#функция рисует таблицу
def draw_table(player_number, comp_guess, comp_att, guess_number, user_att):    
    global turn_count    
    if turn_count == 1:
        tbl = ["Ход", player_number, "Быки", "Коровы", "Число компьютера", "Быки ", "Коровы "]
        columns = len(tbl)
        table = PrettyTable(tbl)
        table.add_row([">", "Ход компьютера", "<<<", "<<<", "Ход Игрока", "<<<", "<<<" ])
        print(table)
        return table
    else:
        global header
        y = int(turn_count / 2)
        header.add_row([y, comp_guess, comp_att[0], comp_att[1], guess_number, user_att[0], user_att[1]])
        print(header)    

#функция ведет подсчет быков и коров
def score_counter(guess_number):
    bulls, cows = 0, 0
    global turn_count    
    if turn_count % 2 != 0:
        x = player_number
    else:
        x = comp_number    
    for i in range(4):
        for j in range(4):
            if i == j and x[i] == guess_number[j]:
                bulls += 1                
            elif i != j and x[i] == guess_number[j]:
                cows += 1                
            else:
                continue
    return bulls, cows

#функция определяет все возможные варианты ответов для компьютера
def get_all_answers():
    ans = []
    for i in range(10000):
        tmp = str(i).zfill(4)
        if len(set(map(int, tmp))) == 4:
            ans.append(list(map(int, tmp)))
    return ans
    
#функция выбора одного варианта из множества уникальных
def get_one_answer(answers):
    num = random.choice(answers)
    return num

#функция удаляет неверные варианты из множества уникальных
def del_bad_answers(answers, comp_guess, comp_att):
    ans_c = answers[:]
    deleted = 'false'
    if comp_att[1] == 4 or comp_att[0] + comp_att[1] == 4 :
        for x in range(len(answers)):
            ansi = answers[x]
            cross = set(comp_guess) - set(ansi)
            if len(cross) > 0:
                ans_c.remove(ansi)
                deleted = 'true'                
    elif comp_att[0] + comp_att[1] == 0:
        for x in range(len(answers)):
            ansi = answers[x]
            garbage = 'false'       
            for y in range(4):
                for z in range(4):
                    if comp_guess[y] == ansi[z]:
                        garbage = 'true'
                        break
            if garbage == 'true':
                ans_c.remove(ansi)
                deleted = 'true'   
    elif comp_att[0] == 0 and comp_att[1] != 0:
        for x in range(len(answers)):
            ansi = answers[x]
            garbage = 'false'
            for y in range(4):
                for z in range(4):
                    if y == z and comp_guess[y] == ansi[z]:
                        garbage = 'true'
            if garbage == 'true':
                ans_c.remove(ansi)
                deleted = 'true'               
    elif comp_att[1] == 0 and comp_att[0] != 0:
        for x in range(len(answers)):
            ansi = answers[x]
            garbage = 'false'
            for y in range(4):
                for z in range(4):
                    if y != z and comp_guess[y] == ansi[z]:
                        garbage = 'true'
            if garbage == 'true':
                ans_c.remove(ansi)
                deleted = 'true'
    else:
        ans_c.remove(comp_guess)
        deleted = 'true'
    if deleted == 'false':
        ans_c.remove(comp_guess)    
    #print('Вариантов у компьютера:', len(ans_c))
    return ans_c
       
#основной цикл программы
turn_count = 1
answers = get_all_answers()
player_number = user_data()
comp_number = get_one_answer(answers)
header = draw_table(player_number, 0, 0, 0, 0)
while True:
    if turn_count % 2 != 0:
        comp_guess = get_one_answer(answers)
        comp_att = score_counter(comp_guess)
        answers = del_bad_answers(answers, comp_guess, comp_att)
        if comp_att[0] == 4:
            print('Победил компьютер! Ваше число:', player_number)
            break
        else:
            turn_count += 1
    else:
        print('Ход игрока')
        guess_number = user_data()
        user_att = score_counter(guess_number)
        if user_att[0] == 4:
            print('Победил игрок!')
            break
        else:
            draw_table(player_number, comp_guess, comp_att, guess_number, user_att)
            turn_count += 1
print('Игра окончена.')
x = input()




    
