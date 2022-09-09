# sz-docker-compose-simple

Simple set of Docker Compose files to start a demonstrable and example Senzing stack using pre-built container images.

This stack emulates many components of one type of Senzing  architectural deployment patterns: https://senzing.zendesk.com/hc/en-us/articles/360051562333-Senzing-Architectural-Pattern-for-Perpetual-Insights

## Prerequisites

- Assumes using Linux
- Docker / Docker Compose are installed
- Internet connection
- Your user is a member of the docker group or you have sudo access. If you have sudo access prefix the docker/docker-compose commands with sudo. These instructions assume the user is a member of the docker group.

## Demonstration

This demonstrator utilises a number of example Docker images available at https://github.com/Senzing.

## Running

When localhost is referenced below it is assumed all actions are on the same machine. If you deploy the assets on one machine and use a browser to access them, change localhost to the hostname of the machine running the assets.

Run commands from within the yaml directory.

Export the SENZING_ENGINE_CONFIGURATION_JSON env var on the host with the Senzing engine configuration, change <host_name_here> to the hosts host name:

```export SENZING_ENGINE_CONFIGURATION_JSON='{"PIPELINE":{"CONFIGPATH":"/etc/opt/senzing","LICENSESTRINGBASE64":"","RESOURCEPATH":"/opt/senzing/g2/resources","SUPPORTPATH":"/opt/senzing/data"},"SQL":{"CONNECTION":"postgresql://postgres:password@<host_name_here>:5432:g2"}}'```

### Postgres

```docker-compose -f docker-compose-postgres.yaml up --detach```


### Senzing Tools - To add default Senzing configuration

```docker-compose -f docker-compose-tools.yaml up --detach```

### Senzing Loader 

```docker-compose -f docker-compose-loader.yaml up --detach --scale senzing-loader=2```

In the RabbitMQ console and the senzing queue, you should shortly see 5000 records removed from the queue as they are sent to Senzing for ingestion and entity resolution.

### Senzing Redeor

```docker-compose -f docker-compose-redoer.yaml up --detach```

### Senzing REST API Server

```docker-compose -f docker-compose-restserver.yaml up --detach```

Test the REST API Server by navigating to http://localhost:8250 or using curl:

```curl -X GET http://localhost:8250/specifications/open-api```

### Senzing Web App Demo

```docker-compose -f docker-compose-webapp.yaml up --detach```

Navigate to http://localhost:8251, search for 'RIOS BARBARA'

### Swagger UI

Run curl to fetch the API specification from the Senzing REST API Server, taking note to use the port from above:

```curl -X GET http://localhost:<port_from_above>/specifications/open-api -o /tmp/apispec.json```

This step uses a utility to extract the section from the specification required for Swagger, you may have to install this, e.g., on Debian 'sudo apt install jq'.

```curl -X GET http://localhost:8250/specifications/open-api | jq -c '.data' > ../data/rest_api_spec.json```

```docker-compose -f docker-compose-swagger.yaml up --detach```

Launch the Swagger UI console at: http://localhost:9180/
