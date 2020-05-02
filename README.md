# escala-rest-api [![Build Status](https://travis-ci.org/mirandarfsm/escala-rest-api.svg?branch=master)](https://travis-ci.org/mirandarfsm/escala-rest-api)
Military Public Institutions need to be guarded 24 hours a day 7 days a week. This is done through a shift rotation between the military personnel assigned to this task. One single person is assigned to organize escalations; normally this is done through a spreadsheet. This is a difficult process to execute because even after intense planning there will always be changes that will be done increasing the chance of error, for example, one person can be assigned more work than others. Evaluating this scenario, we through of a system to generate and allocate people for guard duty and military organization. An algorithm was developed after several military registries did the same allocated plan of one person in a determined period. Using the system interface the user can use the services in a dynamic way to exchange shifts and the system has total control to validate and modify without needing permission between the other workers. By using this escalation system for the users, the process has become more simple, trusting and just.

**Keywords**: Flask; SQLAlchemy; AngularJS; Rest; Escalations; Allocation.


## Requirements

* Docker
* Docker Composer

## Installation

```
docker-compose build
docker-compose up -d
```
Access by 127.0.0.1 in your favorite browser

## Development

```
docker-compose -f development.yml build
docker-compose -f development.yml build
```

### Debug code

Edit deployement.yml, uncomment debug code line

```
command: python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess -m flask run -h 0.0.0.0 -p 5000 --no-debugger --no-reload
```

#### VS code

Create a lauch.json with this configs

```
{
            "type": "python",
            "request": "attach",
            "name": "Python Attach",
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/server/",
                    "remoteRoot": "/app/server"
                }
            ],
            "port": 5678,
            "host": "127.0.0.1",
            "subProcess": true,
        },
```


## References

[johnpapa/angular-styleguide](https://github.com/johnpapa/angular-styleguide/tree/master/a1)

[miguelgrinberg/api-pycon2014](https://github.com/miguelgrinberg/api-pycon2014)

[gomex/docker-para-desenvolvedores](https://github.com/gomex/docker-para-desenvolvedores)
