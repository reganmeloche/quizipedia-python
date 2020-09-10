Todo:
- Part 1: get familiar with the NLP tools (udemy)
- Part 2: closely mimic the existing JS functionality
- Part 3: perform analysis on the words to generate the quiz
- Part 4: Perform analysis on the sentences to generate the quiz

Other:
- Store the documents for monitoring - likely in a document store
- Create an admin page to view the monitoring and judgment calls

* The python engine will likely do the processing and send back a fairly bulky object
- the object willl include judgment calls and calculations and scores
- it will all be sent back to js. But only the subset will be stripped away for actual saving and playing
- the bulk of it will get stored in a document store
- then it can be accessed using the admin page.


## Running

python wsgi.py

## Deploying

git push heroku master

## Testing

python -m unittest tests/*.py