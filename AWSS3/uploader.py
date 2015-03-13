from boto.s3.connection import S3Connection

from boto.s3.key import Key
from boto.s3.key import Key
import math, os
import boto
from filechunkio import FileChunkIO
from boto.s3.connection import Location

AWSAccessKeyId=""
AWSSecretKey=""



import socket
def hack_fileobject_close():
    if getattr(socket._fileobject.close, '__hacked__', None):
        return
    old_close = socket._fileobject.close
    def new_close(self, *p, **kw):
        try:
            return old_close(self, *p, **kw)
        except Exception, e:
            print("Ignore %s." % str(e))
    new_close.__hacked__ = True
    socket._fileobject.close = new_close
hack_fileobject_close()



def help_s3():
    print "https://console.aws.amazon.com/s3/home?region=us-west-2"
    print "http://boto.readthedocs.org/en/latest/s3_tut.html"
    print "this is a tips from aws s3."


def test():
    #conn = S3Connection('<aws access key>', '<aws secret key>')
    conn = S3Connection(AWSAccessKeyId, AWSSecretKey)
    print '\n'.join(i for i in dir(Location) if i[0].isupper())

    bucket = conn.get_bucket('tcloud_xenserver_vhd_test')
    #k = Key(bucket)
    #k.key = 'mice'
    #k.set_contents_from_string('A manager in TCloudComputing .')

    rs = conn.get_all_buckets()
    for b in rs:
        print b.name


    source_path = '/Users/cloud/Documents/ShareWith58/b5c7f006-612a-4283-9469-c2c2c682509a.vhd'
    source_size = os.stat(source_path).st_size


    '''
    mp = bucket.initiate_multipart_upload(os.path.basename(source_path))

    #chunk_size = 52428800
    chunk_size = 1024 * 1024 * 5
    chunk_count = int(math.ceil(source_size / chunk_size))
    for i in range(chunk_count + 1):
        print "begin chunk count:" + str(i)
        offset = chunk_size * i
        bytes = min(chunk_size, source_size - offset)
        with FileChunkIO(source_path, 'r', offset=offset,bytes=bytes) as fp:
            mp.upload_part_from_file(fp, part_num=i + 1)
        mp.complete_upload()
    print "successed transfer end."
    '''













