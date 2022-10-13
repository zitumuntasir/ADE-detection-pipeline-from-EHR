import glob, os
import sys
import re
import os.path
cnntt = 0;
checking_duplicates = {};
count_negative_sentence = 0;
grade_check_external = 0;nivolumab_count = 0; sob_count = 0;
all_tag_types = {}; start_all_tag_types = {}; end_all_tag_types = {};
temp_causal_term = 0; causal_term_cross_check = 0; num_of_tot_R = 0;
entity_list = [None] * 10000000
all_sent_strt_R = [None] * 1000;
original_text_list = [None] * 10000000
date = 0;ADE = 0;drug = 0;grade = 0;causal_term = 0;ade_date = 0;drug_date = 0;GRADE = 0;sngl_pos_rltd = 0;mult_pos_rltd = 0;sngl_neg_rltd = 0;mult_neg_rltd = 0;sngl_rltd = 0;mult_rltd = 0;
total_folders = 0; str_len = 0; cnt = 0; total_sentences = 0;
rltn_start_index = [None] * 100000;rltn_end_index = [None] * 100000;folder_list = [None]*50;all_notes = [None]*100;all_notes_ann_ext = [None]*100;
all_notes_txt_ext = [None]*100; tagged_item = [None]*1000; original_tagged_text = [None] * 1000;
start_ind = [None] * 1000;end_ind = [None] * 1000;tag_number = [None] * 1000;saved_sent_tag_num = [None] * 1000;lst = [None]*4;
toal_positive = 0;current_note_original = "";tot_num_of_mult_sent = 0;tot_num_of_singl_sent = 0;total_drug_date_rel = 0;total_ade_date_rel = 0;inside_tags = 0;
input_location = "enter path of input note location";
output_location = "enter path of output note location";
note_date_dict = {};duplicate_flag = {};total_relation_types = {}; strength_of_relation = {};  total_dates_different_notes = 0;
entities_inside = {}; drug_frequency = {}; ade_frequency = {}; causal_term_frequency = {};
def map_note_date():
    global note_date_dict, total_dates_different_notes;
    date_input_file = open("notes_summary", "r");
    for line in date_input_file:
        total_dates_different_notes += 1
        separate = line.split()
        if(separate[2] in note_date_dict):
            do_nothing = 1 + 1;
        else:
            note_date_dict[separate[2]] = separate[1];
    date_input_file.close();

def validation_folders_list():
    global total_folders, folder_list;
    input_file = open("enter path of patient specific notes","r");
    for line in input_file:
        folder_list[total_folders] = line;
        total_folders += 1;
    input_file.close();

