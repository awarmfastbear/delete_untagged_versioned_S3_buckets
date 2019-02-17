import argparse
import boto3
from functools import reduce  # forward compatibility for Python 3
import operator

#boto3.set_stream_logger('botocore') #debug logging at the ready!

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("--destructive", "--d", "-d", help="WARNING: If specified, buckets that are untagged will be removed. This switch will PERMANENTLY delete objects in nontagged buckets. Please ensure you are comfortable with permanently deleting data in your untagged buckets before running this script.",
                    action="store_true")
args = parser.parse_args()

def lambda_handler(event, context):

	n_of_buckets_to_remove = 0
	bucket_name_array = []
	buckets_to_delete_array = []
	buckets_deleted = []

	client = boto3.client('s3', region_name='us-east-1')
	bucket_list_response = client.list_buckets() # get a list of buckets
	session = boto3.Session()
	s3_session = session.resource(service_name='s3')



	if not args.destructive:
		print("                 ==== DRY RUN MODE ENABLED ====")
	else:
		print("                 ==== DESTRUCTIVE MODE ENABLED, PERMANENTLY REMOVING DATA ====")

	 #Get list of buckets in the account
	for bucket in bucket_list_response["Buckets"]:
		#print(bucket['Name']) #print all bucket names in the account.
		bucket_name_array.append(bucket['Name'])

	#For each bucket in the account look for tags on the bucket.
	for bucket_name in bucket_name_array:
		try:
			tag_response = client.get_bucket_tagging(
		Bucket=bucket_name)

		#if there's no tag on the bucket we'll get an exception and mark this bucket as deletable
		except Exception as e:
			#print(e)
			buckets_to_delete_array.append(bucket_name)

	for b_name in buckets_to_delete_array:
		bucket = s3_session.Bucket(b_name)
		try:
			print("====================")
			if args.destructive:
				print("Attempting to remove bucket: " + b_name)
				print("Attempting to delete all objects in: " + b_name + ".")
				bucket.object_versions.delete()
			else:
				print("Dry run mode: Would of attempted to delete all objects in bucket: " + b_name)

		except Exception as e:
			print(e)
			print("Failed to list and delete objects, please ensure that you do not have a setting or policy explicitly denying list and delete calls.")
			pass
		try:
			if args.destructive:
				print("Attempting to deleting bucket named: " + b_name)
				bucket.delete()
				n_of_buckets_to_remove += 1
				buckets_deleted.append(b_name)
			else:
				print("Dry run mode: Would of attempted to delete bucket: " + b_name)
				n_of_buckets_to_remove += 1
		except Exception as e:
			print(e)
			print("Could not delete bucket named: " + b_name + "." + "This was likely due to a 403 from a bucket policy, an object could not be deleted due to an object lock, or root account's ACL is missing. Please investigate this bucket as to why it cannot be deleted.")
			continue

	print("====================")

	if n_of_buckets_to_remove >= 1:
		print("Bucket names deleted: " + str(buckets_deleted))
		print("Deleted " + str(len(buckets_deleted)) + " buckets!")
	if n_of_buckets_to_remove == 0:
		print("No buckets found that are untagged, script exiting.")

#dirty error wrapping
try:
    lambda_handler(1,1)
except Exception as e:
    print(e)
    code = 1
except Exception as e:
    raise
    code = 2

print("If you want to run without dryrun mode, add '-d' as an argument, otherwise use '-h' for help'")
print("Script exiting! Have nice day!")
