# delete_untagged_versioned_S3_buckets
Deletes untagged, versioned, S3 buckets.

The script will skip over buckets that have MFA delete enabled, S3 object locking, bucket policies making explicit denies, etc.

### Usage:

  #### Dryrun mode

  `python3 FindAndDeleteUnTaggedBuckets.py`
  
  #### Help
  
  `python3 FindAndDeleteUnTaggedBuckets.py -h`
  
  #### Destructive / Data Deletion / Bucket Removal Mode
  
  `python3 FindAndDeleteUnTaggedBuckets.py --destructive`


