import random


def selection_sort(num):
    for i in range(len(num)):
        minimum = i
        for j in range(i+1, len(num)): # i보다 하나 큰 수부터 list끝까지 iterate한다
            if num[j] < num[minimum]: 
                minimum = j # list내에 제일 작은 숫자를 찾고 그 index를 minumum 변수에 저장한다
        if minimum != i: 
            num[i], num[minimum] = num[minimum], num[i]
    return num
    


def insertion_sort(num):
    for j in range(1,len(num)):
        key = num[j]
        i = j - 1
        while i>=0 and (num[i] > key): # i가 list맨 앞까지 오던지, num[i]가 위에 저장된 num[j]보다 작으면 loop빠져 나온다.
            num[i+1] = num[i]
            i -= 1
        num[i+1] = key
    return num


def bubble_sort(num):
    for i in range(len(num)):
        for j in range(len(num)-1-i): # 맨 앞부터 비교를 시작한다
            if num[j]>num[j+1]:
                num[j], num[j+1] = num[j+1], num[j] # swap한다
    return num

number = [i for i in range(10)]
random.shuffle(number)
print(number)
# selection = selection_sort(number)
# print(selection)

# insertion = insertion_sort(number)
# print(insertion)

bubble = bubble_sort(number)
print(bubble)