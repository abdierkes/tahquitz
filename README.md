# tahquitz project
## Taking a look at weather patterns at one of the home crags. Tahquitz sports 4-8 pitch lines of splitter crack and sticky slab climbing. Currently, I am collecting data from the previous day using a cron job to automate running the py script.

To do:
-git clone <ssh-key>
-git checkout -b new_branch_name 
-pip install -r requirements.txt
-crontab -e
-input text below to schedule a 6AM run, activate the venv & run the python exe from here, and send a log to a filed named tah_log in the root directory; if you nano tah_log.log you should see {date} and committed
-0 6 * * * /home/abdierkes/tahquitz/venv/bin/python /home/abdierkes/tahquitz/run_daily.py >> /home/abdierkes/tahquitz/tah_log.log 2>&1
-visualization TO DO
