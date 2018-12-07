import boto # developed on boto 2.9.6.
from boto.s3.connection import S3Connection
conn = S3Connection("YOUR_AWS_ACCESS_KEY", "YOUR_AWS_SECRET_KET")
source = conn.get_bucket("YOUR_SOURCE_BUCKET_NAME_HERE")
target = conn.get_bucket("YOUR_TARGET_BUCKET_NAME_HERE")

# .list() is a magical iterator object, it'll make
# more requests of S3 as needed
for idx, entry in enumerate(source.list()):
    if entry.name.endswith("/"):
        continue
    print idx, entry.name
    if not target.get_key(entry.name):
        # this is a trade-off. Checking for target existence makes the first
        # run slower, but subsequent runs much faster, assuming only a subset
        # of files change.
        print "..copying"
        try:
            entry.copy(dst_bucket=target, dst_key=entry.name, validate_dst_bucket=False)
        except boto.exception.S3ResponseError, e:
            # Only copying files I have access to. Never bomb out half-way.
            print e

print "all done!"