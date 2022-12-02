import sys

def main():
    n = len(sys.argv)
    if(n >= 4):
        s = int(sys.argv[1])
        bp = int(sys.argv[2])
        gh = int(sys.argv[3])
        lh = int(sys.argv[4])
        print("Bits a indexar: ", s)
        print("Tipo de predictor: ",sys.argv[2])
        print("Tamaño de registro de historia global: ",sys.argv[3])
        print("Tamaño de registro de historia local: ",sys.argv[4])
        globalRegister = 0
        predictor =  [[0 for i in range(2)]for j in range(2**s)]
        print(len(predictor))
        
    if(bp == 1):

        with open('saltos.trace','r') as f:
            branches = 0
            takenHit = 0
            takenMiss = 0
            notTakenHit = 0
            notTakenMiss = 0

            for line in f:

                subset = line.split()
                address = int(subset[0])
                jumptaken = subset[1]

                mask = (2**s)-1
                globalMask = (2**gh)-1

                #valor actual del registro global
                globalRegisterCurrentValue = globalRegister & globalMask

                #ultimos s bits de pc
                indexer =address & mask

                #Xor entre el valor del registro global y los ultimos s bits de PC
                globalIndexer = globalRegisterCurrentValue ^ indexer

                if predictor[globalIndexer] == [0,0] and jumptaken == 'T':
                    globalRegister << 1
                    globalRegister += 1

                    notTakenMiss += 1
                    predictor[globalIndexer] = [0,1]

                elif predictor[globalIndexer] == [0,0] and jumptaken == 'N':
                    globalRegister << 1

                    notTakenHit += 1
                    predictor[globalIndexer] = [0,0]

                elif predictor[globalIndexer] == [0,1] and jumptaken == 'T':
                    globalRegister << 1
                    globalRegister += 1

                    notTakenMiss += 1
                    predictor[globalIndexer] = [1,1]

                elif predictor[globalIndexer] == [0,1] and jumptaken == 'N':
                    globalRegister << 1

                    notTakenHit += 1
                    predictor[globalIndexer] = [0,0]

                elif predictor[globalIndexer] == [1,1] and jumptaken == 'T':
                    globalRegister << 1
                    globalRegister += 1

                    takenHit += 1
                    predictor[globalIndexer] = [1,1]

                elif predictor[globalIndexer] == [1,1] and jumptaken == 'N':
                    globalRegister << 1

                    takenMiss += 1
                    predictor[globalIndexer] = [1,0]

                elif predictor[globalIndexer] == [1,0] and jumptaken == 'T':
                    globalRegister << 1
                    globalRegister += 1

                    takenHit += 1
                    predictor[globalIndexer] = [1,1]

                elif predictor[globalIndexer] == [1,0] and jumptaken == 'N':
                    globalRegister << 1

                    takenMiss += 1
                    predictor[globalIndexer] = [0,0]

            branches = takenMiss + takenHit + notTakenHit + notTakenMiss
            print("Branches: ", branches)
            print("Predicted taken branches: ", takenHit)
            print("Not predicted taken branches: ", takenMiss)
            print("Predicted not taken branches: ", notTakenHit)
            print("Not predicted not taken branches: ", notTakenMiss)
            print("percentage: ", (takenHit + notTakenHit) * 100/(branches))

    elif(bp == 0):

        ##Predictor de saltos de 2-bits
        with open('saltos.trace','r') as f:
            branches = 0
            takenHit = 0
            takenMiss = 0
            notTakenHit = 0
            notTakenMiss = 0

            for line in f:

                subset = line.split()
                address = int(subset[0])
                jumptaken = subset[1]

                mask = (2**s)-1
                indexer = address & mask

                if predictor[indexer] == [0,0] and jumptaken == 'T':
                    notTakenMiss += 1
                    predictor[indexer] = [0,1]

                elif predictor[indexer] == [0,0] and jumptaken == 'N':
                    notTakenHit += 1
                    predictor[indexer] = [0,0]

                elif predictor[indexer] == [0,1] and jumptaken == 'T':
                    notTakenMiss += 1
                    predictor[indexer] = [1,1]

                elif predictor[indexer] == [0,1] and jumptaken == 'N':
                    notTakenHit += 1
                    predictor[indexer] = [0,0]

                elif predictor[indexer] == [1,1] and jumptaken == 'T':
                    takenHit += 1
                    predictor[indexer] = [1,1]

                elif predictor[indexer] == [1,1] and jumptaken == 'N':
                    takenMiss += 1
                    predictor[indexer] = [1,0]

                elif predictor[indexer] == [1,0] and jumptaken == 'T':
                    takenHit += 1
                    predictor[indexer] = [1,1]

                elif predictor[indexer] == [1,0] and jumptaken == 'N':
                    takenMiss += 1
                    predictor[indexer] = [0,0]

            branches = takenMiss + takenHit + notTakenHit + notTakenMiss
            print("Branches: ", branches)
            print("Predicted taken branches: ", takenHit)
            print("Not predicted taken branches: ", takenMiss)
            print("Predicted not taken branches: ", notTakenHit)
            print("Not predicted not taken branches: ", notTakenMiss)
            print("percentage: ", (takenHit + notTakenHit) * 100/(branches))
        
        

if __name__ == "__main__":
    main()