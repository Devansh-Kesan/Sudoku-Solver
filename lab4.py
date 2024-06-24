import pycosat
import itertools
from operator import itemgetter
import time

#opening the output file for appending output into it:
output_file = open('output.txt', 'w')

# Opening the file and reading data from it
with open('p.txt', 'r') as file:
    start = time.time()
    print("!! Running !!")
    for line in file:
        s = line.strip()
        n = len(s)
        sq_n = int(n**(0.5))
        sq_sq_n = int(sq_n**(0.5))


        d = dict()
        for i in range(0,sq_n):
            for j in range(0,sq_n):
                for num in range(1,sq_n+1):
                    if i==0 and j==0 and num==sq_n:
                        d[i,j,num] = sq_n*sq_n*sq_n
                    else:
                        num1 = num
                        if num==sq_n:
                            num1 = 0
                        d[i,j,num] = sq_n*(sq_n*j + i) + num1

        sort_dict = dict(sorted(d.items(),key=itemgetter(1)))

        
        filled_list = []
        for i in range(0,n):
            if (s[i]!="."):
                row_ind = i//sq_n
                col_ind = i%sq_n
                num = int(s[i])
                filled_list.append([sort_dict[row_ind,col_ind,num]])

        # every cell should have atleast one value
        for i in range(sq_n):
            for j in range(sq_n):
                curr_list = []
                for num in range(1,sq_n+1):
                    curr_list.append(d[i,j,num])
                filled_list.append(curr_list)

        # every cell should have atmost one value
        for i in range(sq_n):
            for j in range(sq_n):
                for num in range(1,sq_n+1):
                    for n1 in range(num+1,sq_n+1):
                        filled_list.append([-d[i,j,num],-d[i,j,n1]])

        # row Constraint                      
        for i in range(sq_n):
            for num in range(1,sq_n+1):
                curr_list = []
                for j in range(sq_n):
                    curr_list.append(d[i,j,num])
                filled_list.append(curr_list)

        # column Constraint
        for j in range(sq_n):
            for num in range(1,sq_n+1):
                curr_list = []
                for i in range(sq_n):
                    curr_list.append(d[i,j,num])
                filled_list.append(curr_list)

        # Box Constraint
        for i1 in range(0,sq_n,sq_sq_n):
            for j1 in range(0,sq_n,sq_sq_n):        
                for num in range(1,sq_n+1):
                        curr_list = []
                        for i in range(i1,i1+sq_sq_n):
                            for j in range(j1,j1+sq_sq_n):
                                curr_list.append(d[i,j,num])
                        filled_list.append(curr_list)


        # Outputing the result
        output = pycosat.solve(filled_list)
        if output=="UNSAT":
            # print("The given sudoku is not solvable")
            output_file.write("The given sudoku is not solvable")
            output_file.write("\n")
        else:
            filled = 0
            final_list = []
            d_final = dict()

            for i in output:
                if i>0:
                    d_final[i] = 1
                else:
                    d_final[-i] = 0

            cordinate_list = []
            for x in sort_dict:
                if d_final[sort_dict[x]] == 1:
                    final_list.append(x)

            s_output = ""
            final_list.sort()
            for i in range(n):
                s_output += str(final_list[i][2])

            output_file.write(s_output)
            output_file.write("\n")
            # print(s_output)

end = time.time()
print("!! Finished !!")

print("Time Taken : ",end-start)






