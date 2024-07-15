# README #

<!-- This README would normally document whatever steps are necessary to get your application up and running. -->

### What is this repository for? ###

* .... put a brief description ...

### Setting up CDK for the first time
- Install NPM if you don't have
- Install the following (Windows)
- Install cdk toolkit
```
npm install -g aws-cdk
npx -p aws-cdk
```
- Check it is installed 
```
cdk --version 
npx cdk --version
```
- If you need to setup a new project, run the following `cdk init app --language python`

### To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add them to your `setup.py` file and rerun the `pip install -r requirements.txt` command.

### How do I get set up? ###

* clone the repo `git clone` or using ssh
* install requirements `pip install -r requirements-dev.txt`
* install commit-linter `commit-linter install`
* install git hooks `pre-commit install`
* test you can build aws resources templates `cdk synth`
* run the tests
```
    pytest -v tests/ --junitxml=test-reports/report.xml
    pytest -v aws/tests/ --junitxml=test-reports/report.xml
```
* To run individual test scripts or tests, use the following code
```
pytest <test_path> -vv -k '<test_name>' -s
```

> **What do the flags mean?**
>> `-v` verbos of output (add more `v`'s for more verbosity)
> >
>> `-k` specify a test
>>
>> `-s` output the print or logging statements to the console


* run either one of the test coverage commands to generate a report (locally)
```
pytest --cov
pytest --cov --cov-report=html
pytest --cov --junitxml=test_reports/coverage_report.xml
```

### Contribution guidelines ###

* Writing unit tests
  * Test single functions
  * One assertion per test
  * Keep data fixtures in line
  * Test happy path
  * Test error handling
  * Test any known edge cases
  * Add messages to tests that describe the edge cases
  * For any known defects add a test that fails that exemplify the defect
* Writing integration tests
  * Link functionality to reflect code execution
  * Provide plain in line input
  * Define in line expected output
  * Test that input produces desired output
  * For any known defects add a test that fails that exemplify the defect
* Code review:
  * only the stated feature should be in the code change
  * any new feature or change should have a unit test
  * pipeline run should be green
  * pipeline run should not do changes to code(formatting)
* Other guidelines

### Who do I talk to? ###

* Anyone in the Data Platform Team