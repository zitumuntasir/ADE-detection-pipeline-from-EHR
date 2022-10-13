#include <bits/stdc++.h>
#include<fstream>
#include<dirent.h>
using namespace std;
FILE *write_missing_patients;
FILE *write_output, *rd, *wr, *wr1, *rd1, *read_date, *read_drug_name, *read_patient_list, *read_note;
const int NN = 10000005;
int caseno, cases;
int m, n, pi[NN], res = 0;
map<string, long>indv_cnt;
char note_in_original_case[1000000];
long catg_map[5000000][12], missing_folders[1000], negative_patients[1000], total_negatives = 0;
long term_frequency[1000], catg[100], note_number = 0;
char a[NN], b[NN], output_file[1000], output_directory[1000], original_current_dir[1000];
char all_drugs[1000][100], temp_line[1000000], temp_word[1000], all_patients[1000][100], all_dates[1000][100];
char ch, st;
long total_missing, total_folders, negative = 0, lines = 0, len = 0, ii = 0, wlen = 0, words = 0,total_patients = 0, total_drugs = 0, total_dates = 0, dirlen = 0;
char all_files[1000], current_dir[1000], not_empty = 0;
long notes_in_total = 0, flag, strt_indx = 0, out_dir_len = 0, out_file_len = 0, file_opened = 0, total_notes = 0, resn = 0;


int kmpMatcher() {
    int cnt = 0;
    for( int i = 1, k = 0; i <= n; i++ ) {
        while( k > 0 && b[k+1] != a[i] ) k = pi[k];
        if( b[k+1] == a[i] ) k++;
        if( k == m ) {
            cnt++;
            k = pi[k];
        }
    }
    return cnt;
}

void computePrefix() {
    pi[1] = 0;
    for( int i = 2, k = 0; i <= m; i++ ) {
        while( k > 0 && b[k+1] != b[i] ) k = pi[k];
        if( b[k+1] == b[i] ) k++;
        pi[i] = k;
    }
}
void prn()
{
    for(int iiii = 0; iiii < len; iiii++)
    {
        fprintf(write_output,"%c",note_in_original_case[iiii]);
    }
    fprintf(write_output,"\n");
}

void file_operation(int current_id)
{
DIR *dir;
struct dirent *ent;
strcpy(current_dir,"Enter the path of the notes");
dirlen = strlen(current_dir);
strcpy(output_directory, "Enter path of the output directory");
out_dir_len = strlen(output_directory);

/*CREATING DIRECTORIES, DESTINATION UPTO FOLDER*/
for(int pid = 0; pid < 171; pid++)
{
    current_dir[dirlen + pid] = all_patients[current_id][pid];
    output_directory[out_dir_len + pid] = all_patients[current_id][pid];
}
current_dir[dirlen + 9] = '\0';
strcpy(original_current_dir, current_dir);
output_directory[out_dir_len + 9] = '/';
output_directory[out_dir_len + 10] = '\0';

/*CHECK IF THE FOLDER EXISTS*/
if ((dir = opendir (current_dir)) != NULL) {
  while ((ent = readdir (dir)) != NULL) {
    strcpy(all_files,ent->d_name);
    strt_indx = all_files[0] - 48;
    file_opened = 0;
    strcpy(current_dir,original_current_dir);
    /*CHECK IF A FILE STARTS WITH A NUMBER TO AVOD DOT*/
    if(strt_indx > 0 && strt_indx <= 9)
    {
        notes_in_total++;
        strcpy(output_file, output_directory);
        out_file_len = strlen(output_file);
        dirlen = strlen(current_dir);
        current_dir[dirlen] = '\\';
        current_dir[dirlen + 1] = '\0';
        dirlen = strlen(current_dir);
        int filelen = strlen(all_files);
        /* current_dir FOR OPENNING THE READ FILE, output_file TO CREATE AN OUTPUT*/
        for(int iii = 0; iii < filelen; iii++)
        {
            current_dir[dirlen + iii] = all_files[iii];
            output_file[out_file_len + iii] = all_files[iii];
        }
        current_dir[dirlen + filelen] = '\0';
        output_file[out_file_len + filelen] = '\0';
        out_file_len = strlen(output_file);
        output_file[out_file_len] = '.';
        output_file[out_file_len + 1] = 't';
        output_file[out_file_len + 2] = 'x';
        output_file[out_file_len + 3] = 't';
        output_file[out_file_len + 4] = '\0';


        read_note = fopen(current_dir, "r");
        len = 0;
        while((ch = getc(read_note)) != EOF)
     {
        if(isprint(ch)) {note_in_original_case[len] = ch; temp_line[len] = tolower(ch); len++;}
     }

             if(ch == EOF)
        {
            note_number++;
            int res1 = 0, res2 = 0;
            resn = 0;
            res = 0;
            flag = 0;
            lines++;
            temp_line[len] = '\0';
            note_in_original_case[len] = '\0';
            strcpy(a + 1,temp_line);
            n = strlen(a + 1);
            for(int dd = 0; dd < total_drugs; dd++)
            {
                strcpy(b + 1,all_drugs[dd]);
                m = strlen(b + 1);
                computePrefix();
                res = kmpMatcher();
                if(res > 0) break;
            }


                if(res > 0)
                {
                    for(int ee = 0; ee < total_dates; ee++)
                    {
                        strcpy(b + 1,all_dates[ee]);
                        m = strlen(b + 1);
                        computePrefix();
                        resn = kmpMatcher();
                        if(resn > 0)
                        {
                        flag = 1;
                        if(not_empty == 0)
                        {
                            total_folders++;
                            mkdir(output_directory); not_empty = 1;
                        }
                        term_frequency[ee]++;
                        }
                    }
                }
            if(res > 0 && flag > 0){
                    file_opened = 1;
                    total_notes++;
                    write_output = fopen(output_file, "w");
                    cout << total_notes << "  " << negative << "  " << notes_in_total << "  " << total_folders << endl;
                    prn(); res = 0, resn = 0, flag = 0;
            }
            else
            {
                negative++;
            }
            len = 0;
        }

        fclose(read_note);
    }
    if(file_opened == 1)
        {
            fclose(write_output);
        }
    file_opened = 0;
    memset(all_files,NULL,sizeof(all_files));
  }
  closedir (dir);
}
 else {
  missing_folders[total_missing] = current_id;
  total_missing++;
}
}


