#!/usr/bin/env python

import turbotutils
import turbotutils.cluster
import turbotutils.guardrails
import argparse
import csv
import json

if __name__ == '__main__':
    """ Performs a dump of a turbot accounts guardrails"""

    parser = argparse.ArgumentParser(description='dump a turbot accounts guardrail settings')
    parser.add_argument('source', help='The source account. Use cluster if you wish to use the cluster as a reference')
    args = parser.parse_args()
    
    filename = 'reports/guardrails/account_dump_of_' + args.source + '.csv'    
    
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        # Set to False if you do not have a valid certificate for your Turbot Host
        turbot_host_certificate_verification = True

        # Set to your Turbot Host URL
        turbot_host = turbotutils.get_turbot_host()

        # Get the access and secret key pairs
        (turbot_api_access_key, turbot_api_secret_key) = turbotutils.get_turbot_access_keys()
        urn_format = turbotutils.cluster.get_cluster_id(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification)
        if args.source == 'cluster':
            source_account_urn = urn_format
            print(source_account_urn)
        else:
            source_account_urn = urn_format + ':' + args.source
        
        

        sourceguardrails = turbotutils.guardrails.get_guardrail_list(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification,
                                                                     turbot_host,
                                                                     source_account_urn)

        
        writer.writerow(['Account Name', 'Guardrail Name', 'value' , 'Requirement'])
        print("Dumping the guardrails for %s" % (args.source))
        for guardrail in sourceguardrails:
            source = sourceguardrails[guardrail]['value']
            if not ((source.get('value') is not None ) and ( 'value' in source)):
                print("Guardrail %s is not set on source account (%s), requirement is: %s" % (guardrail, args.source,source['requirement']))
                writer.writerow([args.source,guardrail, 'No Value Set',source['requirement']])
                continue
            else: 
                print("Guardrail %s on %s is set to %s; requirement: %s" % (guardrail, args.source, source['value'],source['requirement']))
                writer.writerow([args.source, guardrail, source['value'],source['requirement']])
