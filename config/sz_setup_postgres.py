#! /usr/bin/env python3

import json
import os
import sys
import shutil

from senzing import G2Config, G2ConfigMgr, G2Exception
from urllib.parse import urlparse


def main():
    """ """

    engine_config = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON')

    if not engine_config:
        print('The environment variable SENZING_ENGINE_CONFIGURATION_JSON must be set with a proper JSON configuration.\n'
              'Please see https://senzing.zendesk.com/hc/en-us/articles/360038774134-G2Module-Configuration-and-the-Senzing-API')
        exit(-1)
    else:
        try:
            json_config = json.loads(engine_config)
        except ValueError as ex:
            print(f'Couldn\'t parse SENZING_ENGINE_CONFIGURATION_JSON, please check the format: {ex}\n'
                  'Please see https://senzing.zendesk.com/hc/en-us/articles/360038774134-G2Module-Configuration-and-the-Senzing-API')
            exit(-1)

    if json_config.get('SQL', None).get('BACKEND', None) and json_config['SQL']['BACKEND'].upper() == 'HYBRID':
        print('Clustered backends are not supported')
        exit(-1)

    try:
        uri = urlparse(json_config['SQL']['CONNECTION'])
    except ValueError:
        print('SENZING_ENGINE_CONFIGURATION_JSON doesn\'t contain a connection string!')
        exit(-1)
    else:
        if uri.scheme.upper() != 'POSTGRESQL':
            print(f'Only Postgres DBs are supported. Found: {uri.scheme}')
            exit(-1)

    try:
        default_config_id = bytearray()
        g2_config_mgr = G2ConfigMgr()
        g2_config_mgr.init("g2ConfigMgr", engine_config, False)
        g2_config_mgr.getDefaultConfigID(default_config_id)

        if default_config_id:
            print('Database already contains a default configuration.  Skipping creation.')
        else:
            g2_config = G2Config()
            g2_config.init("g2Config", engine_config, False)
            config_handle = g2_config.create()
            new_configuration_bytearray = bytearray()
            g2_config.save(config_handle, new_configuration_bytearray)
            g2_config.close(config_handle)

            config_json = new_configuration_bytearray.decode()
            new_config_id = bytearray()
            g2_config_mgr.addConfig(config_json, 'Configuration added from sz-docker-compose-simple.', new_config_id)
            g2_config_mgr.setDefaultConfigID(new_config_id)
            g2_config.destroy()
            print('Created default configuration')

        g2_config_mgr.destroy()

    except G2Exception as err:
        print(err, file=sys.stderr)
        exit(-1)


if __name__ == "__main__":
    main()
