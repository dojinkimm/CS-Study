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


class QuickSort:
    def __init__(self, num):
        self.num = num

    def quick_sort(self, p, r):
        # p는 list시작, r은 끝, q는 중간인 pivot
        if p<r:
            q = self.partition(p,r)
            self.quick_sort(p,q-1) # pivot의 왼쪽을 다시 분할한다
            self.quick_sort(q+1,r) # pivot의 오른쪽을 다시 분할한다
        

    def partition(self, p, r):
        x = self.num[r] # pivot 값 저장
        i = p - 1
        for j in range(p, r): 
            if self.num[j] <= x: # pivot보다 작으면 해당 값을 pivot index보다 왼쪽으로 이동시킨다
                i += 1
                self.num[i], self.num[j] = self.num[j] ,self.num[i] 
        self.num[i+1], self.num[r] = self.num[r], self.num[i+1] # pivot을 전체 list에 정렬된 위치에 놓는다
        return i+1  # pivot의 위치를 리턴한다


def merge_sort(num): 
    if len(num) >1: 
        mid = len(num)//2 # list의 중간을 찾는다
        L = num[:mid] # list의 왼쪽을 분할한다
        R = num[mid:] # list의 오른쪽을 분할한다
  
        merge_sort(L) # 왼쪽 list를 정렬한다
        merge_sort(R) # 오른쪽 list를 정렬한다
  
        i = j = k = 0
          
        # 일시적으로 만든 L과 R을 비교한다
        while i < len(L) and j < len(R): 
            if L[i] < R[j]: # 왼쪽 list에 있던 item이 더 작으면 L[i]를 list 왼쪽에 위치하게 한다
                num[k] = L[i] 
                i+=1
            else: # 오른쪽 list에 있던 item이 더 작으면 R[j]를 list 왼쪽에 위치하게 한다
                num[k] = R[j] 
                j+=1
            k+=1
          
        # 위에 len(L) and len(R)이었기 때문에, 더 긴 list의 숫자가 남았을 것이다,
        # 그 숫자들을 이어 붙힌다.
        # 남은 숫자들은 크기 때문에 남은 것이기에 오른쪽에 붙혀진다
        while i < len(L): 
            num[k] = L[i] 
            i+=1
            k+=1
          
        while j < len(R): 
            num[k] = R[j] 
            j+=1
            k+=1

class HeapSort:
    def __init__(self, num, heapSize):
        self.num = num
        self.heapSize = heapSize

    def heap_sort(self):
        for i in range(len(self.num), -1, -1): 
            self.max_heapify(i) 
   
        for i in range(len(self.num)-1, 0, -1):
            self.num[0], self.num[i] = self.num[i], self.num[0]
            self.heapSize -= 1
            self.max_heapify(0)


    def max_heapify(self, i):
        largest = i
        L = 2 * i + 1
        R = 2 * i + 2
        
        if (L < self.heapSize) and (self.num[L] > self.num[i]):
            largest = L
        else:
            largest = i

        if (R < self.heapSize) and (self.num[R] > self.num[largest]):
            largest = R
        
        if largest != i:
            self.num[i], self.num[largest] = self.num[largest], self.num[i]
            self.max_heapify(largest)
         

def couting_sort(A, k):
    B = [0] * len(A)
    C = [0] * (k+1)

    for i in range(len(A)): # 각 element가 몇개있는지 C에 저장한다
        C[A[i]] += 1
    
    for i in range(1,len(C)): # C를 누적값으로 바꾼다
        C[i] += C[i-1]

    for i in range(len(A)): # C를 indexing해서 B에 저장한다
        B[C[A[i]]-1] = A[i]
        C[A[i]] -= 1

    return B


class RadixSort:
    def __init__(self, num):
        self.num = num

    def radix_sort(self):
        # 최대 digit을 알아보기 위해 가장 큰 수를 찾는다
        max1 = max(self.num) 
    
        exp = 1
        while max1/exp > 0: 
            self.count_sort(self.num,exp) 
            exp *= 10


    def count_sort(self, A, k):
        B = [0] * len(A)
        C = [0] * (10) # 1의 자리, 10의 자리수만 비교하기 때문에 범위는 0~9이다

        for i in range(0, len(A)): # 각 element가 몇개있는지 C에 저장한다
            index = (A[i]//k) 
            C[ (index)%10 ] += 1
        
        for i in range(1,10): # C를 누적값으로 바꾼다, 0~9까지 밖에 없다
            C[i] += C[i-1]

        i = len(A)-1
        while i>=0:  # C 를 indexing해서 정렬된 리스트를 찾는다
            index = (A[i]//k) 
            B[ C[ (index)%10 ] - 1] = A[i] 
            C[ (index)%10 ] -= 1
            i -= 1

        # 기존 리스트에 복사를 한다
        for i in range(len(A)): 
            A[i] = B[i] 


number = [i for i in range(10)]
random.shuffle(number)
print(number)
# selection = selection_sort(number)
# print(selection)

# insertion = insertion_sort(number)
# print(insertion)

# bubble = bubble_sort(number)
# print(bubble)

# quick = QuickSort(number)
# quick.quick_sort(0, len(number)-1) # list의 첫 index와 가장 마지막 index를 전달한다
# print(quick.num)

# merge = merge_sort(number)
# print(number)

# heap = HeapSort(number, len(number))
# heap.heap_sort()
# print(heap.num)

# counting_number = [1, 0, 3, 1, 0, 2, 5, 2, 1, 4]
# print(counting_number)
# count = couting_sort(counting_number, max(counting_number))
# print(count)


number = [ 170, 45, 75, 90, 802, 24, 2, 66] 
print(number)
radix = RadixSort(number)
radix.radix_sort() 
print(radix.num)
