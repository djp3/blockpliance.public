#!/bin/bash
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
#

#Check for command-line commands
for cmd in curl jq; do
    command -v $cmd >/dev/null 2>&1 || { echo >&2 "I require $cmd but it's not installed. Aborting."; exit 1; }
done

# File containing the initial authentication payload.
AUTH_PAYLOAD="user-data.json"

# File containing the refresh token payload template.
REFRESH_PAYLOAD_TEMPLATE="user-token-refresh.json.template"
REFRESH_PAYLOAD="user-token-refresh.json"

# Cognito endpoint
COGNITO_ENDPOINT="https://cognito-idp.us-east-1.amazonaws.com/"

# Authenticate and acquire tokens
if ! AUTH_RESULT=$(curl -s -X POST --data @"$AUTH_PAYLOAD" -H 'X-Amz-Target: AWSCognitoIdentityProviderService.InitiateAuth' -H 'Content-Type: application/x-amz-json-1.1' $COGNITO_ENDPOINT);  then
	echo "Error: Authentication request failed"
	exit 1
fi

#Save result for inspection
echo "$AUTH_RESULT" | jq -r > result.json

# Extract access and refresh tokens
ACCESS_TOKEN=$(echo "$AUTH_RESULT" | jq -r .AuthenticationResult.AccessToken)
REFRESH_TOKEN=$(echo "$AUTH_RESULT" | jq -r .AuthenticationResult.RefreshToken)

#identify btc addresses you are interested in querying for the grade endpoint
declare -a hashs=( 1FfmbHfnpaZjKFvyi1okTjJJusN455paPH/BTC 12cbQLTFMXRnSzktFkuoG3eHoMeFtpTu3S/BTC )

#identify any crypto addresses you are interested in querying for the beta endpoint
#declare -a hashs=( 12cbQLTFMXRnSzktFkuoG3eHoMeFtpTu3S/BTC 0x001cf27131e91371038e808e00f951197356c663/ETH 0x002026372b31817899d414a0f226b8b500136f5f/ETH 0x00271ba71c16cb0fdf532570091341665d147350/ETH )

#query each in turn and store in output file for inspection
for i in "${hashs[@]}"; do
    filename=$(echo "$i" | tr '/' '_')
	echo -n "$i,";
    curl -s -X GET -H "Authorization: Bearer $ACCESS_TOKEN" "https://api.blockpliance.com/v1/grade/$i" | tee "${filename}.output" | jq .;
    #curl -s -X GET -H "Authorization: Bearer $ACCESS_TOKEN" "https://api.blockpliance.com/v1/beta/$i" | tee "${filename}.output" | jq .;
done

# Prepare the refresh token payload by replacing the placeholder in the template
cp $REFRESH_PAYLOAD_TEMPLATE $REFRESH_PAYLOAD
sed -i '' "s/foo/$REFRESH_TOKEN/g" $REFRESH_PAYLOAD

# Attempt to refresh the tokens
REFRESH_RESULT=$(curl -s -X POST --data @$REFRESH_PAYLOAD -H 'X-Amz-Target: AWSCognitoIdentityProviderService.InitiateAuth' -H 'Content-Type: application/x-amz-json-1.1' $COGNITO_ENDPOINT)

# Output the result of the token refresh attempt
echo "Refresh result:"
echo "$REFRESH_RESULT" | jq -r .
