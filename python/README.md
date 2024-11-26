# python
* Obtain credentials from our friendly team [https://calendly.com/blockpliance/personalized-intro](https://calendly.com/blockpliance/personalized-intro]).
* Create a python environment
  * ```python -m venv api_env```
* Activate the environment
  * ```source api_env/bin/activate```
* Install dependencies
  * ```pip install -r requirements.txt```
* Review the code in ```call_api.py```
  * No changes are typically necessary
* Execute the code with environment variables holding the credentials
  * ```python ./call_api.py -h```
  * ```BLOCKPLIANCE_USERNAME='<username>' BLOCKPLIANCE_PASSWORD='<password>' python ./call_api.py <method> <address> <address>```
     * For example:
     * ```BLOCKPLIANCE_USERNAME='my-blockpliance-account@blockchain.com' BLOCKPLIANCE_PASSWORD='my-blockpliance-password' python ./call_api.py ofac_check 1FfmbHfnpaZjKFvyi1okTjJJusN455paPH```
     * ```BLOCKPLIANCE_USERNAME='my-blockpliance-account@blockchain.com' BLOCKPLIANCE_PASSWORD='my-blockpliance-password' python ./call_api.py risk_attributes 12cbQLTFMXRnSzktFkuoG3eHoMeFtpTu3S```
     * ```BLOCKPLIANCE_USERNAME='my-blockpliance-account@blockchain.com' BLOCKPLIANCE_PASSWORD='my-blockpliance-password' python ./call_api.py risk_analysis 1HQ3Go3ggs8pFnXuHVHRytPCq5fGG8Hbhx 1Fz29BQp82pE3vXXcsZoMNQ3KSHfMzfMe3```
     
* Deactivate the environment
  * ```deactivate```