def read_notes():
    output = open("output file of all single sentence relation", "w");
    output1 = open("output file of all single sentence relation with precision", "w");
    output_without_duplicate = open("output file of all single sentence relation without duplication","w");
    global cnntt, start_all_tag_types, end_all_tag_types, grade_check_external, nivolumab_count, sob_count, count_negative_sentence;
    global causal_term_frequency, temp_causal_term, causal_term_cross_check, all_sent_strt_R, num_of_tot_R, all_tag_types;
    global date, ADE, drug, grade, causal_term, ade_date, drug_date;
    global GRADE,sngl_pos_rltd,mult_pos_rltd,sngl_neg_rltd,mult_neg_rltd,sngl_rltd,mult_rltd;
    global inside_tags, total_sentences, total_relation_types, tot_num_of_mult_sent, tot_num_of_singl_sent, total_drug_date_rel, original_tagged_text, tagged_item;
    global total_ade_date_rel, note_date_dict, current_note_original, write_file, read_file, total_folders, folder_list, strength_of_relation;
    global input_location, ch, cnt, current_note, current_output_location, output_note_location, toal_positive;
    entities_inside["date"] = 0;entities_inside["ADE"] = 0;entities_inside["drug"] = 0;entities_inside["grade"] = 0;entities_inside["causal_term"] = 0;
    entities_inside["new_ADE"] = 0;entities_inside["new_drug"] = 0;entities_inside["new_date"] = 0;entities_inside["negative_sentence"] = 0;
    entities_inside["mis_ADE"] = 0;
    entities_inside["mis_drug"] = 0;
    entities_inside["mis_date"] = 0;
    entities_inside["Replication"] = 0;
    entities_inside["negative_ADE"] = 0;
    entities_inside["Drug"] = 0;
    entities_inside["PHI"] = 0;
    entities_inside["actual_number_required"] = 0;
    entities_inside["history"] = 0;
    checking_duplicates.clear();
    for i in range(0, total_folders):
        tot_num = 0; all_notes_ann_ext = [None] * 100; all_notes_txt_ext = [None] * 100; all_notes = [None] * 100;
        current_location = input_location; current_location += folder_list[i]; current_location = current_location[:-1]    #eliminated_newline
        current_location += "/"
        print(current_location)
        if(os.path.exists(current_location) == True):
            print(current_location)
            current_output_location = output_location;
            current_output_location += folder_list[i]
            current_output_location = current_output_location[:-1]
            current_output_location += "/"
            os.chdir(current_location)
            print(os.chdir(current_location))
            note_count_in_folder = 0;
            #saving note numbers
            for file in glob.glob("*.ann"):
                all_notes[note_count_in_folder] = file.split('.')[0]
                all_notes_ann_ext[note_count_in_folder] = all_notes[note_count_in_folder] + ".ann";
                all_notes_txt_ext[note_count_in_folder] = all_notes[note_count_in_folder] + ".txt";
                print(all_notes_txt_ext[note_count_in_folder])
                note_count_in_folder += 1;
            #working on single note in a folder start index, end index of every tag
            for i in range(0, note_count_in_folder):
                #print(num_of_tot_R)
                #clearing variables
                strength_of_relation.clear();
                start_all_tag_types.clear();
                end_all_tag_types.clear();
                all_tag_types.clear();
                num_of_tot_R = 0;
                rltn_start_index = [None] * 500000; rltn_end_index = [None] * 500000;
                start_ind = [None] * 1000; end_ind = [None] * 1000; tag_number = [None] * 1000; saved_sent_tag_num = [None] * 1000;
                tagged_item = [None] * 1000; original_tagged_text = [None] * 1000; lst = [None] * 4;
                current_line = ""; total_tags = 0;current_note = "";
                #duplicate_flag.clear();
                rs = 0;
                read_file = current_location; read_file += all_notes_ann_ext[i];
                f = open(read_file, 'r')
                while True:
                    ch = f.read(1)
                    if not ch:
                        break
                    current_line += ch
                    current_note += ch #for frequency count
                    if(ch == '\n'):
                        word = current_line.split();
                        if(word[0][0] == 'R'):
                            all_sent_strt_R[num_of_tot_R] = current_line[:-1];
                            num_of_tot_R += 1;
                        if(word[0][0] == 'T'):
                            entity_list[total_tags] = word[1];
                            original_text_list[total_tags] = word[4];
                            all_tag_types[word[0]] = word[1];
                            start_all_tag_types[word[0]] = str(word[2])
                            end_all_tag_types[word[0]] = str(word[3])
                            original_tagged_text[int(word[0].split("T")[1])] = word[4];
                            if(len(word) > 5):
                                original_text_list[total_tags] += " " + word[5];
                                original_tagged_text[int(word[0].split("T")[1])] += " " + word[5];
                            if(len(word) > 6):
                                original_tagged_text[int(word[0].split("T")[1])] += " " + word[6];
                                original_text_list[total_tags] += " " + word[6];
                            if(len(word) > 7):
                                original_tagged_text[int(word[0].split("T")[1])] += " " + word[7];
                                original_text_list[total_tags] += " " + word[7];
                            if(len(word) > 8):
                                original_tagged_text[int(word[0].split("T")[1])] += " " + word[8];
                                original_text_list[total_tags] += " " + word[8];
                            if(len(word) > 9):
                                original_tagged_text[int(word[0].split("T")[1])] += " " + word[9];
                                original_text_list[total_tags] += " " + word[9];
                            tag_number[total_tags] = int(word[0].split("T")[1]);
                            start_ind[total_tags] = int(word[2]);
                            end_ind[total_tags] = int(word[3]);
                            tagged_item[int(word[0].split("T")[1])] = word[1];
                            total_tags = total_tags + 1;
                        current_line = "";
                current_line = ""; current_note_original = "";
                read_file = current_location;read_file += all_notes_txt_ext[i];
                f = open(read_file, 'r')
                sent_start = 0; cnt = 0; sent_end = 0;space = 0;
                while True:
                    ch = f.read(1)
                    if not ch:
                        break
                    current_line += ch
                    current_note_original += ch
                    yes_positive = 0;
                    if (ch == '\n'):
                        space += 1
                        current_note_original += " "
                        sent_end = cnt
                        for j in range(0, total_tags):
                            if(start_ind[j] >= sent_start and start_ind[j] <= sent_end + 1 and end_ind[j] >=sent_start  and end_ind[j] <= sent_end + 1):
                                tag = tag_number[j]
                                saved_sent_tag_num[tag] = current_line
                                yes_positive = 1;
                                rltn_start_index[tag] = sent_start
                                rltn_end_index[tag] = sent_end
                        if(yes_positive == 1):
                            toal_positive += 1
                        sent_start = sent_end + 2
                                #output.write(current_line)
                        current_line = "";
                        cnt += 1
                    cnt += 1
                current_line = ""
                read_file = current_location;
                read_file += all_notes_ann_ext[i]
                f = open(read_file, 'r')
                while True:
                    ch = f.read(1)
                    if not ch:
                        break
                    current_line += ch
                    if (ch == '\n'):
                        word = current_line.split()
                        if (current_line[0] == '#' and (word[3][0] == "p" or word[3][0] == "P" or word[3][0] == "N" or word[3][0] == "n") and word[2][0] == "R"):
                            strength_of_relation[word[2]] = word[3];
                            #print(current_line)
                        current_line = ""
                current_line  = ""


                #print Specific type of lines
                current_line = ""
                read_file = current_location;
                read_file += all_notes_ann_ext[i]
                f = open(read_file, 'r')
                while True:
                    ch = f.read(1)
                    if not ch:
                        break
                    current_line += ch
                    if(ch == '\n'):
                        rs = 0;
                        output_string = ""
                        word = current_line.split()
                        if(word[0][0] == 'R'):
                            relation_type = word[1]
