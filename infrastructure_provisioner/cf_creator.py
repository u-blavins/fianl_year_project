import yaml
import json

from cf_s3 import S3_CF

def main():
    payload = {
        "BucketEncryption": {
            "SSEAlgorithm": "AES256"
        },
        "BucketName": "test-bucket-provisioner",
        "PublicAccessBlockConfiguration": {
            "BlockPublicAcls": True,
            "BlockPublicPolicy": True,
            "IgnorePublicAcls": True,
            "RestrictPublicBuckets": True
        },
        "ObjectLockConfiguration": {
            "ObjectLockEnabled": "Enabled",
            "DefaultRetention": {
                "Mode": "GOVERNANCE",
                "Days": 1
            }
        },
        "VersioningConfiguration": "Enabled",
        "Tags": {
            "Owner": "Usama Blavins",
            "Role": "CloudFormation Template Bucket for EU-WEST-1"
        }
    }
    s3_cf = S3_CF(payload)
    s3_cf.set_template()
    print (json.dumps(s3_cf.get_template(), indent=4))
    return 0

main()