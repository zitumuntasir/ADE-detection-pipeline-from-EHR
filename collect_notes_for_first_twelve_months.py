# -*- coding: utf-8 -*-
import sys
import re
import shutil
import glob, os
from numpy import genfromtxt
import pandas as pd
from datetime import date,timedelta
import datetime
import calendar
import csv
total_selected_patient_ids = 0;
id_to_drug_date = {};
folder_created = {}
is_selected ={};
total_lines_note_summary = 0;
selected_patient_list = [None]*2000
map_current_note_id = {}
def read_patients():
    is_selected.clear();
    global total_selected_patient_ids;
    input_file = open("Enter the path of that file containing patient id","r")
    for line in input_file:
        id = line.rstrip('\n')
        is_selected[id] = 1;
    input_file.close();

def read_drug_date():
    id_to_drug_date.clear();
    drug_date_table = pd.read_csv("Enter the path of that file that has drug start date of patients")
    length = len(drug_date_table)
    for i in range(0, length):
        val = str(drug_date_table['mrn'][i])
        val1 = str(drug_date_table['ici_start'][i])
        lngth = len(str(drug_date_table['ici_start'][i]))
        if(lngth != 3):
            id_to_drug_date[val] = val1;
        else:
            id_to_drug_date[val] = "date_not_found"



def six_months_notes():
    cnt = 0
    count_total_dash = 0;
    folder_created.clear()
    output_location = "path of the output file"
    global id_to_drug_date
    global is_selected
    global map_current_note_id
    print("hello 1")
    summary_table = pd.read_csv("Enter the path of that file that has the clinical notes", engine='python')
    length = len(summary_table)

    for i in range(0,length):
        current_id = str(summary_table['PAT_MRN_ID'][i])
        current_date = str(summary_table['ici_start'][i])
        current_note = str(summary_table['NOTE_TEXT'][i])
        current_note_id = str(summary_table['NOTE_ID'][i])
        current_csn_txt_withinpt_coded = str(summary_table['csn_txt_withinpt_coded'][i])
        current_note_type = str(summary_table['IP_NOTE_TYPE_C_name'][i])
        current_date.replace('-','/')
        if((current_id in is_selected) and (len(current_date) > 3)):
            if(current_id in folder_created):
                s = 1 + 1
            else:
                folder_created[current_id] = 1;
                current_output_location = output_location
                current_output_location += current_id + "/"
                os.makedirs(current_output_location)
            if((current_date.find('-') != -1)):
                count_total_dash += 1;
            if(id_to_drug_date[current_id] != "date_not_found" and current_date.find('-') == -1 and id_to_drug_date[current_id].find('-') == -1):
                start_date = id_to_drug_date[current_id]
                start_date.replace('-','/')
                start_mm_dd_yy = start_date.split("/");
                current_mm_dd_yy = current_date.split("/");
                crr_mm = int(current_mm_dd_yy[0])
                crr_dd = int(current_mm_dd_yy[1])
                crr_yy = int(current_mm_dd_yy[2])
                if(crr_yy < 2000):
                    crr_yy += 2000
                str_mm = int(start_mm_dd_yy[0])
                str_dd = int(start_mm_dd_yy[1])
                str_yy = int(start_mm_dd_yy[2])
                if(str_yy < 2000):
                    str_yy += 2000
                start_time = date(str_yy, str_mm, str_dd)

                days_in_month = calendar.monthrange(start_time.year, start_time.month)[1]
                time_in_six_twelve = start_time + timedelta(days=365)

                date_started =  datetime.datetime(str_yy,str_mm,str_dd)
                date_now = datetime.datetime(crr_yy, crr_mm, crr_dd)
                date_in_twelve = datetime.datetime(time_in_six_twelve.year, time_in_six_twelve.month, time_in_six_twelve.day)
                if(date_now >= date_started and date_now <= date_in_twelve):
                    if(current_note_id in map_current_note_id):
                        saved_csn_id = map_current_note_id[current_note_id]
                        current_csn_id = int(current_csn_txt_withinpt_coded)
                        if(saved_csn_id == current_csn_id):
                            dest =current_output_location
                            source = " " + current_note
                            dest += "/" + str(summary_table["NOTE_ID"][i])
                            f = open(dest, "a", encoding="utf8", errors='ignore')
                            f.write(source)
                            f.close()
                    else:
                        map_current_note_id[current_note_id] = int(current_csn_txt_withinpt_coded)
                        dest = current_output_location
                        source = current_note
                        dest += "/" + str(summary_table["NOTE_ID"][i])
                        f = open(dest, "a", encoding="utf8", errors='ignore')
                        f.write(source)
                        f.close()
                    cnt += 1
    print("total notes ", cnt)
    print(count_total_dash)

def main():
    read_patients();
    read_drug_date();
    six_months_notes();
main()


