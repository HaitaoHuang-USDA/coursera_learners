# Steps to revoke Coursera license

* Find learners no longer in ARS (**manually**).
* Select learners having longest period of inactive.

  * Coursera main page -> Home -> Programs -> select program -> Program Learners -> Modify columns (Button on top right of the table) -> ensure the following checked
    * Status, Join Date, Last Activity
    * Full name and Email will be included (Learners name - always displayed)
  * Click 'Joined' button (make it black) and keep 'Invited' and 'Removed' buttons white.
  * **Don't do**:
    * desc sort the learners by Last Activity and delete the top learners
    * a learner in one program with earliest Last Activity date may have much later Last Activity date in other program
    * this way can be done only if there's only one program ('AI Center of Excellence Program' of Study or 'SCINet Program of Study')
  * Select all (The checkbox in the table's title)-> "Download csv" (appears in blue table title area table after select all)
  * download csv for other 1 program
  * Clear the local folder "SCINet Office - Documents\Training\Coursera License\Downloaded Learner List" (move to a new date folder in backups) - the following steps will read all the csv files
  * Wait for the emails for download is ready ->Received email -> Download -> Save to the folder "SCINet Office - Documents\Training\Coursera License\Downloaded Learner List"
  * Run the python program process_learners.py (conda env 'ai4onp2') - https://github.com/HaitaoHuang-USDA/coursera_learners
    * the program chooses latest date from join date and last activity in the programs, and sort the latest date.
    * local position: _github_scinet\coursera_learners
    * open the folder in vscode, run 'Python: Process Learners'
    * In the downloaded csv file, the header of Full Name and Email may change. If so, change the columns names in the python code. (e.g. Email changed to Email*)
    * The invitation date in final df may be blank - ok
  * Open the result csv, copy the top n rows and **paste values** to the end of the Excel file 'Coursera Learners' - Sheet 'Removed List' (in folder "SCINet Office - Documents\Training\Coursera License)
    * The copied list is ordered by latest activity date.
* On Coursera Admin page, remove the selected learners from the joined programs (**remove all programs associated with the learner**)
  * tip - copy 5 cells in the email column and paste to the search box on the program learner's page (above the table) - so the 5 learners can be filltered in one step (tried more but the Coursera page seems confused)
   
