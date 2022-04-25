# Task 5. Solution Design:
Customer is facing following problem: when processing xml file via cron-job, cron-job fails, doesn’t process all lines (connection timem-out, CPU time limit exceeded). File is very big and increasing limit_time_real_cron or other params on odoo.config, doesn’t solves the issue.
The cron-job is creating/updating products from xml file.
Xml could look like this, but with much more <book> tags: https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ms762271(v=vs.85)

#### • Write a solution design, how you would fix this issue.

#### • Provide estimation for development

## Solution:

1. After getting data by first cron we need to split data by items(book) and save raw data in object with fields: raw_data, state(new,done,error)
2. Second cron must get variables 'limit' and 'time'(by default 50 and 4*60) and process raw_data. It cron time executing shouldn't be more than 4 minutes and in every object with raw data need to change state on 'done' after a good processing or 'error' if something was wrong