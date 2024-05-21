<div style="float: right; margin-left: 20px;">
  <img src="https://assets-global.website-files.com/64fc9d87825785416c12539b/65b97d05b11bebdb3cf6c7c5_Screenshot%202024-01-30%20at%2014.45.22-p-500.png" alt="Blockpliance Risk Cards A through F" width="200" align="right"/>
</div>

![Blockpliance Sticker Logo](https://assets-global.website-files.com/64fc9d87825785416c12539b/64fcb20e15ed201d5bac2906_blockpliance_stickers-2%225-p-500.png)
# API and Developer Documentation

Welcome to the Blockpliance API documentation. This guide will help you understand how to integrate and utilize our API to leverage Blockpliance's Artificial Intelligence and Machine Learning driven compliance features in your applications.

## Table of Contents



1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Authentication](#authentication)
4. [API Endpoints](#api-endpoints)
   - [Bitcoin Risk Assessment](#bitcoin-risk-assessment)
   - [Multi-currency Risk Assessment (Beta)](#multi-currency-risk-assessment)
5. [Request and Response Formats](#request-and-response-formats)
6. [Error Handling](#error-handling)
7. [Code Examples](#code-examples)
   - [Bash](#bash)
   - [Python](#python)
8. [Best Practices](#best-practices)
9. [FAQ](#faq)
10. [Support and Feedback](#support-and-feedback)

## Introduction

Blockpliance is a leading blockchain compliance platform that offers a comprehensive suite of tools and services to ensure regulatory compliance for blockchain-based projects. Our API allows developers to seamlessly integrate Blockpliance's functionalities into their applications.  

We are a fast moving start-up company, so if you don't see what you like, reach
out to [us](mailto:djp3@blockpliance.com) to see if we can change our endpoint for your needs.

## Getting Started

To get started with the Blockpliance API, follow these steps:

1. Sign up for a Blockpliance account with our friendly team [https://calendly.com/blockpliance/personalized-intro] (https://calendly.com/blockpliance/personalized-intro]).
2. Review the code in this repo to understand how to obtain credentials.
3. Review the API documentation to understand the available endpoints and their usage.

## Authentication

All API requests require authentication using AWS Cognito. 

For example using the bash command-line:
```
# Authenticate and acquire tokens
if ! AUTH_RESULT=$(curl -s -X POST --data @"$AUTH_PAYLOAD" -H 'X-Amz-Target: AWSCognitoIdentityProviderService.InitiateAuth' -H 'Content-Type: application/x-amz-json-1.1' $COGNITO_ENDPOINT);  then
	echo "Error: Authentication request failed"
	exit 1
fi

# Extract access and refresh tokens
ACCESS_TOKEN=$(echo "$AUTH_RESULT" | jq -r .AuthenticationResult.AccessToken)
REFRESH_TOKEN=$(echo "$AUTH_RESULT" | jq -r .AuthenticationResult.RefreshToken)
```

## API Endpoints

### Bitcoin Risk Assessment

Request a risk assessment for a bitcoin address

```
https://api.blockpliance.com/v1/grade/<address hash>/BTC
```

JSON Response:
```{
	"version": "1.1",
	"errors": [<array of strings, empty if no errors>],
	"warnings": [<array of warnings, empty if no warnings>],
	"result": {
		"grade": {
			"letter": <string drawn from "A+","A","A-","B+","B","B-","C+","C","C-","D+","D","D-","F">,
			"ordinal": <integer drawn from [0:11]>
		},
		"risk_categories": [<array of strings describing the rationale for the grade>],
		"computed_on": {
			"date_time": "<string in  "yyyy:MM:dd:HH:mm:ss:z" format>",
			"millis": <long, millis since epoch>
		},
	}
}
```

For example:
```
{
	"version": "1.1",
	"errors": [],
	"warnings": [],
	"result": {
		"grade": {
			"letter": "F",
			"ordinal": 11
		},
		"risk_categories": ["OFAC", "Dark Web"],
		"computed_on": {
			"date_time": "2023:03:30:19:19:01:UTC",
			"millis": 1680202854689
		},
	}
}
```

### Endpoint 2 : multi-currency risk assessment (beta)

Request a risk assessment for a cryptocurrency address in one of the following
currencies:
| Common Name | API Abbreviation |
| ----------- | ---------------- |
| Arbitrum | ARB |
|     Bitcoin Cash | BCH |
|     Binance Smart Chain | BSC |
|     Bitcoin SV | BSV |
|     Bitcoin | BTC |
|     Bitcoin Gold | BTG |
|     Celo | CELO |
|     Dash | DASH |
|     Ethereum Classic | ETC |
|     Ethereum | ETH |
|     Litecoin | LTC |
|     Tron | TRX |
|     USD Coin | USDC |
|     Tether | USDT |
|     USDT on Ethereum | USDT_ON_ETH | 
| USDT on Tron | USDT_ON_TRON |
|     Monero | XMR |
|     Ripple | XRP |
|     Verge | XVG |
|     Zcash | ZEC |

```
https://api.blockpliance.com/v1/beta/<address hash>/<API Abbreviation>
```

JSON Response:
```{
	"version": "1.1",
	"errors": [<array of strings, empty if no errors>],
	"warnings": [<array of warnings, empty if no warnings>],
	"result": {
		"grade": {
			"letter": <string drawn from "A+","A","A-","B+","B","B-","C+","C","C-","D+","D","D-","F">,
			"ordinal": <integer drawn from [0:11]>
		},
		"risk_categories": [<array of strings describing the rationale for the grade>],
		"computed_on": {
			"date_time": "<string in  "yyyy:MM:dd:HH:mm:ss:z" format>",
			"millis": <long, millis since epoch>
		},
	}
}
```

For example:
```
https://api.blockpliance.com/v1/beta/0x00271ba71c16cb0fdf532570091341665d147350/ETH

{
  "version": "1.1",
  "errors": [],
  "warnings": [],
  "result": {
    "grade": {
      "letter": "F",
      "ordinal": 12
    },
    "risk_categories": [ "Darknet Market" ],
    "computed_on": {
      "date_time": "2024:05:21:21:43:51:UTC",
      "millis": 1716327831264
    }
  }
}

```

## Request and Response Formats

All information is passed in the URL as an https GET method.
The Blockpliance API returns data in JSON format.

## Error Handling

In case of any errors, the API will return an appropriate HTTP status code and/or an error message in the response body.

## Code Examples

### Bash
* [bash example](./bash)

### Python
* [python example](./python)

## Best Practices

- We enforce HTTPS for all API requests to ensure secure communication. 
- Consider how to gracefully handle errors, including timeout errors for network problems.
- Keep your AWS credentials secure to avoid unauthorized parties charging your account.

## FAQ

1. **How can I get more help** Contact djp3@blockpliance.com

## Support and Feedback

If you have any questions, issues, or feedback regarding the Blockpliance API, please contact our support team at [djp3@blockpliance.com](mailto:djp3@blockpliance.com). We are here to assist you and ensure a smooth integration experience.
