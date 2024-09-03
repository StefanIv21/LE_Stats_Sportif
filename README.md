# Nutrition Statistics Server
## Purpose
The goal of this project is to:
  - Efficiently use synchronization elements studied in the lab.
  - Implement a concurrent application using a classic client-server problem.
  - Deepen understanding of Python elements including classes, syntax, threads, synchronization, and using Python modules for threading.

## Implementation
 A Python server that handles a series of requests based on a dataset in CSV (comma-separated values) format. The server will provide statistics based on the data from the CSV file.
Dataset

The dataset contains information about nutrition, physical activity, and obesity in the United States from 2011 to 2022. The data, collected by the U.S. Department of Health & Human Services, is organized by state (e.g., California, Utah, New York) and addresses the following questions:

    Percent of adults who engage in no leisure-time physical activity
    Percent of adults aged 18 years and older who have obesity
    Percent of adults aged 18 years and older who have an overweight classification
    Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)
    Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week
    Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)
    Percent of adults who engage in muscle-strengthening activities on 2 or more days a week
    Percent of adults who report consuming fruit less than one time daily
    Percent of adults who report consuming vegetables less than one time daily

Values used for statistical calculations are in the Data_Value column.
## Implementation Details

The server application is multi-threaded. When the server starts, it load the CSV file and extract information to calculate the required statistics. The server model includes:

 - An endpoint (e.g., /api/states_mean) that receives a request and returns a job_id (e.g., “job_id_1”, “job_id_2”, …, “job_id_n”).
 - An endpoint /api/get_results/job_id that checks if the job_id is valid, whether the result is ready or not, and returns the appropriate response.

## Request Mechanics
  - Associate a job_id with the request.
  - Put the job (closure encapsulating the unit of work) into a job queue processed by a thread pool.
  - Increment the internal job_id and return the job_id to the client.
  - A thread will pick a job from the queue, perform the operation (what was captured by the closure), and write the result to a file named after the job_id in the results/ directory.

## Endpoints implemented

- <b> states_mean: </b> Receives a question and calculates the mean value (Data_Value) for each state, sorted in ascending order.
- <b> state_mean: </b> Receives a question and a state, and calculates the mean value for the specified state.
- <b> best5: </b> Receives a question and calculates the mean value for each state, returning the top 5 states.
- <b> worst5: </b> Receives a question and calculates the mean value for each state, returning the bottom 5 states.
- <b> global_mean: </b> Receives a question and calculates the global mean value from the entire dataset.
- <b> diff_from_mean: </b> Receives a question and calculates the difference between the global mean and the state mean for all states.
- <b> state_diff_from_mean: </b> Receives a question and a state, and calculates the difference between the global mean and the state mean for that state.
- <b> mean_by_category: </b> Receives a question and calculates the mean value for each segment (Stratification1) within categories (StratificationCategory1) for each state.
- <b> state_mean_by_category: </b> Receives a question and a state, and calculates the mean value for each segment within categories for that state.
- <b> graceful_shutdown: </b> Responds to a GET request to notify the thread pool about ending processing. No new requests will be accepted, and the application will shutdown gracefully after processing existing requests.
- <b> jobs: </b> Responds to a GET request with a JSON listing all JOB_IDs and their statuses.
- <b> num_jobs: </b> Responds to a GET request with the number of remaining jobs to be processed. After /api/graceful_shutdown, it should return 0, signaling that the Flask server can be stopped.
- <b> get_results/<job_id>: </b> Responds to a GET request with the result of the job based on the job_id.

## Server Implementation

The server is implemented using the Flask framework.

Alternatively, use the provided Makefile:

## Run
```bash

make create_venv
source venv/bin/activate
make install
 ```   



    



