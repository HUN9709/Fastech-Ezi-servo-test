import time

if __name__ == '__main__':
    a = 0
        
    start = time.time()


    for i in range(0, 10000, 1):
        for j in range(0, 10000, 1):
            a = 1-1

    end = time.time()

    print(end - start)