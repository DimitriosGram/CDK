# FROM public.ecr.aws/lambda/python:3.11
FROM python:3.11-slim

# Install the function's dependencies using file requirements.txt
# from your project folder.

# WORKDIR /
COPY requirements.txt  .
RUN  pip install -r requirements.txt

# Copy function code
COPY . ./

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
ENTRYPOINT [ "./src/lambdas/x.handler" ] 