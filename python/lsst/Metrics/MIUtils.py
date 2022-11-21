#!/usr/bin/env python
"""
This is a standalone program to generate scripts
 used in creation and ingestion of production metrics.
"""
import yaml


class MIUtils:
    """
    The class contains methods to create scripts necessary for
    producing metrix jason files, and injection of them into
    squash database.
    Parameters:
        input_file : a yaml file containing configuration parameters
    """
    def __init__(self, input_file):
        """Get parameters - yaml file """
        with open(input_file) as pf:
            input_parameters = yaml.safe_load(pf)
        self.dataset = input_parameters['dataset']  # 'DC2'
        self.run_id = input_parameters['run_id']  # 'DM-36611'
        self.version_tag = input_parameters['version_tag']  # 'w_2022_42'
        self.sand_box = input_parameters['sand_box']  # '/sdf/group/rubin/sandbox/kuropatk/metrics_json/'
        self.date_tag = input_parameters['date_tag']  # '2022-10-20T07:51'
        self.squash_login = input_parameters['squash_login']  #
        self.squash_pas = input_parameters['squash_pas']
        self.repo = input_parameters['repo']  # /sdf/group/rubin/repo/dc2/
        self.run = input_parameters['run']  # 2.2i/runs/test-med-1/w_2022_42/DM-36611
        self.steps = {'step1': 'step1', 'step2': 'step2', 'step3': 'step3', 'step4': 'step4',
                      'step5': 'step5', 'step6': 'step6', 'step7': 'step7',
                      'step8': 'faro_all', 'step9': 'analysis_coadd_plots'}

    def make_json(self):
        """
        The method creates make_json.sl script.

        """
        template = ['#!/bin/bash -l', '#SBATCH -p roma', '#SBATCH -N 1', '#SBATCH -n 1 ',
                    "#SBATCH --mem=20G", '#SBATCH -t 54:00:00', '#SBATCH -J testres',
                    f"#SBATCH --output=make_json_{self.version_tag}.%j.log",
                    f"#SBATCH --error=make_json_{self.version_tag}.%j.log",
                    f"#SBATCH --chdir {self.sand_box}",
                    f"srun gen3_to_job.py '{self.repo}'  '{self.run}'  --dataset_name '{self.dataset}'"]
        out_file = 'make_json.sl'
        with open(out_file, 'w') as of:
            for line in template:
                of.write(line + '\n')
            of.flush()
            of.close()

    def make_dispatch_sl(self):
        """
         The method creates dispatch.sl script.
        """
        template = ["#!/bin/bash -l", "#SBATCH -p roma", "#SBATCH -N 1", "#SBATCH -n 1",
                    "#SBATCH --mem=20G", "#SBATCH -t 54:00:00", "#SBATCH -J verify",
                    f"#SBATCH --output=dispatch_{self.version_tag}.%j.log",
                    f"#SBATCH --error=dispatch_{self.version_tag}.%j.log", "srun dispatch.sh"]
        out_file = 'dispatch.sl'
        with open(out_file, 'w') as of:
            for line in template:
                of.write(line + '\n')
            of.flush()
            of.close()

    def make_dispatch_sh(self):
        """ The method creates dispatch.sh script to be used with
        dispatch.sl for running in slurm.
        """
        awk_command = f" \'{{print \"dispatch_verify.py {self.sand_box}\" "
        awk_command += "$1,\"--ignore-blobs --ignore-lsstsw  --url https://squash-restful-api.lsst.codes "
        awk_command += "--env=ldf --date-created \"DATETAG\":00Z\"}\'"
        template = ["#!/bin/env bash", "# Look up at https://eups.lsst.codes/stack/src/tags/",
                    f"export DATETAG=\"{self.date_tag}\"", f"export DATASET=\"{self.dataset}\"",
                    "export DATASET_REPO_URL=\"https://community.lsst.org/t/"
                    + "shared-gen3-data-repositories-ready-for-some-use/4845\"",
                    f"export RUN_ID=\"{self.run_id}\"",
                    f"export RUN_ID_URL=\"https://jira.lsstcorp.org/browse/{self.run_id}\"",
                    f"export VERSION_TAG=\"{self.version_tag}\"", "",
                    f"export SQUASH_USER={self.squash_login}",
                    f"export SQUASH_password={self.squash_pas}",
                    f"ls -A1 {self.sand_box} |grep verify.json"
                    + f"| awk -v DATETAG=\"{self.date_tag}\""
                    + awk_command + " | bash"]

        out_file = 'dispatch.sh'
        with open(out_file, 'w') as of:
            for line in template:
                of.write(line + '\n')
            of.flush()
            of.close()

    def make_steps(self):
        """ The method to create step yaml
         files for DC2 test-med-1 production """
        for step in self.steps:
            command = self.steps[step]
            template = ["imports:", "  - $DRP_PIPE_DIR/ingredients/LSSTCam-imSim/DRP.yaml",
                        "  - $ANALYSIS_DRP_DIR/pipelines/LSSTCam-imSim/analysis_drp_plots.yaml",
                        "includeConfigs:", "- ${CTRL_BPS_PANDA_DIR}/config/bps_usdf.yaml ",
                        f"- requestMemory_{step}.yaml", f"- clustering_{step}.yaml", " ",
                        f"LSST_VERSION: {self.version_tag}", " ", "project: dp02",
                        f"campaign: {self.version_tag}/{self.run_id}",
                        "pipelineYaml: \"${DRP_PIPE_DIR}/pipelines/LSSTCam-imSim/DRP-test-med-1.yaml#"
                        + f"{command}\"",
                        " ", "payload:", "  payloadName: 2.2i/runs/test-med-1",
                        "  output: \"{payloadName}/{campaign}\"",
                        "  butlerConfig: /sdf/group/rubin/repo/dc2/butler.yaml",
                        "  inCollection: \"2.2i/defaults/test-med-1\"",
                        "  dataQuery: "
                        + "\"instrument='LSSTCam-imSim' and skymap='DC2' and tract in (3828, 3829)\"",
                        "  payloadFolder: payload",
                        f"  sw_image: \"lsstsqre/centos:7-stack-lsst_distrib-{self.version_tag}\""]
            out_file = str(step) + '.yaml'
            with open(out_file, 'w') as of:
                for line in template:
                    of.write(line + '\n')
                of.flush()
                of.close()
