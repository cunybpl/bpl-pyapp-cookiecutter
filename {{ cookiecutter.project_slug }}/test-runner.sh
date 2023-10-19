#!/bin/bash 
set -e

usage_exit(){
    printf '\nUsage: %s: [-n] name [-m] marker \n' $0; exit 1;
}



marker=""
name=""
nameset=0
markerset=0

while getopts n:m:h flag; do 
    case "${flag}" in 
        m) marker=${OPTARG}; markerset=1;; 
        n) name=${OPTARG}; nameset=1;;        
        ?|h) usage_exit
    esac 
done 

POSTGRES_USER=${{ cookiecutter.project_env_prefix }}_POSTGRES_USER
POSTGRES_PASSWORD=${{ cookiecutter.project_env_prefix }}_POSTGRES_PASSWORD
POSTGRES_TEST_DB=${{ cookiecutter.project_env_prefix }}_POSTGRES_TEST_DB
POSTGRES_HOST=${{ cookiecutter.project_env_prefix }}_POSTGRES_HOST 
POSTGRES_PORT=${{ cookiecutter.project_env_prefix }}_POSTGRES_PORT


if [[ -v $user || -v $pass || -v $db || -v $host || -v $port ]]; then 
    
    echo "POSTGRES Environment variables not configured."; 
    echo POSTGRES_USER: $POSTGRES_USER
    echo POSTGRES_PASSWORD: $POSTGRES_PASSWORD
    echo POSTGRES_TEST_DB: $POSTGRES_TEST_DB
    echo POSTGRES_HOST: $POSTGRES_HOST
    echo POSTGRES_PORT: $POSTGRES_PORT
    
    exit 1;
fi


PGPASSWORD=$pass dropdb -h $host -p $port -U $user -e -f --if-exists $db
PGPASSWORD=$pass createdb -h $host -p $port -U $user -e $db

poetry run alembic upgrade head

# if we get a module name the run that one, or a marker name run that one or run everything
# if both -n and -m are set then -n takes precedence.
if [ $nameset -eq 1 ] 
then
    poetry run pytest --cov={{ cookiecutter.project_slug }}/ --cov-report=term-missing ${name} -v -s
    
elif [ $markerset -eq 1 ]
then  
    poetry run pytest -v -s -m ${marker} --cov={{ cookiecutter.project_slug }}/ --cov-report=term-missing 

else 
    poetry run pytest -s -v -m "not live" --cov={{ cookiecutter.project_slug }}/ --cov-report=term-missing

fi
poetry run alembic downgrade base
poetry run mypy {{ cookiecutter.project_slug }} --strict

PGPASSWORD=$pass dropdb -h $host -p $port -U $user -e -f --if-exists $db