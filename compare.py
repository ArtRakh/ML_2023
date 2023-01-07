#!/bin/python3

import sys
import re
#from tqdm import tqdm

# для чтения файлов со скриптами
def access_data(path: str) -> None:
    with open(path) as f:
          code=f.read()
    return code

# каждый файл очищаю от спец.символов, оставляю только буквы, без регистра
def normalize(path: str) -> None:
    data=access_data(path)
    for ch in ['\a', '\b', '\f', '\t', '\r', '\v', ' ']:
        data = data.replace(ch, '')
    text=re.sub('[^а-яА-Яa-zA-Z]+', '', data).strip().lower()
    return text

# считаю редакционное расстояние
def lev_distant(f1: str, f2: str) -> None:
    n1, n2 = len(f1)+1, len(f2)+1
    # Проверить n1 <= n2, чтобы min корректно срабатывала
    if n1 > n2:
        f1, f2 = f2, f1
        n1, n2 = n2, n1
    # определяем матрцу D, первые две строки (в виде списка)
    D=[]
    D.append([k for k in range(n2)])
    D.append([0 for p in range(n2)])

    # Сокращаю complexity, перезаписывая только тек. и пред. строки матрицы ред. расстояний
    for i in range(1, n1):
        # для всех случаев, когда у матрицы нет 2ой строки для заполнения, мы добавляем ее
        if len(D)==1:
            D.append([0 for p in range(n2)])
        D[1][0]=i
        # субфункция, которая считает эти расстояния, заполняя вторую строку матрицы D
        D=sub_lev_distant(f1, f2, D, n2, i)
    return (D[-1][-1]/(n1-1))

# считает ред. расстояния в соответствии с процедурой Вагнера-Фишера
def sub_lev_distant(f1: str, f2: str, D, n2: int, i: int) -> None:

    for j in range(1, n2): 
        if f1[i-1] == f2[j-1]: 
            D[1][j] = min(
                D[0][j] + 1,
                D[0][j-1],
                D[1][j-1] + 1
            )
        else: 
            D[1][j] = min(
                D[0][j] + 1,
                D[0][j-1] + 1,
                D[1][j-1] + 1
            )
    return [D[1]]

# для каждой пары документов в файле input считает расстояние Левенштейна
# файл input предполагает последовательность двух документов для сравнения, разделенных единичным пробелом
def compare(input_file_path, scores_file_path):  
    with open(input_file_path) as f:
        str = [row.strip() for row in f]
    for k in range(len(str)):
        dist=lev_distant(normalize(str[k].split()[0]),
                         normalize(str[k].split()[1]))
        with open(scores_file_path, 'a') as file:
            file.write(f"{dist:.5f}"+'\n')

if __name__ == '__main__':
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    compare(arg1, arg2)
