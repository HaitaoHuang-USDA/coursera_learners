# Steps to revoke Coursera license

* Coursera web page -> Home -> select program -> Manage Learners -> Select all -> "Download as .csv"
* Received email Download -> Save to the folder "SCINet Office - Documents\Training\Coursera License\Downloaded Learner List"
* Run the python program process_learners.py
* Open the result csv, copy the top n rows to the Excel file 'Coursera Learners' - Sheet 'Removed List' (in folder "SCINet Office - Documents\Training\Coursera License)
* On Coursera Admin page, remove the selected learners from the joined programs (**remove all programs associated with the learner**)
