# an SMS Sync Intergration
Pulls Messags pushed by Ushahidi's SMSsync and displays them in a downladable format<br`

## TODO
- [ ] Add flask-socket io Intergartion
- [ ] Register call back to start receiving messages
- [ ] Write Tests


## running the application

###### 1. clone the repo to the directory of your choice

`$ git clone git@github.com:Piusdan/sms-sync-MPESA.git`

###### 2. go to the project's root directory
` $ cd sms-sysncM-MPESA`

###### 3. add priviledges to the projects running scripts
`$ chmod +x ./run_app.sh && chmod +x run_worker.sh`

###### 4. create and activate your virtual environment

`$ python3 -m venv .venv $$ source .venv/bin/activate`

###### 5. Install dependancies

`$ pip install -r requirements.txt`

###### 6. launch the development server
`$ ./run_app.sh`

The app will start at [localhost](http://127.0.0.1:5000/dashboard) :smile:

## To run the worker

###### 1. Open a new Terminal and repeat procesess 2 and 4(since you have a virtual environment created, just activate it)

###### 2. Run the worker script
` $ ./run_worker.sh`

Your worker will now launch and will be ready to start receiving tasks :smile:

