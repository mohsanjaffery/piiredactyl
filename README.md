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
