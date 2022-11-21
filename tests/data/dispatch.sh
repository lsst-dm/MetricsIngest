#!/bin/env bash
# Look up at https://eups.lsst.codes/stack/src/tags/
export DATETAG="2022-10-20T07:51"
export DATASET="DC2_test-med-1"
export DATASET_REPO_URL="https://community.lsst.org/t/shared-gen3-data-repositories-ready-for-some-use/4845"
export RUN_ID="DM-36611"
export RUN_ID_URL="https://jira.lsstcorp.org/browse/DM-36611"
export VERSION_TAG="w_2022_42"

export SQUASH_USER=<squash login>
export SQUASH_password=<squash password>
ls -A1 /sdf/group/rubin/sandbox/kuropatk/metrics_json/ |grep verify.json| awk -v DATETAG="2022-10-20T07:51" '{print "dispatch_verify.py /sdf/group/rubin/sandbox/kuropatk/metrics_json/" $1,"--ignore-blobs --ignore-lsstsw  --url https://squash-restful-api.lsst.codes --env=ldf --date-created "DATETAG":00Z"}' | bash
