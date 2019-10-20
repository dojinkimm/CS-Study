def knapsack_2d():
    N, W = 4, 5
    w = [2, 3, 4, 5]
    b = [3, 4, 5, 6]

    knap = [[0 for _ in range(W+1)] for _ in range(N+1)]

    for i in range(N+1):
        for j in range(W+1):
            if w[i-1] <= j: 
                knap[i][j] = max(b[i-1] + knap[i-1][j-w[i-1]],  knap[i-1][j]) 
            else: 
                knap[i][j] = knap[i-1][j] 

            print(knap)

def knapsack_1d():
    N, W = 4, 5
    bag = [(2,3), (3,4), (4,5), (5,6)] # (weight,benefit) 순서

    knap = [0 for _ in range(W+1)]

    for i in range(N):
        for j in range(W, 1, -1):
            if bag[i][0] <= j:
                knap[j] = max(knap[j], knap[j-bag[i][0]] + bag[i][1])

    print(knap)

def knapsack_greedy():
    N, W = 4, 5
    w = [2, 3, 4, 5]
    b = [3, 4, 5, 6]
    ratio = [[0, 0] for _ in range(N)] # 왼쪽은 ratio값, 오른쪽은 index를 저장한다

    for i in range(N):
        ratio[i][0] = b[i]/w[i]
        ratio[i][1] = i 

    ans = 0
    for r in sorted(ratio, key=lambda x:-x[0]):
        if w[r[1]] <= W:
            W -= w[r[1]]
            ans += b[r[1]]
        else:
            ans += (W * r[0])
            break
    print(ans)



if __name__=="__main__":
    knapsack_2d()
    knapsack_1d()
    knapsack_greedy()