#                            output_string += relation_type + "	"
#                            print(relation_type)
                            index1 = int(word[2].split("T")[1])
                            index2 = int(word[3].split("T")[1])
                            lst[0] = rltn_start_index[index1];
                            lst[1] = rltn_end_index[index1];
                            lst[2] = rltn_start_index[index2];
                            lst[3] = rltn_end_index[index2];
                            lst.sort();
                            current_note_original[lst[0]:lst[3]]
                            found_causal_term = 0;
                            original_causal_term = ""
                            if (word[1] == "Drug-ADE"):
                                causal_term_start_index = "0";
                                causal_term_end_index = "0";
                                cur_tag1 = word[2].split(":")[1];
                                cur_tag2 = word[3].split(":")[1];
                                other_tag = "";
                                for l in range(0,num_of_tot_R):
                                    other_tag1 = ""
                                    other_tag2 = ""
                                    other_tag = "";
                                    current_sent = all_sent_strt_R[l].split();
                                    if(current_sent[1] == "sngl_rltd"):
                                        if(cur_tag1 == current_sent[2].split(":")[1] or cur_tag1 == current_sent[3].split(":")[1]):
                                            if(cur_tag1 == current_sent[2].split(":")[1]):
                                                other_tag = current_sent[3].split(":")[1];
                                            else:
                                                other_tag = current_sent[2].split(":")[1];
                                            found_causal_term = 1;
                                        elif(cur_tag2 == current_sent[2].split(":")[1] or cur_tag2 == current_sent[3].split(":")[1]):
                                            if (cur_tag2 == current_sent[2].split(":")[1]):
                                                other_tag = current_sent[3].split(":")[1];
                                            else:
                                                other_tag = current_sent[2].split(":")[1];
                                            found_causal_term = 1;
                                    if(found_causal_term == 1):
                                        causal_term_start_index = start_all_tag_types[other_tag];
                                        causal_term_end_index = end_all_tag_types[other_tag];
                                        original_causal_term = original_tagged_text[int(other_tag.split("T")[1])]
                                        break;
                                for k in range(0,total_tags):
                                    if (start_ind[k] >= lst[0] and start_ind[k] <= lst[3] and end_ind[k] >= lst[0] and end_ind[k] <= lst[3]):
                                        if(entity_list[k] == "drug" or entity_list[k] == "ADE"):
                                            if (entity_list[k] == "drug"):
                                                if(original_text_list[k] == "nivolumab"):
                                                    cnntt += 1;
                                                if(original_text_list[k] in drug_frequency):
                                                    drug_frequency[original_text_list[k]] += 1;
                                                else:
                                                    drug_frequency[original_text_list[k]] = 1;
                                            else:
                                                if (original_text_list[k] in ade_frequency):
                                                    ade_frequency[original_text_list[k]] += 1;
                                                else:
                                                    ade_frequency[original_text_list[k]] = 1;
                                        if (entity_list[k] == "causal_term"):
                                            causal_term_cross_check += 1;
                                            if (original_text_list[k] in causal_term_frequency):
                                                causal_term_frequency[original_text_list[k]] += 1;
                                            else:
                                                causal_term_frequency[original_text_list[k]] = 1;
                                        entities_inside[entity_list[k]] += 1;
                                        inside_tags += 1;
                                total_sentences += 1;
                                sent_track =  ""
                                output_string = ""
                                output_string += all_notes[i] + "|||";
                                output_string += relation_type + "|||"
                                #output_string += tagged_item[index1] + " "
                                first_tag = word[2].split(":")[1];
                                second_tag = word[3].split(":")[1];
                                if(all_tag_types[first_tag] == "drug"):
                                    output_string += str(start_all_tag_types[first_tag]) + "|||"
                                    output_string += str(end_all_tag_types[first_tag]) + "|||"
                                elif(all_tag_types[second_tag] == "drug"):
                                    output_string += str(start_all_tag_types[second_tag]) + "|||"
                                    output_string += str(end_all_tag_types[second_tag]) + "|||"
                                output_string += original_tagged_text[index1] + "|||" #drug