void drug_list()
{
    wlen = 0;
    while((st = getc(read_drug_name)) != EOF)
    {
        temp_word[wlen] = tolower(st);
        wlen++;
        if(st == '\n')
        {
            temp_word[wlen - 1] = '\0';
            strcpy(all_drugs[total_drugs], temp_word);
            total_drugs++;
            wlen = 0;
        }
    }
    fclose(read_drug_name);
}

void ADE_list()
{
    wlen = 0;
    while((st = getc(read_ADE)) != EOF)
    {
        temp_word[wlen] = tolower(st);
        wlen++;
        if(st == '\n')
        {
            temp_word[wlen - 1] = '\0';
            strcpy(all_dates[total_dates], temp_word);
            total_dates++;
            wlen = 0;
        }
    }
    fclose(read_ADE);
}


void patient_list()
{
    wlen = 0;
    while((st = getc(read_patient_list)) != EOF)
    {
        temp_word[wlen] = tolower(st);
        wlen++;
        if(st == '\n')
        {
            temp_word[wlen - 1] = '\0';
            strcpy(all_patients[total_patients], temp_word);
            total_patients++;
            wlen = 0;
        }
    }
    fclose(read_patient_list);
}

int main()
{

    read_ADE= fopen("Enter path of the file that has the ADE list", "r");
    write_missing_patients = fopen("missing_patients.txt", "w");
    read_drug_name = fopen("Enter path of the file that has the drug list", "r");
    read_patient_list = fopen("Enter path of the file that has the patients id", "r");
    patient_list();
    ADE_list();
    drug_list();

    for(int ii = 0; ii < total_patients; ii++)
    {
        not_empty = 0;
        file_operation(ii);
        if(not_empty == 0)
        {
            negative_patients[total_negatives] = ii;
            total_negatives++;
        }
    }
    fclose(write_missing_patients);
    cout << total_notes << endl;
    for(long kk = 0; kk < total_dates; kk++)
    {
        cout << all_dates[kk] << "," << term_frequency[kk] << endl;
    }
    for(int ll = 0; ll < 8; ll++)
    {
        cout << catg[ll] <<endl;
    }
    for(int mm = 0; mm < total_missing; mm++)
    {
        cout << "missing_folders " << all_patients[missing_folders[mm]] << endl;

    }
    for(int nn = 0; nn < total_negatives; nn++)
    {
        cout << "negative_patients " << all_patients[negative_patients[nn]] << endl;
    }

    return 0;
}

