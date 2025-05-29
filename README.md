# Steps to revoke Coursera license

* Select learners no longer in ARS
* Select learners having longest period of inactive.
  * Coursera main page -> Home -> select program -> Manage Learners -> Select all -> "Download as .csv"
  * Clear the folder "SCINet Office - Documents\Training\Coursera License\Downloaded Learner List"
  * Received email -> Download -> Save to the folder "SCINet Office - Documents\Training\Coursera License\Downloaded Learner List"
  * Run the python program process_learners.py
  * Open the result csv, copy the top n rows to the Excel file 'Coursera Learners' - Sheet 'Removed List' (in folder "SCINet Office - Documents\Training\Coursera License)
    * The copied list is ordered by latest activity date.
* On Coursera Admin page, remove the selected learners from the joined programs (**remove all programs associated with the learner**)
