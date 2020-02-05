from flask import Blueprint, request, Response, jsonify
from aws_utils.cf_s3 import S3_CF as CloudFormationS3Handler

import json

provisioner = Blueprint('provisioner', __name__)

@provisioner.route('/api/v1/provisioner/validate', methods=['POST'])
def validate():
    payload = request.get_json()
    cf_provisioner = CloudFormationS3Handler(payload=payload)
    template = cf_provisioner.get_iac_template()
    return jsonify(template=template)

@provisioner.route('/api/v1/provisioner/provision', methods=['POST'])
def provision():
    payload = request.get_json()
    return jsonify(payload)

# curl -d "@payload.json" -X POST http://localhost:8080/api/v1/provisioner/validate