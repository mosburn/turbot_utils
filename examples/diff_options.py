#!/usr/bin/env python

import turbotutils
import turbotutils.cluster
import turbotutils.guardrails
import argparse
import csv
import json

if __name__ == '__main__':
    """ Preforms a guardrail diff of two accounts to allow for easier migration between two accounts and validation"""

    parser = argparse.ArgumentParser(description='diff two turbot account guardrail settings')
    parser.add_argument('source', help='The source account')
    parser.add_argument('dest', help='The Destination account')
    args = parser.parse_args()
    if args.source == "cluster":
        filename = 'reports/guardrails/cluster_to_' + args.dest + '.csv'
    else:
        filename = 'reports/guardrails/' +  args.source + '_to_' + args.dest + '.csv'
        
    
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
            source_account_urn = urn_format + ':'
        else:
            source_account_urn = urn_format + ':' + args.source
        dest_source_account_urn = urn_format + ':' + args.dest
        difference_count = 0

        sourceguardrails = turbotutils.guardrails.get_guardrail_list(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification,
                                                                     turbot_host,
                                                                     source_account_urn)

        destguardrails = turbotutils.guardrails.get_guardrail_list(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification,
                                                                   turbot_host,
                                                                   dest_source_account_urn)
        writer.writerow(['Guardrail Name', 'Source value', 'Destination value'])
        print("Finding the guardrail differences between %s and %s" % (args.source, args.dest))
        for guardrail in sourceguardrails:
            source = sourceguardrails[guardrail]['value']
            dest = destguardrails[guardrail]['value']
            if source != dest:
                if not ((dest.get('value') is not None ) and ( 'value' in dest )):
                    print ( 'dest has no key value')
                    print('dest>>>>')
                    print(json.dumps(dest, indent=3))
                    print('src>>>>')
                    print (json.dumps(source, indent=3))
                    continue
                if not ((source.get('value') is not None ) and ( 'value' in source)):
                    print ('source has no key value')
                    print('dest>>>>')
                    print(json.dumps(dest, indent=3))
                    print('src>>>>')
                    print (json.dumps(source, indent=3))
                    continue 
                if source['value'] != dest['value']:
                    print("Guardrail %s on source account is set to %s and %s on destination account" % (guardrail, source['value'], dest['value']))
                    difference_count += 1
                    writer.writerow([guardrail, source['value'], dest['value']])
        if difference_count != 0:
            print('Accounts %s and %s are not in sync, please manually review and rectify this' %(args.source, args.dest))
            print('I found %d differences between these two accounts' % difference_count)
        else:
            print('Accounts %s and %s are in sync' % (args.source, args.dest))
