#### Features
 - Displays the top 10 ten traded scrips on BSE
 - Search through all listed securities on BSE and get information(OPEN, HIGH, LOW, CLOSE, PREVIOUS CLOSE, NUMBER OF TRADES)

#### Under the hood
 - CherryPy for exposing API endpoints.
 - Selenium with headless Chrome to fetch daily Bhavcopy from BSE.
 - Redis as an in-memory datastore. A key `last_sync` is used to keep track of last updated Bhavcopy with expiry as:
   - 1600 - hour of last_sync (in case when the check is made before 4pm in the evening)
   - +1 day (in case when the check is made after 4pm in the evening)
 - Redis hashes to store details of each scrip
 - Redis Sets for searching through names of all scrips and sorting top 10 traded scrips.
 - Jquery, HTML and CSS for the not-so-good front end.


#### Deployment

The deployed app is at https://zero-task.herokuapp.com/
