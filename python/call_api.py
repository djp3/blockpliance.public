# Original author: Don Patterson, CTO Blockpliance
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import requests
import json
import logging
from os import environ
from typing import Dict

# Contains secrets brought in from environment variables
class Settings:
    AWS_REGION = None
    AWS_APP_CLIENT_ID = None
    AWS_USERNAME = None
    AWS_PASSWORD = None
    AWS_TOKENS = {}
 
    BASE_URL = "https://api.blockpliance.com/v1/"
    ENDPOINT_MAPPING = {
        "ofac_check": "ofac_check",
        "risk_attributes": "risk_attributes",
        "risk_analysis": "risk_analysis"
    }


    def __str__(self):
        return (f"Settings(\n\tAWS_REGION={self.AWS_REGION}, "
                f"\n\tAWS_APP_CLIENT_ID={self.AWS_APP_CLIENT_ID}, "
                f"\n\tAWS_USERNAME={self.AWS_USERNAME}, "
                f"\n\tAWS_PASSWORD={'******' if self.AWS_PASSWORD else None}, "
                f"\n\tAWS_TOKENS={'Present' if self.AWS_TOKENS else 'Empty'})")


def get_cognito_tokens(aws_region, client_id, username, password):
    """
    Authenticate with Amazon Cognito and acquire ID and access tokens.

    Parameters:
    - aws_region: The AWS region for Cognito services.
    - client_id: Cognito App Client ID (without client secret)
    - username: The username of the Cognito user
    - password: The password of the Cognito user

    Returns:
    A dictionary with ID and Access tokens, or error information.
    """
    try:
        # Cognito token endpoint
        url = f'https://cognito-idp.{aws_region}.amazonaws.com/'

        # Headers
        headers = {
            'Content-Type': 'application/x-amz-json-1.1',
            'X-Amz-Target': 'AWSCognitoIdentityProviderService.InitiateAuth'
        }

        # Authentication parameters
        auth_parameters = {
            'AuthFlow': 'USER_PASSWORD_AUTH',
            'ClientId': client_id,
            'AuthParameters': {
                'USERNAME': username,
                'PASSWORD': password
            }
        }

        response = requests.post(url, headers=headers, data=json.dumps(auth_parameters))
        response.raise_for_status()

        # Parse the JSON response
        tokens = response.json().get('AuthenticationResult',{})

        # Extract ID and Access Tokens
        return {
            'id_token': tokens.get('IdToken'),
            'access_token': tokens.get('AccessToken'),
            'refresh_token': tokens.get('RefreshToken')
        }
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return {'error': str(e)}    



def refresh_cognito_tokens(aws_region, client_id, refresh_token):
    """
    Refresh Cognito ID and access tokens using a refresh token.

    Parameters:
    - aws_region: The AWS region of your Cognito User Pool.
    - client_id: The client ID of your Cognito app client.
    - refresh_token: The refresh token received during the initial authentication.

    Returns:
    A dictionary with the new ID and Access tokens, or error information.
    """
    # Construct the URL for token refresh
    url = f'https://cognito-idp.{aws_region}.amazonaws.com/'

    # Headers for the request
    headers = {
        'Content-Type': 'application/x-amz-json-1.1',
        'X-Amz-Target': 'AWSCognitoIdentityProviderService.InitiateAuth'
    }

    # Payload for refreshing tokens
    payload = {
        'ClientId': client_id,
        'AuthFlow': 'REFRESH_TOKEN_AUTH',
        'AuthParameters': {
            'REFRESH_TOKEN': refresh_token
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        # Parse the JSON response to extract the new tokens
        tokens = response.json().get('AuthenticationResult', {})
        return {
            'id_token': tokens.get('IdToken', 'No ID token returned'),
            'access_token': tokens.get('AccessToken', 'No access token returned'),
            'expires_in': tokens.get('ExpiresIn', 'No expiry time returned')
        }
    else:
        # Return error information if the refresh was unsuccessful
        return {'error': response.text, 'StatusCode': response.status_code}


# Standard call to the bitcoin risk assessment endpoint: 
#        json_response = query_api("1FfmbHfnpaZjKFvyi1okTjJJusN455paPH")
#           or
#        json_response = query_api("1FfmbHfnpaZjKFvyi1okTjJJusN455paPH","ofac_check")
#

def query_api(crypto_address: str, end_point: str = "ofac_check") -> Dict:
    # Check if the access token exists
    access_token = settings.AWS_TOKENS.get("access_token")
    if not access_token:
        return {"error": "Access token is missing"}

    # Get the endpoint path from the mapping
    endpoint_path = settings.ENDPOINT_MAPPING.get(end_point)
    if not endpoint_path:
        return {"error": "Invalid endpoint"}

    # Construct the URL
    url = f"{settings.BASE_URL}{endpoint_path}/{crypto_address}"

    # Set up the headers
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        # Make the GET request
        response = requests.get(url, headers=headers, timeout=60)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()  # Returns the JSON response from the API
        else:
            return {"error": "Failed to retrieve data", "status_code": response.status_code}

    except requests.RequestException as e:
        return {"error": str(e)}

 
 
def main():
    # Get secrets from environment variables
    settings.AWS_REGION = environ.get('AWS_REGION')
    settings.AWS_APP_CLIENT_ID = environ.get('AWS_APP_CLIENT_ID')
    settings.AWS_USERNAME = environ.get('AWS_USERNAME')
    settings.AWS_PASSWORD = environ.get('AWS_PASSWORD')

    # Get tokens from AWS Cognito
    tokens = get_cognito_tokens(settings.AWS_REGION, settings.AWS_APP_CLIENT_ID, settings.AWS_USERNAME, settings.AWS_PASSWORD)
    if 'error' in tokens:
        logging.error("Authentication failed: %s", tokens['error'])
        return  # Exit if authentication fails

    settings.AWS_TOKENS = tokens
    logging.info("Successfully authenticated with Cognito.\n%s",settings)

    # Example of querying AWS with two different crypto addresses
    crypto_addresses = ["1FfmbHfnpaZjKFvyi1okTjJJusN455paPH", "12cbQLTFMXRnSzktFkuoG3eHoMeFtpTu3S"]
    for address in crypto_addresses:
        json_response = query_api(address)
        # or
        #  json_response = query_api(address,"ofac_check")
        #  json_response = query_api(address,"risk_attributes")
        #  json_response = query_api(address,"risk_analysis")
        if 'error' in json_response:
            logging.error("Failed to retrieve data for %s:\n%s", address, json.dumps(json_response['error']))
        else:
            logging.info("Data retrieved for %s:\n%s", address, json.dumps(json_response, indent=4))

    # Refresh tokens to demonstrate how to do it
    tokens = refresh_cognito_tokens(settings.AWS_REGION,
                                    settings.AWS_APP_CLIENT_ID,
                                    settings.AWS_TOKENS['refresh_token'])
    if 'error' in tokens:
        logging.error("Authentication failed: %s", tokens['error'])
        return  # Exit if authentication fails

    settings.AWS_TOKENS['id_token'] = tokens['id_token']
    settings.AWS_TOKENS['access_token'] = tokens['access_token']
    settings.AWS_TOKENS['expires_in'] = tokens['expires_in']
    logging.info("Successfully refreshed tokens with Cognito.\n%s",settings)

if __name__ == "__main__":
    # Set up basic configuration for logging
    logging.basicConfig(level=logging.INFO)

    # Set up settings
    settings = Settings();

    # Launch
    main()
