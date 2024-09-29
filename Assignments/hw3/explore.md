## Task 2
### How big is the dataset
```bash
ls -lh clean_dialog.csv
```
```
-rw-rw-r-- 1 ubuntu ubuntu 4.7M Sep 18 23:39 clean_dialog.csv
```
* The size of the dataset is 4.7MB

```bash
wc -l < clean_dialog.csv
```
```
36860
```
* The dataset contains 36860 rows

### **What's the structure of the data?**
```bash
head -2  clean_dialog.csv
```
```
"title","writer","pony","dialog"
"Friendship is Magic, part 1","Lauren Faust","Narrator","Once upon a time, in the magical land of Equestria, there were two regal sisters who ruled together and created harmony for all the land. To do this, the eldest used her unicorn powers to raise the sun at dawn; the younger brought out the moon to begin the night. Thus, the two sisters maintained balance for their kingdom and their subjects, all the different types of ponies. But as time went on, the younger sister became resentful. The ponies relished and played in the day her elder sister brought forth, but shunned and slept through her beautiful night. One fateful day, the younger unicorn refused to lower the moon to make way for the dawn. The elder sister tried to reason with her, but the bitterness in the young one's heart had transformed her into a wicked mare of darkness: Nightmare Moon."
```
The data is structured in a CSV format with the following fields and values:
- "title": The title of the episode.
- "writer": The writer of the episode.
- "pony": The pony character who is speaking.
- "dialog": The spoken dialog by the character.


### How many episodes does it cover
```bash
csvtool col 1 clean_dialog.csv | tail -n +2 | sort -u | wc -l
```
```
197
```
* It covers 197 episodes


### one aspect of the dataset that is unexpected
* Some of the pony's dialogues are very long, while others are very short. Therefore, when counting them as a single dialogue, their weights should be different. This could potentially pose issues in future analyses.


## Task 3
* Use grep to count the number of dialogs of each pony
```bash
grep -oE 'Applejack|Fluttershy|Pinkie Pie|Rarity|Rainbow Dash' clean_dialog.csv | sort | uniq -c > pony_count.txt
```
* Calculate the percentage of each pony’s lines in the total lines, and save the results to the Line_percentages.csv file.

```bash
# Create a new CSV file and write the header
echo "pony_name,total_line_count,percent_all_lines" > Line_percentages.csv

# Define the total number of lines
total_lines=36860

# Read the content of the pony_counts.txt file and calculate the percentage
while read -r count pony_name; do
  percent=$(echo "scale=4; $count / $total_lines * 100" | bc)  echo "$pony_name,$count,$percent" >> Line_percentages.csv
done < pony_counts.txt
```

