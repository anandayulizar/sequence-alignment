class NW_Algorithm(object):
  def setSequence(self, seq1, seq2):
    self.seq1 = seq1
    self.seq2 = seq2
    self.matrix = [['x' for x in range(len(self.seq1) + 1)] for x in range(len(self.seq2) + 1)]
    self.traceBackMatrix = [[[] for x in range(len(self.seq1) + 1)] for x in range(len(self.seq2) + 1)]
    self.matrix[0][0] = 0
    self.solutions = []
    self.final = []

  def setScoringSystem(self, match, mismatch, gap):
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

  def printMatrix(self):
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

  def startAlgorithm(self):
    iterX = 1
    iterY = 1
    while (iterX < len(self.matrix) and iterY < len(self.matrix[0])):
      y = iterY
      while (y < len(self.matrix)):
        # print('({}, {})'.format(self.seq1[iterX], self.seq2[y]))
        self.processSquare(iterX, y)
        y += 1

      x = iterX
      while (x < len(self.matrix[iterY])):
        # print('({}, {})'.format(self.seq1[x], self.seq2[iterY]))
        self.processSquare(x, iterY)
        x += 1
      
      iterX += 1
      iterY += 1

    self.recursive(len(self.seq2), len(self.seq1), self.solutions)
    # self.solutions = [1,2,3,4,5,6]
    self.reconstruct(self.solutions, [])

  def recursive(self, row, col, arr):
    if (row == 0 and col == 0):
      arr.append(self.matrix[0][0])
    else:
      idxList = self.traceBackMatrix[row][col]
      if len(idxList) > 1:
        for idx in idxList:
          temp = []
          
          if (idx == 0):
            temp.append(self.matrix[row - 1][col - 1])
            self.recursive(row - 1, col - 1, temp)
          elif (idx == 1):
            temp.append(self.matrix[row - 1][col])
            self.recursive(row - 1, col, temp)
          else:
            temp.append(self.matrix[row][col - 1])
            self.recursive(row, col - 1, temp)
          arr.append(temp)
      
      else:
          if (idxList[0] == 0):
            arr.append(self.matrix[row - 1][col - 1])
            self.recursive(row - 1, col - 1, arr)
          elif (idxList[0] == 1):
            arr.append(self.matrix[row - 1][col])
            self.recursive(row - 1, col, arr)
          else:
            arr.append(self.matrix[row][col - 1])
            self.recursive(row, col - 1, arr)

  def reconstruct(self, arr, retArr):
    listPresent = False
    initial = len(retArr)
    for item in arr:
      if isinstance(item, list):
        listPresent = True
        newArr = list(retArr)
        self.reconstruct(item, newArr)
        self.final.append(newArr)
      else:
        retArr.append(item)
    
    if (initial == 0 and not listPresent):
      self.final = list(retArr)
      

def maxFromArr(arr):
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
  # GCATGCU      GCATG-CU      GCA-TGCU      GCAT-GCU
  # GATTACA      G-ATTACA      G-ATTACA      G-ATTACA

  seq1 = 'GCATGCU'
  seq2 = 'GATTACA'

  # seq1 = 'CGTGAATTCAT'
  # seq2 = 'GACTTAC'
  NW = NW_Algorithm()
  NW.setSequence(seq1, seq2)
  NW.setScoringSystem(1, -1, -1)
  NW.printMatrix()
  NW.startAlgorithm()

  print('\nAfter Processing\n')
  NW.printMatrix()

  print(NW.solutions)
  print(NW.final)

  # print(NW.matrix[4][6])
  # print(NW.traceBack[4][6])