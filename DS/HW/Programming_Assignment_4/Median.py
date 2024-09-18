
##Important! You shouldn't use statistics library! ("import statistics" is not allowed)

import math
class MinHeap: #Please store and implement MinHeap data structure with an array
    def __init__(self):
        self.array = []
        self.size = 0
    def getSize(self):
        return self.size
    def insert(self, item): #insert new item
    ### TODO ###
    ### input: a value ###
    ### You need not return or print anything with this function. ###
        self.array.append(item)
        self.size += 1

        cur = self.size - 1
        while cur != 0:
            if self.array[(cur - 1) // 2] > self.array[cur]:
                self.array[(cur - 1) // 2], self.array[cur] = self.array[cur], self.array[(cur - 1) // 2]
                cur = (cur - 1) // 2

            else:
                break

    def peek(self):  #Find Minimum item
        if self.size == 0:
            return
        else:
            return self.array[0]
    def removeMin(self):
    ### TODO ###
    ### You need not return or print anything with this function. ###
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

    def showMinHeap(self):  #Show MinHeap with array
        return self.array

class MaxHeap: #Please store and implement MinHeap data structure with an array
    def __init__(self):
        self.array = []
        self.size = 0
    def getSize(self):
        return self.size
    def insert(self, item): #insert new item
    ### TODO ###
    ### input: a value ###
    ### You need not return or print anything with this function. ###
        self.array.append(item)
        self.size += 1

        cur = self.size - 1
        while cur != 0:
            if self.array[(cur - 1) // 2] < self.array[cur]:
                self.array[(cur - 1) // 2], self.array[cur] = self.array[cur], self.array[(cur - 1) // 2]
                cur = (cur - 1) // 2

            else:
                break

    def peek(self):    #Find Maximum item
        if self.size == 0:
            return
        else:
            return self.array[0]
    def removeMax(self):   #Find Maximum item
    ### TODO ###
    ### You need not return or print anything with this function. ###
        self.array[0] = self.array[self.size - 1]
        del self.array[self.size - 1]
        self.size -= 1

        cur = 1
        while True:
            l = 2 * cur
            r = 2 * cur + 1

            if r <= self.size:
                if self.array[cur - 1] >= max(self.array[l - 1], self.array[r - 1]):
                    break

                left = self.array[l - 1]
                right = self.array[r - 1]

                if left > right:
                    self.array[cur - 1], self.array[l - 1] = self.array[l - 1], self.array[cur - 1]
                    cur = l

                else:
                    self.array[cur - 1], self.array[r - 1] = self.array[r - 1], self.array[cur - 1]
                    cur = r

            elif l <= self.size and self.array[cur - 1] < self.array[l - 1]:
                self.array[cur - 1], self.array[l - 1] = self.array[l - 1], self.array[cur - 1]
                cur = l

            else:
                break

    def showMaxHeap(self):   #Show MaxHeap with array
        return self.array

class FindMedian:
    def __init__(self):
    ### TODO ###
    ### Your own data structure. Implementing with heap structure is highly recommended. ###
        self.left = MaxHeap()
        self.right = MinHeap()
        self.size = 0

    def AddNewValues(self, NewValues):  # Add NewValues(a list of items) into your data structure
    ### TODO ###
    ### input: a list of values ###
    ### You need not return or print anything with this function. ###
        for value in NewValues:

            if self.size == 0:
                self.left.insert(value)

            else:
                mid = self.ShowMedian()
                if value < mid:
                    self.left.insert(value)
                    if self.left.getSize() - self.right.getSize() == 2:
                        self.right.insert(self.left.peek())
                        self.left.removeMax()

                else:
                    self.right.insert(value)
                    if self.right.getSize() - self.left.getSize() == 1:
                        self.left.insert(self.right.peek())
                        self.right.removeMin()

            self.size += 1

    def ShowMedian(self):  # Show Median of your data structure
    ### TODO ###
    ### You need not print anything but "return Median". ###
    ###The return value should always be a float number. ###
        if self.size == 0 or self.size % 2 == 1:
            return float(self.left.peek())
        else:
            return (self.left.peek() + self.right.peek()) / 2

    def RemoveMedian(self): # Remove median
    ### TODO ###
    ### You need not return or print anything with this function. ###
    ### If there are even number of elements, remove the larger one ###
    ### For example, if array=[1, 2, 3, 5], remove 3 ###
        if self.size % 2 == 1:
            self.left.removeMax()
        elif self.size != 0:
            self.right.removeMin()

        self.size -= 1