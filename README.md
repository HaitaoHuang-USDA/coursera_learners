# Steps to revoke Coursera license

* Select learners no longer in ARS
* Select learners having longest period of inactive.
  * Coursera main page -> Home -> select program)-> Program Learners -> Modify columns (Button on top right of the table) -> ensure the following checked
    * Status, Join Date, Latest Activity Date
    * Full name and Email will be included (Learners name - always displayed)
  * Select all (The checkbox in the table's title)-> "Download csv" (appears in blue table title area table after select all)
  * download csv for other 1 program
  * Clear the local folder "SCINet Office - Documents\Training\Coursera License\Downloaded Learner List" - the following steps will read all the csv files
  * Wait for the emails for download is ready ->Received email -> Download -> Save to the folder "SCINet Office - Documents\Training\Coursera License\Downloaded Learner List"
  * Run the python program process_learners.py (conda env 'ai4onp2')
  * Open the result csv, copy the top n rows and **paste values** to the end of the Excel file 'Coursera Learners' - Sheet 'Removed List' (in folder "SCINet Office - Documents\Training\Coursera License)
    * The copied list is ordered by latest activity date.
* On Coursera Admin page, remove the selected learners from the joined programs (**remove all programs associated with the learner**)
