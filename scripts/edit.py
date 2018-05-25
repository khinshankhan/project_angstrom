import os
import sys

windows_replace = {'\"database.db\"':'\"/var/www/angstrom/angstrom/database.db\"'}
revert_replace = {'\"/var/www/angstrom/angstrom/database.db\"':'\"database.db\"'}
wordReplacements = {'hi':'hello'}

def transform_line(line, choice):
    if (choice == "windows"):
            wordReplacements = windows_replace
    elif (choice == "revert"):
        wordReplacements = revert_replace
    
    for key, value in wordReplacements.iteritems():
        line = line.replace(key, value)
    wordReplacements = {'hi':'hello'}
    return line

def replace_file(fname, choice):
    with open("temp_file", "w") as output_file, open(fname) as input_file:
        for line in input_file:
            output_file.write(transform_line(line, choice))
    os.remove(fname)
    os.rename("temp_file", fname)

def run():
    sys.stdout.flush()
    print '\'windows\' will convert files to work with a DO apache2 deployment server'
    print '\'revert\' will convert files back to normal, localhost use'
    print
    print 'Now choose either: windows or revert'
    sys.stdout.flush()
    choice = raw_input()
    if (choice == "windows" or choice == "revert"):
        replace_file("../angstrom/__init__.py", choice)
    else:
        print
        print 'Invalid choice'
    
run()
