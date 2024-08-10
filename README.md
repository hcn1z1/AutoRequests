# AutoRequests

**AutoRequests** is a powerful Python library designed to automate the process of sending HTTP requests based on a configuration file. It is particularly useful for scenarios where you need to interact with multiple websites concurrently, extract tokens like cookies and hidden form tokens, and customize request parameters such as headers, cookies, proxies, and mor

## Features
- Multi-Threading: Execute HTTP requests across multiple websites simultaneously, improving efficiency and performance.
- Token Grabbing: Automatically extract and handle tokens, cookies, and other dynamic elements required for successful requests.
- Customizable Requests: Easily customize headers, cookies, proxies, and other parameters to suit your specific needs.
- Configuration-Driven: Define all your request flows in a configuration file, reducing the need for repetitive coding.
- Extensible: The library is designed to be extensible, allowing developers to add or modify functionality as required.

## Installation

You can install AutoRequests directly from GitHub using pip:

```bash
pip install git+https://github.com/hcn1z1/AutoRequests
```

## Requirements
- Python 3.7>=
- requests library
- lxml library
- configparser library

## Usage

### Basic Example

To start using **AutoRequests**, you need to create a configuration file that defines the websites and their respective request flows. Here’s a basic example:

```json
{
    "websites": [{
        "name": "USTHB.dz",
        "layers": [
            {
                "url": "https://ent.usthb.dz/index.php/accueil",
                "method": "POST",
                "success_request": {
                    "success_code": 200
                },
                "headers": {
                    "type": "DEFAULT"
                },
                "data": {
                    "type": "urlencode",
                    "actual_data": {}
                },
                "cookies": {
                    "static_status": false
                }
            }
        ]
    }]
}

```

### Running AutoRequests

Once you have your configuration file ready, you can start sending requests by initializing and running the AutoRequests class:
```python
from autorequests import AutoRequests

cpn_data = {
    "Firstname": "John",
    "Lastname": "Doe",
    "Email": "john.doe@example.com"
}

auto_filler = AutoRequests(test = "config.json")
auto_filler.enqueue_data(cpn_data)
auto_filler.shared_queue.join()

```
## Advanced Features
AutoRequests can automatically extract tokens (such as CSRF tokens or session cookies) using regex or XPath queries. This is particularly useful for interacting with web forms or APIs that require dynamic tokens.

### Advance Example

In this advanced scenario, you can utilize multiple variables within your configuration file to create more complex and dynamic web scraping operations.

Let's take for example the next input dictionary

```python
cpn_data = {
    "Firstname": "John",
    "Lastname": "Doe",
    "Email": "john.doe@example.com"
}
```

These variables can be incorporated into your configuration file as follows:

```json
{
    "websites": [{
        "name": "USTHB.dz",
        "layers": [
            {
                "url": "https://ent.usthb.dz/index.php/accueil",
                "method": "POST",
                "success_request": {
                    "success_code": 200
                },
                "headers": {
                    "type": "DEFAULT"
                },
                "data": {
                    "type": "urlencode",
                    "actual_data": {
                        "informations":{
                            "email":"{Email}"
                        },
                        "coordination":{
                            "fname":"{Firstname}",
                            "lname":"{Lastname}"
                        }
                    }
                },
                "cookies": {
                    "static_status": false
                }
            }
        ]
    }]
}

```

In this example, the variables {Email}, {Firstname}, and {Lastname} are dynamically inserted into the request data, making the process more adaptable to different inputs.

**Using Regex Variables in Subsequent Requests**

You can also capture values using regex in one layer and use them in subsequent requests. Here's how you can achieve that:

```json
{
    "websites": [{
        "name": "USTHB.dz",
        "layers": [
            {
                "url": "https://ent.usthb.dz/index.php/accueil",
                "method": "POST",
                "success_request": {
                    "success_code": 200
                },
                "collection_regex":[{
                    "regex":"\\d+",
                    "variable":"number"
                }],
                "headers": {
                    "type": "DEFAULT"
                },
                "data": {
                    "type": "urlencode",
                    "actual_data": {
                        "informations":{
                            "email":"{Email}"
                        },
                        "coordination":{
                            "fname":"{Firstname}",
                            "lname":"{Lastname}"
                        }
                    }
                },
                "cookies": {
                    "static_status": false
                }
            },
            {
                "url": "https://ent.usthb.dz/index.php/profile",
                "method": "POST",
                "success_request": {
                    "success_code": 200
                },
                "headers": {
                    "type": "DEFAULT"
                },
                "data": {
                    "type": "urlencode",
                    "actual_data": {
                        "informations":{
                            "email":"{Email}",
                            "number":"{number}"
                        }
                    }
                },
                "cookies": {
                    "static_status": false
                }
                
            }
        ]
    }]
}

```

In this configuration:

- The first layer sends a request to ``accueil`` URL to capture a numerical value from the response using the regex pattern (``\\d+``) and stores it in a new variable ``{number}``
- In the second layer, a request to ```profile`` is sent along with the new variable ``{number}`` alongside the original ``{Email}``.

This approach enables you to create a more dynamic workflow passing data between requests. This'll make the scrapping process smoother and flexible.


## Contribution
Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.
