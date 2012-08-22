#coding=utf-8
'''
Created on 2012-7-9

@author: fengclient
'''
import gearman

if __name__ == '__main__':
    gm_admin_client = gearman.GearmanAdminClient(['localhost:4730'])

    # Inspect server state
    status_response = gm_admin_client.get_status()
    version_response = gm_admin_client.get_version()
    workers_response = gm_admin_client.get_workers()
    for worker in workers_response:
        #unregister before shutdown
        worker.shutdown()