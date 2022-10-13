# -*- coding: utf-8 -*-
import sys
import re
import os.path

total_patients = 0; str_len = 0; cnt = 0;
current_output_location = ""; read_file =  ""; current_note = ""; write_file = ""; patient_list = [None]*1200;
current_location = ""; ch  = '';
output_note_location = "Enter the path of output location"
note_location = "path of the input note location"
import glob, os
def read_patients():
    global total_patients
    global patient_list
    global note_location
    input_file = open("Path of the file that has ids of the patients","r")
    for line in input_file:
        patient_list[total_patients] = line;
        total_patients += 1;
    input_file.close();

def read_notes():
    global write_file, read_file, total_patients, patient_list, note_location, ch, cnt, current_note, current_output_location, output_note_location;
    for i in range(0, total_patients):
        print(note_location)
        current_location = note_location;
        print(current_location)
        print(note_location)
        current_location += patient_list[i]
        current_location = current_location[:-1]    #eliminated_newline
        current_location += "/"
        if(os.path.exists(current_location) == True):
            current_output_location = output_note_location;
            current_output_location += patient_list[i]
            current_output_location = current_output_location[:-1]
            os.makedirs(current_output_location)
            current_output_location += "/"
            os.chdir(current_location)
            for file in glob.glob("*.txt"):
                read_file = current_location
                read_file += file
                write_file = current_output_location
                write_file += file
                output = open(write_file, "w")
                cnt = 0
                f = open(read_file, 'r')
                current_note = ""
                st = ""
                while True:
                    ch = f.read(1)
                    #print(ch)
                    if not ch:
                        break
                    if(st != "\n" or ch != "\n"):
                        current_note += ch
                        cnt += 1
                    st = ch
                current_note = re.sub("___", ":", current_note)
                current_note = re.sub("[*]+[*]+[*]+[*]+[*]+[*]+[*]+[*]+[*]", "(", current_note)
                current_note = re.sub("01913908352", ")", current_note)
                current_note = re.sub("31079085048009", ";", current_note)
                current_note = re.sub("123456789", "\"", current_note)
                current_note = re.sub(" dr ", "dr. ", current_note)
                current_note = re.sub(" vs ", "vs. ", current_note)
                current_note = re.sub(" ms ", "ms. ", current_note)
                current_note = re.sub(" pt ", "pt. ", current_note)
                current_note = re.sub(" mr ", "mr. ", current_note)
                current_note = re.sub(" jr ", "jr. ", current_note)
                output.write(current_note)
                print(i)

        else:
            print(patient_list[i])

def main():
    read_patients();
    read_notes();
main()
