import json
import time
import argparse
from bisect import bisect_left, bisect_right

# --- TODO START --- #
# You can define any class or function
# You can import any python standard library : https://docs.python.org/3/library/
# However, you are not allowed to import any libraries other than python standard library, (such as numpy)
# --- TODO END --- #

#For 1st Solution
class MinHeap:
    def __init__(self):
        self.array = []
        self.size = 0
    def getSize(self):
        return self.size
    def insert(self, item):
        self.array.append(item)
        self.size += 1
        cur = self.size - 1
        while cur != 0:
            if self.array[(cur - 1) // 2] > self.array[cur]:
                self.array[(cur - 1) // 2], self.array[cur] = self.array[cur], self.array[(cur - 1) // 2]
                cur = (cur - 1) // 2
            else:
                break
    def peek(self):
        if self.size == 0:
            return
        else:
            return self.array[0]
    def removeMin(self):
        self.array[0] = self.array[self.size - 1]
        del self.array[self.size - 1]
        self.size -= 1
        cur = 1
        while True:
            l = 2 * cur
            r = 2 * cur + 1
            if r <= self.size:
                if self.array[cur - 1] <= min(self.array[l - 1], self.array[r - 1]):
                    break
                left = self.array[l - 1]
                right = self.array[r - 1]
                if left < right:
                    self.array[cur - 1], self.array[l - 1] = self.array[l - 1], self.array[cur - 1]
                    cur = l
                else:
                    self.array[cur - 1], self.array[r - 1] = self.array[r - 1], self.array[cur - 1]
                    cur = r
            elif l <= self.size and self.array[cur - 1] > self.array[l - 1]:
                self.array[cur - 1], self.array[l - 1] = self.array[l - 1], self.array[cur - 1]
                cur = l
            else:
                break
    def showMinHeap(self):
        return self.array

#For 2nd Solution
def update(bit, k, n):
    while k <= n:
        bit[k] += 1
        k += k & (-k)

def query(bit, k):
    s = 0
    while k > 0:
        s += bit[k]
        k -= k & (-k)
    return s

def check(mid, n, k, zero, prefix, unique):
    cnt = 0
    bit = [0] * (n + 1)
    update(bit, zero + 1, n)
    for i in range(1, n + 1):
        cnt += query(bit, bisect_right(unique, unique[prefix[i]] - mid - 1))
        update(bit, prefix[i] + 1, n)
    return cnt < k

def solution(json_input):
    # --- TODO START --- #

    array = json_input["array"]
    k = json_input["topk"]

    n = len(array)
    prefix = [0]
    for i in range(n):
        prefix.append(prefix[i] + array[i])

    #1st Solution: Can run in restricted runtime but O(n^2logk)
    answer = MinHeap()
    for i in range(n):
        for j in range(i + 1, n + 1):
            sum = prefix[j] - prefix[i]
            if answer.size < k:
                answer.insert(sum)
            elif sum > answer.peek():
                answer.removeMin()
                answer.insert(sum)

    json_sum = sorted(answer.showMinHeap(), reverse = True)

    '''#2nd Solution: O(nklogk) but will exceed restricted runtime
    R = max(prefix) - min(prefix)
    L = -R
    unique = sorted(set(prefix))
    zero = bisect_left(unique, 0)
    for i in range(1, n + 1):
        prefix[i] = bisect_left(unique, prefix[i])

    json_sum = []
    for i in range(k):
        r, l = R, L
        while r - l > 1:
            mid = (l + r) // 2
            if check(mid, n, i + 1, zero, prefix, unique):
                r = mid
            else:
                l = mid

        json_sum.append(r)'''

    # --- TODO END --- #
    return json_sum

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='input_1.json')
    parser.add_argument('--output', default='output_1.json')
    args = parser.parse_args()
    json_input = json.load(open(args.input, "r"))
    t1 = time.time()
    json_output = solution(json_input)
    t2 = time.time()
    json.dump(json_output, open(args.output, "w"))
    print("runtime of %s : %s" % (args.input, t2 - t1))

'''References: TIOJ 1208'''