#                                output_string += tagged_item[index2] + " "
                                if (all_tag_types[first_tag] == "ADE"):
                                    output_string += str(start_all_tag_types[first_tag]) + "|||"
                                    output_string += str(end_all_tag_types[first_tag]) + "|||"
                                elif (all_tag_types[second_tag] == "ADE"):
                                    output_string += str(start_all_tag_types[second_tag]) + "|||"
                                    output_string += str(end_all_tag_types[second_tag]) + "|||"
                                output_string += original_tagged_text[index2] + "|||" #ade
                                output_string += causal_term_start_index + "|||"
                                output_string += causal_term_end_index + "|||"
                                if(found_causal_term == 1):
                                    output_string += original_causal_term + "|||" #causal term
                                else:
                                    output_string += "no_causal_term" + "|||";
                                strength = ""
                                if word[0] in strength_of_relation:
                                    strength = strength_of_relation[word[0]];
                                else:
                                    strength = "Strength_Not_Found";
                                if(strength[0] == "N"):
                                    ttt = 1 + 1;
                                    #print("negative strength found ", strength)
                                output_string += strength + "|||"
                                output_string += str(lst[0]) + "|||" + str(lst[3]) + "|||"
                                output_string += current_note_original[lst[0]:lst[3]] + "\n"
                                new_temp_output_string = current_note_original[lst[0]:lst[3]] + "\n"
                                current_note_length = len(current_note_original)
                                next_line_count = 0;
                                output.write(output_string)
                                output1.write(new_temp_output_string)
                                if(new_temp_output_string in  checking_duplicates):
                                    do_nothing = 1;
                                else:
                                    output_without_duplicate.write(new_temp_output_string)
                                    checking_duplicates[new_temp_output_string] = 1
                                if current_note_original[lst[0]:lst[3]] in duplicate_flag:
                                    rs = 1
                                else:
                                    tot_num += 1
                                    if relation_type in total_relation_types:
                                        total_relation_types[relation_type] += 1
                                    else:
                                        total_relation_types[relation_type] = 1
                                    duplicate_flag[current_note_original[lst[0]:lst[3]]] = 1
                        current_line = "";
                #print_all_counts
                current_note = ""
                read_file = current_location;
                read_file += all_notes_ann_ext[i]
                f = open(read_file, 'r')
                test_new_line = ""
                #print(all_notes_ann_ext[i])
                while True:
                    ch = f.read(1)
                    if not ch:
                        break
                    if(ch == "\n"):
                        test_new_line = "";
                    current_note += ch
                    test_new_line += ch
                #print(current_note)
                date += current_note.count("	date ");
                ADE += current_note.count("	ADE ");
                drug += current_note.count("	drug ");
                grade += current_note.count("	grade ");
