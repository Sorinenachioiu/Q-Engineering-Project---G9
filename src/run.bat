@echo off

REM Build the Docker image
docker build -t q_eng_proj .

REM Run the Docker container and map the output folder to ./circuits
docker run --rm -it -v "%cd%/circuits:/app/output" q_eng_proj

REM Notify the user
echo Outputs saved to ./circuits
