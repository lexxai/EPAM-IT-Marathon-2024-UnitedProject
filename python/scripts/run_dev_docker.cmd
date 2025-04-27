@echo off
PUSHD ..

docker compose up --build --no-attach mailtrap

POPD
