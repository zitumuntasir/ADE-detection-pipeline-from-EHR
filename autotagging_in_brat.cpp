#include <bits/stdc++.h>
#include<fstream>
#include<dirent.h>
using namespace std;
FILE *read_corpus, *read_patient_list, *read_note, *read_corpus_without_space;
FILE *wr, *read_dup_cnt_file;
const int NN = 10000005;
char nxt_one;
char nxt_two;
char nxt_three;
int caseno, cases;
int ins_check;
char a[NN], b[NN];
long lines = 0, ii = 0, got_end_point = 0, current_sent_num = 0;
long len1, c_len, flag[10000000], m, n, pi[NN], res = 0, len = 0, word_num = 0;
map<string, long>indv_cnt;
map<int, int>map_dup_sent;
long t_count, cnt2, indx[100000], already_annotated = 0, all_ind_cnt = 0;
char st, ch;
char extracted_date[550];
char dictionary[1000][1000], temp_word[1000], output_file[1000];
char all_patients[2000][1000], original_current_dir[1000], dict_without_space[1000][1000];
char inp[1000000], temp_line[10000000], current_dir[1000], output_directory[1000], all_files[1000], current_dir_dup_cnt[1000];
long counting_number = 0, day_length = 0, month_length = 0, year_length = 0;
long total_patients = 0, dirlen = 0, out_dir_len = 0, strt_indx = 0;
long out_file_len, wlen = 0, words = 0, file_opened = 0, notes_in_total = 0;
char temp_input[1000000];
long kmpMatcher() {
    long cnt = 0;
    for( long i = 1, k = 0; i <= n; i++ ) {
        while( k > 0 && b[k+1] != a[i] ) k = pi[k];
        if( b[k+1] == a[i] ) k++;
        if( k == m ) {
            cnt++;
            k = pi[k];
            all_ind_cnt++;
            indx[all_ind_cnt] = i;
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
void prn(long w_num, long index, long word_index)
{
    for(long iii = 1; iii <= all_ind_cnt; iii++)
    {
        long mis_drug = 0;
        if(w_num == 32 || w_num == 11|| w_num == 53)
        {
         nxt_one = 'a'; nxt_two = 'a'; nxt_three = 'a';
         if(indx[iii] + 2 < strlen(temp_line))
         {
         nxt_one = tolower(temp_line[indx[iii]]);
         nxt_two = tolower(temp_line[indx[iii] + 1]);
         nxt_three = tolower(temp_line[indx[iii] + 2]);
         }
         if(nxt_one == 't' && nxt_two == 'o' && nxt_three == 'r')
            mis_drug = 1;

        if(nxt_one == 'd' && nxt_two == 'e' && nxt_three == 'm')
            mis_drug = 1;

        if(nxt_one == 't' && nxt_two == 'a' && nxt_three == 'l')
            mis_drug = 1; //occipital

        if(nxt_one == 't' && nxt_two == 'a' && nxt_three == 't')
            mis_drug = 1;            //precipitating
        }
        if(mis_drug == 1)
        {
            cout << current_dir << endl;
            cout << nxt_one << nxt_two << nxt_three << endl;
        }
    if(mis_drug == 0)
    {
        already_annotated = indx[iii] - strlen(dictionary[w_num]);
        if(flag[already_annotated] == 0)
        {
        flag[already_annotated] = 1;
        fprintf(wr,"T%ld	", t_count);
        if(w_num <= 62) fprintf(wr,"drug ");
        else if(w_num <= 372)fprintf(wr,"ADE ");
        else
        {
            cout << "history Found" << endl;
            fprintf(wr,"history ");
        }
        if(word_index == 90 || word_index == 152 ||
           word_index == 156 || word_index == 158 || word_index == 160 || word_index == 165 ||
           word_index == 193 || word_index == 255 || word_index == 259 || word_index == 261 ||
           word_index == 263 || word_index == 268 || word_index == 296 || word_index == 358 ||
           word_index == 362 || word_index == 364 || word_index == 366 || word_index == 371)
            fprintf(wr,"%ld %ld	%s",indx[iii] - strlen(dictionary[w_num]) + 1, indx[iii] - 1, dict_without_space[w_num]);
        else
            fprintf(wr,"%ld %ld	%s",indx[iii] - strlen(dict_without_space[w_num]), indx[iii], dict_without_space[w_num]);
        t_count++;
        fprintf(wr,"\n");
        }
    }
    }
}

void prn_date(int st_ind, int end_ind)
{
        fprintf(wr,"T%ld	", t_count);
        fprintf(wr,"date ");
        fprintf(wr,"%ld %ld	%s",st_ind, end_ind, extracted_date);
        t_count++;
        fprintf(wr,"\n");
}
void prn_dup(int st_ind, int end_ind)
{
        char spc = ' ';
        fprintf(wr,"T%ld	", t_count);
        fprintf(wr,"duplicated_sent ");
        fprintf(wr,"%ld %ld	_sent_",st_ind, end_ind);
        t_count++;
        fprintf(wr,"\n");
}



void patient_list()
{
    wlen = 0;
    while((st = getc(read_patient_list)) != EOF)
    {
        temp_word[wlen] = st;
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

void dic_construct()
{
    wlen = 0;
    words = 0;
    while((st = getc(read_corpus)) != EOF)
    {
        temp_word[wlen] = st;
        wlen++;
        if(st == '\n')
        {
            temp_word[wlen - 1] = '\0';
            strcpy(dictionary[words], temp_word);
            words++;
            wlen = 0;
        }
    }

}

void dic_construct_without_space()
{
    wlen = 0;
    words = 0;
    while((st = getc(read_corpus_without_space)) != EOF)
    {
        temp_word[wlen] = st;
        wlen++;
        if(st == '\n')
        {
            temp_word[wlen - 1] = '\0';
            strcpy(dict_without_space[words],temp_word);
            words++;
            wlen = 0;
        }
    }

}



void file_operation(long current_id)
{
DIR *dir;
struct dirent *ent;

strcpy(current_dir,"enter path of clinical notes");
dirlen = strlen(current_dir);
strcpy(output_directory, "enter path of output directory");
out_dir_len = strlen(output_directory);

/*CREATING DIRECTORIES, DESTINATION UPTO FOLDER*/
for(int pid = 0; pid < 13; pid++)
{
    current_dir[dirlen + pid] = all_patients[current_id][pid];
    output_directory[out_dir_len + pid] = all_patients[current_id][pid];
}
current_dir[dirlen + 13] = '\0';
strcpy(original_current_dir, current_dir);
output_directory[out_dir_len + 13] = '/';
output_directory[out_dir_len + 14] = '\0';

int strln = 0;
strln = strlen(output_directory);
output_directory[strln] = '/';
if ((dir = opendir (current_dir)) != NULL) {
    mkdir(output_directory);
  while ((ent = readdir (dir)) != NULL) {
    strcpy(all_files,ent->d_name);
    strt_indx = all_files[0] - 48;
    file_opened = 0;
    strcpy(current_dir,original_current_dir);
    /*CHECK IF A FILE STARTS WITH A NUMBER TO AVOD DOT*/
    if(strt_indx > 0 && strt_indx <= 9 && strlen(all_files) > 10)
    {
        strcpy(output_file, output_directory);
        out_file_len = strlen(output_file);
        dirlen = strlen(current_dir);
        current_dir[dirlen] = '\\';
        current_dir[dirlen + 1] = '\0';
        dirlen = strlen(current_dir);
        strcpy(current_dir_dup_cnt,current_dir);
        int filelen = strlen(all_files);
        /* current_dir FOR OPENNING THE READ FILE, output_file TO CREATE AN OUTPUT*/
        got_end_point = 0;
        for(int iii = 0; iii < filelen; iii++)
        {
            if(all_files[iii] == '.')
            {
                current_dir_dup_cnt[dirlen + iii] = '\0';
                got_end_point = 1;
            }
            else if(got_end_point == 0)
                current_dir_dup_cnt[dirlen + iii] = all_files[iii];
            current_dir[dirlen + iii] = all_files[iii];
            output_file[out_file_len + iii] = all_files[iii];
        }
        current_dir[dirlen + filelen] = '\0';
        read_dup_cnt_file = fopen(current_dir_dup_cnt, "r");
        len = 0;
        map_dup_sent.clear();
       while((ch = getc(read_dup_cnt_file)) != EOF)
      {
        if(ch == '\n' && len > 0) {
        temp_line[len] = '\0';
        int x = atoi(temp_line);
        map_dup_sent[x] = 1;
        len = 0;
        }
        else{
        temp_line[len] = ch;
        len++;
        }
      }
      if(len > 0)
      {
        temp_line[len] = '\0';
        int x = atoi(temp_line);
        map_dup_sent[x] = 1;
      }

        output_file[out_file_len + filelen] = '\0';
        out_file_len = strlen(output_file);
        output_file[out_file_len - 1] = 'n';
        output_file[out_file_len - 2] = 'n';
        output_file[out_file_len - 3] = 'a';
        read_note = fopen(current_dir, "r");
        wr = fopen(output_file,"w");
        len = 0;
        current_sent_num = 0;
        t_count = 0;
        int start_len = 0;
       while((ch = getc(read_note)) != EOF)
      {
        word_num = 0;
        if(ch == '\n') {
        if(map_dup_sent[current_sent_num] == 1)
                prn_dup(start_len + 2,start_len + 8);
        temp_line[len] = ' ';
        inp[len] = ' ';
        start_len = len;
        len++;
        current_sent_num++;
        }
        temp_line[len] = ch;
        inp[len] = ch;
        len++;
      }
        temp_line[len] = '\0';
        inp[len] = '\0';
        long res1 = 0, res2 = 0;
        res = 0;
        lines++;
        strcpy(a + 1,temp_line);
        n = strlen(a + 1);
        memset(flag,0,sizeof(flag));
        for(long dd = 0; dd < words; dd++)
        {
            long val = dictionary[dd][0] - 97;
            all_ind_cnt = 0;
            strcpy(b + 1,dictionary[dd]);
            m = strlen(b + 1);
            computePrefix();
            res = kmpMatcher();
            if(res > 0)
            {
                word_num = dd;
                prn(word_num, res, dd);
                res = 0;
                flag[val] = 1;
            }
        }
        res = 0;
        len = 0;
        word_num = 0;

    len1 = strlen(inp);
    for(ii = 0; ii < len1; ii++)
    {
        c_len = 0; month_length = 0; day_length = 0; year_length = 0; cnt2 = 0;
        if(inp[ii] == '*' && inp[ii+1] == '*' && ii+12 < len1 && ii+13 < len1 && inp[ii+12] == '*' && inp[ii+13] == '*' && inp[ii-1] == '[' && inp[ii+14] == ']' && inp[ii+6] == '-' && inp[ii+9] == '-')
        {
         extracted_date[0] = inp[ii + 2];
         extracted_date[1] = inp[ii + 3];
         extracted_date[2] = inp[ii + 4];
         extracted_date[3] = inp[ii + 5];
         extracted_date[4] = inp[ii + 6];
         extracted_date[5] = inp[ii + 7];
         extracted_date[6] = inp[ii + 8];
         extracted_date[7] = inp[ii + 9];
         extracted_date[8] = inp[ii + 10];
         extracted_date[9] = inp[ii + 11];
         extracted_date[10] = '\0';
         prn_date(ii+2,ii+12);
         ii += 13;
        }
    }
    }
        fclose(wr);
        fclose(read_note);
  }
}
}


int main()
{
    read_corpus = fopen("corpus.txt", "r");
    dic_construct();
    fclose(read_corpus);
    read_corpus_without_space = fopen("corpus_without_space.txt", "r");
    dic_construct_without_space();
    fclose(read_corpus_without_space);
    read_patient_list = fopen("Enter path of the file having patients id", "r");
    patient_list();
    for(long ii = 0; ii < total_patients; ii++)
    {
        cout << ii << endl;
        file_operation(ii);
    }
     return 0;
}
