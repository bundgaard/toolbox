#!/bin/env python
import os, sys, re
from datetime import datetime, timedelta 
import urllib
import_uri = 'http://vss-s-db01.sth.basefarm.net:8082/solr3/xplaycms/dataimport?command=full-import&clean=false&wt=json'
clean_uri = 'http://vss-s-db01.sth.basefarm.net:8082/solr3/xplaycms/update?commit=true&wt=json'
status_uri = 'http://vss-s-db01.sth.basefarm.net:8082/solr3/xplaycms/dataimport?command=status&wt=json'


def UTC_NOW():
	return (datetime.utcnow()).strftime("%Y-%m-%dT%H:%M:%Sz")

def UTC_HALF_HOUR():
	return (datetime.utcnow() - timedelta(seconds=60*30)).strftime("%Y-%m-%dT%H:%M:%Sz")

def data():
	return "<delete><query>index_time_s:[{0} TO {1}]</query></delete>"
def check_ten_times(sleep=10):
	pass

"""
The handler exposes all its API as http requests . The following are the possible operations

    full-import : Full Import operation can be started by hitting the URL http://<host>:<port>/solr/dataimport?command=full-import

        This operation will be started in a new thread and the status attribute in the response should be shown busy now.
        The operation may take some time depending on size of dataset.

        When full-import command is executed, it stores the start time of the operation in a file located at conf/dataimport.properties (this file is configurable)
        This stored timestamp is used when a delta-import operation is executed.
        Queries to Solr are not blocked during full-imports.
        It takes in extra parameters:

            entity : Name of an entity directly under the <document> tag. Use this to execute one or more entities selectively. Multiple 'entity' parameters can be passed on to run multiple entities at once. If nothing is passed, all entities are executed.

            clean : (default 'true'). Tells whether to clean up the index before the indexing is started.

            commit : (default 'true'). Tells whether to commit after the operation.

            optimize : (default 'true' up to Solr 3.6, 'false' afterwards). Tells whether to optimize after the operation. Please note: this can be a very expensive operation and usually does not make sense for delta-imports.

            debug : (default 'false'). Runs in debug mode. It is used by the interactive development mode (see here).
                Please note that in debug mode, documents are never committed automatically. If you want to run debug mode and commit the results too, add 'commit=true' as a request parameter. 

    delta-import : For incremental imports and change detection run the command http://<host>:<port>/solr/dataimport?command=delta-import . It supports the same clean, commit, optimize and debug parameters as full-import command.

    status : To know the status of the current command, hit the URL http://<host>:<port>/solr/dataimport . It gives an elaborate statistics on no. of docs created, deleted, queries run, rows fetched, status etc.

    reload-config : If the data-config is changed and you wish to reload the file without restarting Solr. Run the command http://<host>:<port>/solr/dataimport?command=reload-config .

    abort : Abort an ongoing operation by hitting the URL http://<host>:<port>/solr/dataimport?command=abort . 
"""
if __name__ == '__main__':
	print '#', len(sys.argv[:1]), sys.argv[1:]
	if len(sys.argv) < 2:
		print "provide a clean or import statement"
		sys.exit(1)
	if 'clean' in sys.argv[1:]:
		print "curl -XPOST --data-binary \"{0}\" -H\"content-type:application/json\" \"{1}\"".format( data().format(urllib.quote(UTC_HALF_HOUR()).encode('utf8'), urllib.quote(UTC_NOW()).encode('utf8')), clean_uri)
	elif 'import' in sys.argv[1:]:
		print "curl -XGET \"{0}\"".format( import_uri )
	elif 'status' in sys.argv[1:]:
		print "curl -s -XGET \"{0}\"".format(status_uri)
	
