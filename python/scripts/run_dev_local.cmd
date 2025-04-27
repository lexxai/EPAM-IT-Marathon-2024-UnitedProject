@echo off

PUSHD ..\pet-project

uvicorn main:main_app --host 0.0.0.0 --port 8001 
rem --reload 

POPD
