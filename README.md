# tahquitz project
## Taking a look at weather patterns at one of the home crags. Tahquitz sports 4-8 pitch lines of splitter crack and sticky slab climbing. Currently, I am collecting data from a weather api using a cron job to automate running the py script.

To do:<br>
-git clone ssh-key <br>
-git checkout -b new_branch_name <br>
-pip install -r requirements.txt <br>
-crontab -e <br>
-input text below to schedule a 6AM run, activate the venv & run the python exe from here, and send a log to a filed named<br> tah_log in the root directory<br>
-0 6 * * * /home/abdierkes/tahquitz/venv/bin/python /home/abdierkes/tahquitz/run_daily.py >><br> /home/abdierkes/tahquitz/tah_log.log 2>&1<br>
-nano tah_log.log & you should see Parsed and Uploaded on date<br>
-visualization TO DO<br>
