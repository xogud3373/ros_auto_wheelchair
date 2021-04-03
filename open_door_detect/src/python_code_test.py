lis = [1,4,5,6,7,10,11,14,15,16,17,20]
#       0 1 2 3 4  5  6  7  8  9 10 11
#       
#       1,0,4,3,7,0,8,2,20,0 
array = []

count = 0

def hello():
    count = 0
    inf_start = 0
    array.append(lis[0])
    for i in range(1, len(lis)):
        a = lis[i] - lis[i - 1]
        if a == 1:
            inf_start += 1
            count += 1
            if i == len(lis) - 1 :
                array.append(count)

        if a > 1:
            inf_start += 1
            array.append(count)
            array.append(lis[inf_start])
            count = 0
            if i == len(lis) - 1 :
                array.append(count)
            
        
    print(array)
    #print(len(lis))

        

def qwer():
    global count
    for i in range(0, 20, count):
        if i == 5:
            count = 3
        print(i)

def zxcv():
    
    for i in range(0,10,2):
        if i == 2:
            break
        if i == 4:
            print("ehed")
        #a = lis[i] - lis[i - 1]    
        print(i)             
    

zxcv()
#hello()

