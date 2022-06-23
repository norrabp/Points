# Points
This server allow you to add new transactions and spend points from those transactions. Each transaction has a payer the transaction was made with and the number of points obtained by each transaction. When spending these points, the points from the earliest transactions are spent first.

## Install

Install [Python3.6](https://www.python.org/downloads/) or greater

Clone this project

```
$ git clone https://github.com/norrabp/points.git platform
```

Install project dependencies:

```
cd Points
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
chmod +x points.sh
```

## Project Structure

The repository should look like this:
```
.
├── README.md
├── app
│   ├── __init__.py
│   ├── api_v1
│   │   ├── __init__.py
│   │   ├── errors.py
│   │   └── points.py
│   ├── core
│   │   ├── __init__.py
│   │   └── core.py
│   └── exceptions.py
├── config
│   ├── development.py
│   └── testing.py
├── points.sh
├── requirements.txt
├── run.py
├── test.py
└── tests
    ├── __init__.py
    ├── cases
    │   ├── __init__.py
    │   ├── test_add_transactions.py
    │   ├── test_input_checks.py
    │   ├── test_spend_points_negative.py
    │   ├── test_spend_points_positive.py
    │   └── test_validation.py
    └── utils
        ├── __init__.py
        ├── client.py
        └── timestamp.py
```
`/app` contains all the code for the web server including APIs, core functions,
and error handling
- `/api_v1` contains the HTTP endpoints for getting transactions and payer totals, adding transactions, and spending points in `points.py` and error handling in `errors.py`
- `/core` contains core functions used by the api. Currently it only contains a function that subtracts points from a transaction

`/config` contains the configuration settings for testing versus development.

`/tests` contains the unit tests for the application.
- `/cases` contains the files for all unit test cases
- `/utils` contains utility functions and a test client interface to interact with the server

## Running the Application

To run the application normally, type in 

```
export FLASK_CONFIG=development
python3 run.py
```

To run the tests, run
```
export FLASK_CONFIG=testing
python3 test.py
```

## APIs

Run the following commands in your terminal (separate from the one running the instance of the website)

##### Getters

- Get a list of all transactions
    - Command: `http GET http://localhost:5000/api/v1/transactions/`
    - Returns:
        - Status Code: `200`
        - Data: 
        ```
        [
            {
                payer: <payer name>
                points: <points from the transaction>
                points_remaining: <remaining points to spend on the transaction>
                timestamp: <timestamp of the transaction>
            },
            ...
        ]
        ```

- Get a summary of the points associated with each payer
    - Command: `http GET http://localhost:5000/api/v1/points/`
    - Returns:
        - Status Code: `200`
        - Data: 
        ```
        [
            {
                payer: <payer name>
                points: <total points the payer currently has>
            },
            ...
        ]
        ```

##### Create

- Add a transaction
    - Command: `http POST http://localhost:5000/api/v1/transactions/`
    - Arguments:
        - payer: Name of the payer for the transaction
        - points: Points added by the transaction
        - timestamp: OPTIONAL: timestamp for the transaction in YYYY-MM-DDTHH:MM:SSZ format
            - Ex. "2020-11-02T14:00:00Z"
            - Defaults to now
    - Returns:
        - Status Code: `201`
        - Data: 
        ```
        [
            {
                payer: <payer name>
                points: <points from the transaction>
                points_remaining: <remaining points to spend on the transaction>
                timestamp: <timestamp of the transaction>
            },
            ...
        ]
        ```
    - If the transaction is negative and would make the payer total negative:
        - Status Code: `200`
        - Data:
        ```
        {
            'message': "Transaction would make payer points lets than 0",
            'payer': <name of payer>,
            'payer_points': <total points for that payer>
        }
        ```
- Spend points
    - Command: `http PUT http://localhost:5000/api/v1/points/`
    - Arguments:
        - points: Points to spend
    - Returns:
        - Status Code: `200`
        - Data: 
        ```
        {
            <payer name>: <points subtracted from payer total>,
            ...
        }
        ```
    - If points specified greater than the total points of all payers:
        - Status Code: `200`
        - Data:
        ```
        {
            "message": "Not enough points to spend",
            "total_points": <Sum of all payers current points>
        }
        ```

