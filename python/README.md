# python
* Obtain credentials from Blockpliance (sales@blockpliance.com)
* Create a python environment
  * ```python -v venv api_env```
* Activate the environment
  * ```source api_env/bin/activate```
* Install dependencies
  * ```pip install -r requirements.txt```
* Review the code in ```call_api.py```
  * Optionally change the addresses to query
* Execute the code with environment variables holding the credentials
  * ```AWS_REGION='<region>' AWS_USERNAME='<username>' AWS_PASSWORD='<password>' AWS_APP_CLIENT_ID='<client_id>' python ./call_api.py```
* Deactivate the environment
  * ```deactivate```

