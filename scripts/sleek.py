import os
import sys
import errno

def sremove(filename): #silentremove
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred
            
            
def transform_line(line):
    #print line
    num = 0
    line2 = line.split(' ')
    if (line2[0] == 'Merge:'):
        line = ''
        num = 5
    return (line, num)

def clean_log(fname):
    with open("temp_file.txt", "w") as output_file, open(fname) as input_file:
        name = "name"
        ticker = 0
        for line in input_file:
            check = line.split(' ')
            
            if (check[0] == 'commit' or ticker > 0):
                #print ('######################', ticker)
                if (ticker > 0):
                    ticker -= 1
                pass
            elif (check[0] == 'Author:'):
                if (check[1] == 'Khinshan' or check[1] == 'kkhan01'):
                    name = 'khinshanK'
                elif (check[1] == 'Stanley'):
                    name = 'stanleyL'
                elif (check[1] == 'Ryan'):
                    name = 'ryanS'
                else:
                    name = 'ishtiaqueM'
                name += ' -- '
            elif (check[0] == 'Date:'):
                temp = line[8:]
                name += temp
                output_file.write(name)
            else:
                newline = ''
                tick = 0
                (newline, tick) = transform_line(line)
                if(tick > 0):
                    ticker = tick
                else:
                    output_file.write(newline)
            
            
def run():
    command ='git log --reverse > hi.txt'
    os.system(command)
    clean_log("hi.txt")
    
run()

# git log --reverse > hi.txt
