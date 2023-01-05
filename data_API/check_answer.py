f = open('answers.txt','r')
while True:
    line = f.readline()
    if not line:
        break
    parsed_line = line.split(" ")
    col_name = parsed_line[0].split(":")[1]
    answer = parsed_line[2].split(":")[1]
    print(col_name, answer)
    
f.close()