#                grade += current_note.count("	grade ");
                causal_term += current_note.count("causal_term");
                ade_date += current_note.count("	ade_date ");
                drug_date += current_note.count("	drug_date ");
                GRADE += current_note.count("	GRADE ");
                sngl_pos_rltd += current_note.count("	sngl_pos_rltd ");
                mult_pos_rltd += current_note.count("	mult_pos_rltd ");
                sngl_neg_rltd += current_note.count("	sngl_neg_rltd ");
                mult_neg_rltd += current_note.count("	mult_neg_rltd ");
                sngl_rltd += current_note.count("	sngl_rltd ");
                mult_rltd += current_note.count("	mult_rltd ");
#                count_negative_sentence += current_note("	negative_sentence ")
        print(tot_num)
    for a in drug_frequency:
        print(a, "\t", drug_frequency[a]);

    print("total_relation_types ", total_relation_types);
    print("total date ", date);
    print("total ADE ",ADE)
    print("total drug ", drug)
    print("total grade ",grade)
    print("total causal_term ", causal_term)
    print("total drug_date", drug_date)
    print("total ade_date ", ade_date)
    print("total relation grade ", GRADE)
    print("total relation single sentence positive ", sngl_pos_rltd)
    print("total relation multiple sentence positive ", mult_pos_rltd)
    print("total relation single sentence negative ", sngl_neg_rltd)
    print("total relation multiple sentence negative ", mult_neg_rltd)
    print("total single sentence relation causal term to drug/ade", sngl_rltd)
    print("total multiple sentence relation causal term to drug/ade", mult_rltd)
    #print("negative_sentence_tag", count_negative_sentence)
    print("total Inside Tags  ", inside_tags)
    print(entities_inside)
    print("external grade check,", grade_check_external);
    print(drug_frequency.keys())
    print(drug_frequency.values())
    print(ade_frequency.keys())
    print(ade_frequency.values())
    print("nivolumab_count ", nivolumab_count);
    print("sob_count ", cnntt);
    print(causal_term_frequency)

def main():
    validation_folders_list(); #Read input folders
    read_notes();
main()
