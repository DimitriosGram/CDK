## Overview

(title)

## Architecture

![Architecture Diagram]()

<details>
<summary>How to generate a 'live' link to LucidCharts</summary>
<ul>
<li>Click file</li>
<li>Click publish</li>
<li>Select Single Page (PDF / Image)</li>
<ul><li>Select PNG</li></ul>
</details>

### Estimated costs

Total (per month): $0.00
- S3: $0.0.
- Lambda: $0.00
- Cloudwatch: $0.00
- SNS: $0.00
- etc.

Assumptions made that impact cost estimates:

<i>(list them here)</i>
Executions of lambda per day: ???
Size of file written to S3: ???


## Background

...


## Executing the program

### Schedule
Every month on ??? @ ???

### Manual execution
* Step-by-step bullets

1. Login to AWS
2. Go to the Lambda Services page and find the Lambda in question
    - It is easier to go via the CloudFormation stack to locate the Lambda
3. Make a note of the Lambda name
4. Execute the following code in the AWS CLI:

```
aws lambda invoke --function-name <my-function> --paylod '{"REGION": "eu-west-2", "BUCKET_NAME": <bucket_name>, "BRANCH": <dev or prod>, "REPORTING_MONTH": "None"}' response.json
```
Payload variables i.e. Context Variables
> BUCKET_NAME: get the bucket name from the cloudformation stack
> <br>BRANCH: dev or prod
> <br>REPORTING_MONTH: YYYYMM e.g. 202403


## Improvements
1. Check naming of resources i.e. are they being double named
2. Create an Image for this Lambda
3. etc.
 

## Troubleshooting
* Step-by-step bullets
```
code blocks for commands
```





