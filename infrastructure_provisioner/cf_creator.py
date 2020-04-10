import json

from cf_s3 import S3_CF
from cf_builder import CF_BUILDER

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
    cf_builder = CF_BUILDER()
    s3_cf = S3_CF(payload)
    s3_cf.set_template()
    resource = s3_cf.get_template()
    cf_builder.set_description("The is a test CloudFormation template")
    cf_builder.set_resources(resource_type='S3Bucket', resource=resource)
    print(json.dumps(
        cf_builder.get_template(),
        indent=4
    ))
    return 0

main()