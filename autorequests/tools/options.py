from .constant import REQUESTS_OBLIGATED
from .expections import *

def method_configuration(method):
    method_dict = {
        "OPTION":"option",
        "GET":"get",
        "POST":"post",
        "DELETE":"delete"
    }
    return method_dict[method] if method_dict.get(method) else "get"

def recursive_data_render(request_data:dict,cpn:dict):
    for key,value in request_data.items():
        value_type = type(value)
        if value_type == dict:
            request_data[key] = recursive_data_render(value,cpn)
        elif value_type == str:
            key,value = key.format(**cpn),value.format(**cpn)


def success_output(response,input_query = ("success_code",200)):
    if input_query[0] == "success_code":
        return response.status_code == input_query[1]
    elif input_query[0] == "sucess_value":
        return input_query[0] in response.text
    
def recursive_obligation_checking(config: dict, obligation: dict):
    for key, values_list in obligation.items():
        config_part = config.get(key)
        
        if not config_part:
            raise BadConfigError(path=key, keys=(key,))
        
        if isinstance(config_part, list):
            for part_index, part in enumerate(config_part):
                for value in values_list:
                    if isinstance(value, tuple):
                        # Handling tuple with 2 or more elements
                        sub_config = part.get(value[0])
                        if sub_config is None:
                            raise BadConfigError(path=key, keys=(part_index, value[0]))

                        if len(value) > 1:
                            if sub_config.get(value[1]) is None:
                                raise BadConfigError(path=key, keys=(part_index, value[0], value[1]))
                    elif isinstance(value, dict):
                        recursive_obligation_checking(config=part, obligation=value)
        else:
            raise BadConfigError(path=key, keys=(key,))

def check_obligation(config:dict,script:str):
    if not config.get("websites"):
        raise BadConfigError(keys= ("website"))
    websites = config.get("websites")
    obligations = REQUESTS_OBLIGATED
    for obligation in obligations:
        recursive_obligation_checking(config,obligation)