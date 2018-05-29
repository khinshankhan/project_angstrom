import os
import sys

servers_replace = {'\"database.db\"':'\"/var/www/angstrom/angstrom/database.db\"', 'app.debug = True':'app.debug = False'}
revert_replace = {'\"/var/www/angstrom/angstrom/database.db\"':'\"database.db\"', 'app.debug = False':'app.debug = True'}
wordReplacements = {'hi':'hello'}

def transform_line(line, choice):
    if (choice == "servers"):
            wordReplacements = servers_replace
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
    print '\'servers\' will convert files to work with a DO apache2 deployment server'
    print '\'revert\' will convert files back to normal, localhost use'
    print
    print 'Now choose either: servers or revert'
    sys.stdout.flush()
    choice = raw_input()
    if (choice == "servers" or choice == "revert"):
        replace_file("../angstrom/__init__.py", choice)
    else:
        print
        print 'Invalid choice'
    
run()
