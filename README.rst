#############
MetricsIngest
#############

``MetricsIngest`` is a package in the `LSST Science Pipelines <https://pipelines.lsst.io>`_.


The program creates scripts to be used to creat metrics files and inject
results to squash. It also can create step yaml files for test-med-1 production.
To make it flexible for use by different users and for different stacks user
need to create and modify   minput.yaml file. User also need to get squash
login and password.
This can be received through dm-hsc-reprocessing slack channel asking
Angelo Fausti - @afausti.

minput.yaml
+++++++++++

dataset:     Data used for test
  'DC2_test-med-1'
run_id:      Current ticket
  'DM-36611'
version_tag:   Current stack version
  'w_2022_42'
sand_box:     Directory where json files will be created
  '/sdf/group/rubin/sandbox/kuropatk/metrics_json/'
date_tag:     Date when production was complete
  '2022-10-20T07:51'
squash_login:  Squash login
  '<squash login>'
squash_pas:    Squash password
  '<squash password>'
repo:     Repository where production results are located
  '/sdf/group/rubin/repo/dc2/'
run:      Path to the production results
  '2.2i/runs/test-med-1/w_2022_42/DM-36611'

Name: metrics

Commands:
+++++++++
--help, -h  : Help on commands

make-dispatch-sl  : Create dispatch.sl script

make-dispatch-sh : Create dispatch.sh script

make-js-file : Create make_json.sl script

make-steps : Create step yaml files for step1 - step9


Usage
=====
metrics make-steps ./minput.yaml

metrics make-js-file ./minput.yaml

sbatch make_json.sl

metrics make-dispatch-sl ./minput.yaml

metrics make-dispatch-sh ./minput.yaml

sbatch dispatch.sl

The last command will run for a long time.

