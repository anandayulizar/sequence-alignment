from anytree import Node, RenderTree, AsciiStyle, PreOrderIter

class NW_Algorithm(object):
  def setSequence(self, seq1, seq2):
    self.seq1 = seq1
    self.seq2 = seq2
    self.matrix = [['x' for x in range(len(self.seq1) + 1)] for x in range(len(self.seq2) + 1)]
    self.traceBackMatrix = [[[] for x in range(len(self.seq1) + 1)] for x in range(len(self.seq2) + 1)]
    self.matrix[0][0] = 0
    self.solutions = []

  def setScoringSystem(self, match, mismatch, gap):
    # Set the score for the event of match, mismatch, and gap
    self.match = match
    self.mismatch = mismatch
    self.gap = gap
    curVal = 0
    for i in range(len(self.matrix[0])):
      self.matrix[0][i] = curVal
      self.traceBackMatrix[0][i] = [2]
      curVal += self.gap

    curVal = 0
    for j in range(len(self.matrix)):
      self.matrix[j][0] = curVal
      self.traceBackMatrix[j][0] = [1]
      curVal += self.gap

  def printTraceMatrix(self):
    print('|   |   | ', end='')
    for item in self.seq1:
      print('{} | '.format(item), end='')
    print('')
    for idx, item in enumerate(' ' + self.seq2):
      print('| {} | '.format(item), end='')
      for score in self.matrix[idx]:
        print('{} | '.format(score), end='')
      print('')

  def processSquare(self, x, y):
    # Set array in self.traceMatrix containing the previous lowest scores location for square x, y
    # 0 : diagonal
    # 1 : up
    # 2: left
    if (self.seq1[x - 1] == self.seq2[y - 1]):
      top_left = self.matrix[y - 1][x - 1] + self.match
    else:
      top_left = self.matrix[y - 1][x - 1] + self.mismatch

    top = self.matrix[y - 1][x] + self.gap
    left = self.matrix[y][x - 1] + self.gap


    arr = [top_left, top, left]
    maxIdx = maxFromArr(arr)
    self.matrix[y][x] = arr[maxIdx[0]]
    self.traceBackMatrix[y][x] = maxIdx

  def findSolutions(self):
    # Using Needleman-Wunsch Algorithm to find the best alignments
    iterX = 1
    iterY = 1

    # Set the tracebackMatrix by processing each squares previous best scores
    while (iterX < len(self.matrix) and iterY < len(self.matrix[0])):
      y = iterY
      while (y < len(self.matrix)):
        self.processSquare(iterX, y)
        y += 1

      x = iterX
      while (x < len(self.matrix[iterY])):
        self.processSquare(x, iterY)
        x += 1
      
      iterX += 1
      iterY += 1

    # Keep the paths in a tree structure
    root = Node((len(self.seq2), len(self.seq1)))
    self.tracePath(len(self.seq2), len(self.seq1), root)
    paths = [list(node.name for node in leaf.path)[::-1] for leaf in PreOrderIter(root, filter_=lambda node: node.is_leaf)]
    
    for path in paths:
      self.makeSolution(path)

  def tracePath(self, row, col, root):
    # A recursive function to make the coordinate path in a tree structure
    if (row != 0 or col != 0):
      idxList = self.traceBackMatrix[row][col]
      for idx in idxList:
        if (idx == 0):
          child = Node((row - 1, col - 1), parent=root)
          self.tracePath(row - 1, col - 1, child)
        elif (idx == 1):
          child = Node((row - 1, col), parent=root)
          self.tracePath(row - 1, col, child)
        else:
          child = Node((row, col - 1), parent=root)
          self.tracePath(row, col - 1, child)
  
  def makeSolution(self, path):
    # Translate the coordinate path to each sequence alignment
    # And add it to solutions array
    seq1Ret = ''
    seq2Ret = ''
    for idx, item in enumerate(path):
      if (idx != len(path) - 1):
        nextItem = path[idx + 1]
        colDiff = nextItem[1] - item[1]
        rowDiff = nextItem[0] - item[0]
        if (colDiff == 1 and rowDiff == 1):
          seq1Ret += self.seq1[nextItem[1] - 1]
          seq2Ret += self.seq2[nextItem[0] - 1]
        elif (colDiff == 1 and rowDiff == 0):
          seq1Ret += self.seq1[nextItem[1] - 1]
          seq2Ret += "-"
        elif (rowDiff == 1 and colDiff == 0):
          seq1Ret += "-"
          seq2Ret += self.seq2[nextItem[0] - 1]

    self.solutions.append([seq1Ret, seq2Ret])
      

def maxFromArr(arr):
  # Return the indexes of the maximu value in arr
  maxIdx = []
  for idx, num in enumerate(arr):
    max = True
    for num2 in arr:
      if (num < num2):
        max = False
        break
    if (max):
      maxIdx.append(idx)

  return maxIdx
        


if __name__ == "__main__":
  # Testing sequence

  # Sequence 1
  seq1 = 'GCATGCU'
  seq2 = 'GATTACA'
  # Solutions
  # GCATG-CU      GCA-TGCU      GCAT-GCU
  # G-ATTACA      G-ATTACA      G-ATTACA

  # Sequence 2
  # seq1 = 'CGTGAATTCAT'
  # seq2 = 'GACTTAC'


  NW = NW_Algorithm()
  NW.setSequence(seq1, seq2)
  NW.setScoringSystem(1, -1, -1)

  print('Before Processing\n')
  NW.printTraceMatrix()
  NW.findSolutions()

  print('\nAfter Processing\n')
  NW.printTraceMatrix()

  print('\nSolutions:\n')
  for idx, solution in enumerate(NW.solutions):
    print('Solution ', idx + 1)
    print('\tSequence 1: ', solution[0])
    print('\tSequence 2: ', solution[1])

  # print(testing(test, seq1, seq2))

  

  # print(NW.solutions)
  # print(NW.final)

  # print(NW.matrix[4][6])
  # print(NW.traceBack[4][6])