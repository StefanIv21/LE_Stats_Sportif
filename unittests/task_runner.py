"Simple thread pool implementation."
import ast
import logging
import os
from queue import Queue
from threading import Thread, Event
import threading
import json


class ThreadPool:
    "A thread pool, distributing tasks among a fixed number of threads."
    def __init__(self,logger):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        if 'TP_NUM_OF_THREADS' in os.environ:
            self.num_threads = int(os.environ['TP_NUM_OF_THREADS'])
        else:
            self.num_threads = os.cpu_count()
        self.logger = logger
        self.tasks = Queue()
        self.threads = []
        self.terminate = Event()
        self.job_status =[]
        self.job_done = 0
        self.lock = threading.Lock()
        for _ in range(self.num_threads):
            self.threads.append(TaskRunner(self,self.terminate))
        for thread in self.threads:
            thread.start()
        result_path = "./results"
        if not os.path.exists(result_path):
            os.makedirs(result_path)
class TaskRunner(Thread):
    "Worker thread that consumes tasks from a queue and processes them."
    def __init__(self, pool,terminate):
        Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.thread_pool = pool
        self.terminate = terminate

    def run(self):
        queue = self.thread_pool.tasks
        self.logger = self.thread_pool.logger
        while True:
            if(self.terminate.is_set() and queue.empty()):
                break
            (endpoint,recv,job_id,data) = queue.get()
            if endpoint == 'states_mean':
                dictionar = self.states_mean(data)
                self.write_in_file(dictionar,job_id)
            elif endpoint == 'state_mean':
                dictionar = self.state_mean(data,recv['state'])
                self.write_in_file(dictionar,job_id)
            elif endpoint == 'best5':
                top5 = self.best5(data)
                self.write_in_file(top5,job_id)
            elif endpoint == 'worst5':
                worst5 = self.worst5(data)
                self.write_in_file(worst5,job_id)
            elif endpoint == 'global_mean':
                dictionar = self.global_mean(data)
                self.write_in_file(dictionar,job_id)
            elif endpoint == 'diff_from_mean':
                dictionar_states = self.states_mean(data)
                dictionar_states = self.diff_from_mean(data)
                self.write_in_file(dictionar_states,job_id)
            elif endpoint == 'state_diff_from_mean':
                state_mean = self.state_diff_from_mean(data,recv['state'])
                self.write_in_file(state_mean,job_id)
            elif endpoint == 'mean_by_category':
                dictionar = self.mean_by_category(data)
                self.write_in_file(dictionar,job_id)
            elif endpoint == 'state_mean_by_category':
                dictionar = self.state_mean_by_category(data,recv['state'])
                self.write_in_file(dictionar,job_id)
            name_id_job = 'job_id_' + str(job_id)
            for dictionar in self.thread_pool.job_status:
                if name_id_job in dictionar and dictionar[name_id_job] == 'running':
                    dictionar[name_id_job] = 'done'
                    with self.thread_pool.lock:
                        self.thread_pool.job_done += 1
                    break
    def best5(self,data):
        """Function to calculate best 5 states."""
        self.logger.info(" Enter the method BEST5 with parameter Parsed CSV")
        dictionar = self.states_mean(data)
        best5 = dict(list(dictionar.items())[:5])
        self.logger.info(" Exit the method BEST5")
        return best5
    def worst5(self,data):
        """Function to calculate worst 5 states."""
        self.logger.info(" Enter the method WORST5 with parameter Parsed CSV")
        dictionar = self.states_mean(data)
        worst5 = list(dictionar.items())[-5:]
        worst5.reverse()
        self.logger.info(" Exit the method WORST5")
        return dict(worst5)
    def diff_from_mean(self,data):
        """Function to calculate difference between mean of a states and global mean."""
        self.logger.info(" Enter the method DIFF_FROM_MEAN with  parameter Parsed CSV")
        dictionar_states = self.states_mean(data)
        global_mean = self.global_mean(data)
        for state in dictionar_states:
            dictionar_states[state] = global_mean['global_mean'] - dictionar_states[state]
        self.logger.info(" Exit the method DIFF_FROM_MEAN")
        return dictionar_states
    def state_diff_from_mean(self,data,state):
        """Function to calculate difference between mean of a state and global mean."""
        self.logger.info(
            f"Enter the method STATE_DIFF_FROM_MEAN with parameter Parsed CSV and state {state}")
        state_mean = self.state_mean(data[state],state)
        global_mean = self.global_mean(data)
        state_mean[state] = global_mean['global_mean'] - state_mean[state]
        self.logger.info(" Exit the method STATE_DIFF_FROM_MEAN")
        return state_mean
    def states_mean(self,data):
        """Function to calculate mean of a states"""
        self.logger.info(" Enter the method STATES_MEAN with parameter Parsed CSV")
        dictionar = {}
        for state in data:
            lista = data[state]
            lista_numere = [float(x) for x in lista]
            mean = sum(lista_numere) / len(lista_numere)
            dictionar[state] = mean
        final_dict = dict(sorted(dictionar.items(), key=lambda item: item[1]))
        self.logger.info(" Exit the method STATES_MEAN")
        return final_dict
    def write_in_file(self,data,job_id):
        """Function to write on disk."""
        self.logger.info(
            f"Enter the method WRITE_IN_FILE with parameter Parsed CSV and job_id {job_id}")
        path = "./results/job_id_" + str(job_id) + ".json"
        with open(path, 'w',encoding='utf-8') as file:
            file.write(json.dumps(data))
        self.logger.info(" Exit the method WRITE_IN_FILE")
    def state_mean(self,data,state):
        """Function to calculate mean of a state """
        self.logger.info(
            f" Enter the method STATE_MEAN with  parameter Parsed CSV and state {state}")
        lista = data
        lista_numere = [float(x) for x in lista]
        mean = sum(lista_numere) / len(lista_numere)
        dictionar = {}
        dictionar[state] = mean
        self.logger.info(" Exit the method STATE_MEAN")
        return dictionar
    def global_mean(self,data):
        """Function to calculate global mean."""
        self.logger.info(" Enter the method GLOBAL_MEAN with  parameter Parsed CSV")
        all_values_list = []
        for state in data:
            lista = data[state]
            lista_numere = [float(x) for x in lista]
            all_values_list.extend(lista_numere)
        mean = sum(all_values_list) / len(all_values_list)
        dictionar = {}
        dictionar["global_mean"] = mean
        self.logger.info(" Exit the method GLOBAL_MEAN")
        return dictionar
    def mean_by_category(self,data):
        """Function to calculate mean of a states."""
        self.logger.info(" Enter the method MEAN_BY_CATEGORY with  parameter Parsed CSV")
        dictionar = {}
        for category in data:
            lista = data[category]
            lista_numere = [float(x) for x in lista]
            mean = sum(lista_numere) / len(lista_numere)
            dictionar[category] = mean
        sorted_dictionar = dict(sorted(dictionar.items(), key=lambda item: item[0]))
        self.logger.info(" Exit the method MEAN_BY_CATEGORY")
        return sorted_dictionar
    def state_mean_by_category(self,data,state):
        """Function to calculate mean of a state by a category."""
        self.logger.info(
            f" Enter the method STATE_MEAN_BY_CATEGORY with parameter Parsed CSV and state {state}")
        dictionar = {}
        for category in data:
            if state in category:
                lista = data[category]
                lista_numere = [float(x) for x in lista]
                mean = sum(lista_numere) / len(lista_numere)
                all_elem_in_tuple = ast.literal_eval(category)
                new_tuple = (all_elem_in_tuple[1],all_elem_in_tuple[2])
                new_tuple = str(new_tuple)
                dictionar[new_tuple] = mean
        sorted_dictionar = dict(sorted(dictionar.items(), key=lambda item: item[0]))
        final_dictionar = {}
        final_dictionar[state] = sorted_dictionar
        self.logger.info("Exit the method STATE_MEAN_BY_CATEGORY")
        return final_dictionar
