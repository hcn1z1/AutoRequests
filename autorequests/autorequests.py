import json
import time
import re
import threading
import queue
import configparser
from requests import Session
from datetime import datetime
from .tools import *
from typing import *
from lxml import html
from .tools.expections import UnsuccessfulRequestError
import importlib.resources as pkg_resources

class AutoRequests:
    thread_lock = threading.Lock()
    shared_queue = queue.Queue()
    threads = []
    """
    AutoRequests Class
    ==================

    The `AutoRequests` class automates the process of sending HTTP requests to a list of websites defined in a configuration file. It supports multi-threading to handle multiple requests concurrently and includes functionality for customizing headers, cookies, request methods, and payloads.

    Attributes
    ----------
    thread_lock : threading.Lock
        A lock object to synchronize threads.
    shared_queue : queue.Queue
        A thread-safe queue that stores (cpn, website) tuples to be processed by threads.
    threads : list
        A list of threads initialized to process the queue.
    websites : list
        A list of websites to which requests will be sent, loaded from a configuration file.
    max_threads : int
        The maximum number of threads to run concurrently, defined in the configuration file.

    Methods
    -------
    __init__(test=None)
        Initializes the class by loading the configuration and setting up threads. Optionally, a test configuration can be loaded.
        
    navigate_and_init_requests(layers, cpn)
        Navigates through the layers of a website configuration, sends requests, and processes responses.
        
    __send_request(url, headers, cookies, method, data, data_type)
        Sends an HTTP request using the specified parameters and returns the response.
        
    __init_threads()
        Initializes the worker threads for handling requests.
        
    __initialize_session()
        Initializes a new HTTP session.
        
    __before_request(field_info, cpn) -> tuple[dict, str, str]
        Prepares the request headers, cookies, method, and data based on the configuration.
        
    __after_request(response, field, cpn)
        Processes the response to collect data using regex and XPath, and updates the `cpn` dictionary.
        
    __success_checking(response, layer)
        Checks if the response satisfies all the success criteria defined in the layer configuration.
        
    __collect_token(response, regex)
        Extracts data from the response using a regular expression.
        
    __collect_query(response, query)
        Extracts data from the response using an XPath query.
        
    __configure_cookies(response, cookies)
        (TODO) Sets up cookies based on the response. Not yet implemented.
    
    __configure_proxy(session, proxy)
        (TODO) Sets up a proxy connection before making requests. Not implemented yet
        
    register(cpn, website)
        Processes the request workflow for a single website, updating the `cpn` dictionary with collected data.
        
    run()
        Continuously processes items in the queue by sending requests and handling responses.
        
    enqueue_data(cpn)
        Enqueues `cpn` data for all websites in the configuration, triggering the request process.
        

    Usage
    -----
    To use the `AutoRequests` class, initialize it and enqueue data to start processing:

        auto_filler = AutoRequests()
        auto_filler.enqueue_data(cpn_data)
        auto_filler.shared_queue.join()

    TODO
    ----
    - Implement the `__configure_cookies` method to handle cookie setup based on the response.
    - Implement the `__configure_proxy` method to handle HTTP proxy connections and rotations.
    """
    def __init__(self,test = None):
        with pkg_resources.open_text('autorequests.data', 'requests.json') as f:
            config_ = json.load(f)
            check_obligation(config_,"requests")
            self.websites = config_["websites"]
        if test:
            with open(f"{test}") as f:
                config_ = json.load(f)
                check_obligation(config_,"requests")
                self.websites = config_["websites"]
        config = configparser.ConfigParser()
        with pkg_resources.open_text('autorequests.data', 'config.ini') as f:
            config.read_file(f)
        self.max_threads = int(config["requests"]["max_threads"])
        self.__init_threads()


    def navigate_and_init_requests(self,layers,cpn):
        for layer in layers:
            print(cpn)
            url = layer.get("url")
            headers,cookies,method,data = self.__before_request(layer,cpn)
            data_type = layer["data"]["type"]
            response:Session = self.__send_request(url, headers, cookies, method, data, data_type)
            if not self.__success_checking(response,layer):
                raise UnsuccessfulRequestError()
            cpn = self.__after_request(response,layer,cpn)


    def __send_request(self, url: str, headers: dict, cookies: dict, method: str, data: Any, data_type: str) -> Session:
        session = self.__initialize_session()
        response = None
        if method == "post":
            if data_type == "json":
                response = session.post(url, json=data, headers=headers)
            else:
                response = session.post(url, data=data, headers=headers)
        elif method == "get":
            response = session.get(url, headers=headers, cookies=cookies)
        return response

    def __init_threads(self):
        for _ in range(self.max_threads):
            thread = threading.Thread(target=self.run)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def __initialize_session(self):
        session = Session()
        return session

    def __before_request(self,field_info,cpn) -> tuple[dict,str,str]:
        headers = HEADERS if field_info["headers"]["type"].upper() == "DEFAULT" else field_info["headers"]["headers"]
        cookies = {} if not field_info["cookies"]["static_status"] else field_info["cookies"]["static"]
        method  = method_configuration(field_info.get("method"))
        data = recursive_data_render(field_info["data"]["actual_data"],cpn)
        return headers,cookies,method,data

    def __after_request(self,response,field,cpn):
        # collecting data from response 
        regex = {}
        xpath = {}
        if field.get("collection_regex"):
            for expression in field["collection_regex"]: regex[expression["variable"]] = self.__collect_token(response,regex = expression["regex"]) 

        if field.get("collection_xpath"):
            for query in field["collection_xpath"]: xpath[query["variable"]] = self.__collect_query(response,query)

        for key,value in xpath:
            cpn[key] = value

        for key,value in regex:
            cpn[key] = value

        if field.get("sleep"):
            time.sleep(int(field["sleep"]))
        return cpn
    def __success_checking(self,response:Session,layer:dict):
        return all([success_output(response,item) for item in layer["success_request"].items()])

    def __collect_token(self,response:Session,regex:dict):
        text = response.text
        pattern = regex["regex"]
        matches = re.search(pattern,text)
        return matches.group() if matches else ""

    def __collect_query(self,response:Session,query:dict):
        text = response.text
        tree = html.fromstring(text)
        result = tree.xpath(query)
        return result[0] if len(result) > 0 else ""


    def __configure_cookies(self,response:Session,cookies:dict):
        pass
    
    def __configure_proxy(self,session:Session,proxy):
        pass

    def register(self, cpn:dict, website:dict):
        self.navigate_and_init_requests(website["layers"], cpn)

    def run(self):
        while True:
            if not self.shared_queue.empty():
                cpn, website = self.shared_queue.get()
                successful = self.register(cpn, website)
                print(f"Request {'succeeded' if successful else 'failed'} for {website['url']}")
                self.shared_queue.task_done()

    def enqueue_data(self, cpn):
        """
        Enqueues `cpn` data for all websites in the configuration, triggering the request process.
        Parameters
        ----------
            cpn (dict) : a dictionary, keys should be variables in config and values should be either str or int (input) 
        """
        for website in self.websites:
            self.shared_queue.put((cpn, website))

if __name__ == "__main__":
    auto_filler = AutoRequests()
    cpn_data = {
        "Firstname": "John",
        "Lastname": "Doe",
        "Gender": "Male",
        "Birthday": "01/01/1980"
    }

    # Enqueue data
    auto_filler.enqueue_data(cpn_data)
    auto_filler.shared_queue.join()
