"""This module contains the routes for the webserver."""
import json
from flask import request, jsonify
from app import webserver





# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    """Function to check the method of the request."""
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """Function to get the response of a given job_id."""
    webserver.logger.info(
        f" Enter the method GET_RESPONSE with parameter: {job_id}")
    #pentru fiecare job verific statusul acestuia(valoarea din dictionar)
    for dictionar in webserver.tasks_runner.job_status:
        if job_id in dictionar:
            if dictionar[job_id] == 'done':
                path = "./results/" + str(job_id) + ".json"
                with open(path, 'r',encoding='utf-8') as file:
                    data = json.load(file)
                webserver.logger.info(" Exit the method GET_RESPONSE")
                return jsonify({"status": "done", "data": data})
            webserver.logger.info(" Exit the method GET_RESPONSE")
            return jsonify({"status": "running"})
    webserver.logger.info(" Exit the method GET_RESPONSE")
    return jsonify({"status": "error", "reason": "Invalid job_id"})


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    "Function to process a states_mean request."
    webserver.logger.info(" Enter the method STATES_MEAN_REQUEST")
    id_req = complete_request(request.json, "states_mean")
    webserver.logger.info(" Exit the method STATES_MEAN_REQUEST")
    return id_req


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    "Function to process a state_mean request."
    webserver.logger.info(" Enter the method STATE_MEAN_REQUEST")
    id_req = complete_request(request.json, "state_mean")
    webserver.logger.info(" Exit the method STATE_MEAN_REQUEST")
    return id_req


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    "Function to process a best5 request."
    webserver.logger.info(" Enter the method BEST5_REQUEST")
    id_req = complete_request(request.json, "best5")
    webserver.logger.info(" Exit the method BEST5_REQUEST")
    return id_req


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    "Function to process a worst5 request."
    webserver.logger.info(" Enter the method WORST5_REQUEST")
    id_req = complete_request(request.json, "worst5")
    webserver.logger.info(" Exit the method WORST5_REQUEST")
    return id_req


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    "Function to process a global_mean request."
    webserver.logger.info(" Enter the method GLOBAL_MEAN_REQUEST")
    id_req = complete_request(request.json, "global_mean")
    webserver.logger.info(" Exit the method GLOBAL_MEAN_REQUEST")
    return id_req


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    "Function to process a diff_from_mean request."
    webserver.logger.info(" Enter the method DIFF_FROM_MEAN_REQUEST")
    id_req = complete_request(request.json, "diff_from_mean")
    webserver.logger.info(" Exit the method DIFF_FROM_MEAN_REQUEST")
    return id_req


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    "Function to process a state_diff_from_mean request."
    webserver.logger.info(" Enter the method STATE_DIFF_FROM_MEAN_REQUEST")
    id_req = complete_request(request.json, "state_diff_from_mean")
    webserver.logger.info(" Exit the method STATE_DIFF_FROM_MEAN_REQUEST")
    return id_req


@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    """Function to gracefully shutdown the webserver."""
    webserver.logger.info(" Enter the method GRACEFUL_SHUTDOWN")
    webserver.tasks_runner.terminate.set()
    webserver.logger.info(" Exit the method GRACEFUL_SHUTDOWN")
    return jsonify({"status": "shutting_down"})


@webserver.route('/api/jobs', methods=['GET'])
def jobs():
    """Function to get the status of all jobs."""
    webserver.logger.info(" Enter the method JOBS")
    dict_jobs = {}
    dict_jobs["status"] = "done"
    dict_jobs["data"] = webserver.tasks_runner.job_status
    webserver.logger.info(" Exit the method JOBS")
    return jsonify(dict_jobs)


@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs():
    """Function to get the number of jobs."""
    webserver.logger.info(" Enter the method NUM_JOBS")
    remanin = webserver.job_counter - webserver.tasks_runner.job_done - 1
    webserver.logger.info(" Exit the method NUM_JOBS")
    return jsonify({"num_jobs": remanin})


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """Function to process a mean_by_category request."""
    webserver.logger.info(" Enter the method MEAN_BY_CATEGORY_REQUEST")
    id_req = complete_request(request.json, "mean_by_category")
    webserver.logger.info(" Exit the method MEAN_BY_CATEGORY_REQUEST")
    return id_req


@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """Function to process a state_mean_by_category request."""
    webserver.logger.info(" Enter the method STATE_MEAN_BY_CATEGORY_REQUEST")
    id_req = complete_request(request.json, "state_mean_by_category")
    webserver.logger.info(" Exit the method STATE_MEAN_BY_CATEGORY_REQUEST")
    return id_req

# You can check localhost in your browser to see what this displays


@webserver.route('/')
@webserver.route('/index')
def index():
    """Function to display the index page."""
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg


def get_defined_routes():
    """Function to get all defined routes."""
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes


def complete_request(data_request, type_request):
    """Function to complete a given request."""
    webserver.logger.info(
        " Enter the method COMPLETE_REQUEST with parameter: {data_request} and {type_request}")
    # nu mai accept requesturi daca serverul s a oprit
    if webserver.tasks_runner.terminate.is_set():
        return jsonify({"status": "No more requests accepted"})
    #iau id ul si cresc counter ul
    id_req = webserver.job_counter
    webserver.job_counter += 1
    question = data_request['question']
    queue = webserver.tasks_runner.tasks
    #pentru fiecare tip de endpoint, pun in coada datele necesare
    if type_request == "state_mean":
        state = data_request['state']
        queue.put([type_request, data_request, id_req,
                  webserver.data_ingestor.data[question][state]])
    elif type_request in ('best5', 'worst5'):
        question_conditions = [
            "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)",
            "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week",
            "Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)",
            "Percent of adults who engage in muscle-strengthening activities on 2 or more days a week"]
        type1 = ''
        type2 = ''
        if type_request == 'best5':
            type1 = 'worst5'
            type2 = 'best5'
        else:
            type1 = 'best5'
            type2 = 'worst5'

        if question in question_conditions:
            queue.put([type1, data_request, id_req,
                      webserver.data_ingestor.data[question]])
        else:
            queue.put([type2, data_request, id_req,
                      webserver.data_ingestor.data[question]])

    elif type_request in ('mean_by_category', 'state_mean_by_category') :
        queue.put([type_request, data_request, id_req,
                  webserver.data_ingestor.data_by_category[question]])
    else:
        queue.put([type_request, data_request, id_req,
                  webserver.data_ingestor.data[question]])

    dictionar = {}
    name_id = "job_id_" + str(id_req)
    dictionar[name_id] = 'running'
    webserver.tasks_runner.job_status.append(dictionar)
    webserver.logger.info(" Exit the method COMPLETE_REQUEST")
    return jsonify({"job_id": name_id})
