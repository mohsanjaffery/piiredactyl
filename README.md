# Piiredactyl

Piiredactyl lets users redact PII in logs for Cloudtrail and other AWS services.  It is a turnkey solution that can be deployed in a Users AWS account.  

The solution uses AWS Glue to crawl, classify and then process logs, replacing sensitive PII data as per a Users requirements.

## Installation

Deploy the provided [Cloudformation Template](https://pip.pypa.io/en/stable/) to install Piiredactyl.

```bash
aws <command> <subcommand>
```

## Usage

```bash
aws <command> <subcommand>
```

```python
python <script>
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)


## Hacky install

Copy nested templates to cfn-repo

```bash
aws s3 cp piiredactyl-platform.json   s3://builder-cfn-templates/templates/dev/000/piiredactyl-platform.json
aws s3 cp piiredactyl-glue.json   s3://builder-cfn-templates/templates/dev/000/piiredactyl-glue.json
```

Copy scripts to cfn-repo

```bash
aws s3 cp piiredactyl.py   s3://builder-cfn-templates/scripts/dev/000/piiredactyl.py
```

Launch main CFN template

```bash
aws cloudformation create-stack --capabilities CAPABILITY_NAMED_IAM --stack-name piiredactyl --template-body file://piiredactyl-main.json
```

Copy Sample Log data into Ingest bucket. Obtain bucket name with the following

```bash
aws cloudformation describe-stacks --stack-name piiredactyl |jq '.Stacks[].Outputs[]|select(.OutputKey=="IngestDataBucket")|.OutputValue'
```

Run Glue crawler

```bash
aws <command> <subcommand>
```

Run Glue script

```bash
aws <command> <subcommand>
```

Observe transformed log in Transform bucket.  Obtain bucket name with the following

```bash
aws cloudformation describe-stacks --stack-name piiredactyl |jq '.Stacks[].Outputs[]|select(.OutputKey=="TransformDataBucket")|.OutputValue'
```
