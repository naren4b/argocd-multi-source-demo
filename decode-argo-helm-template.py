#alias helmtester="python $PWD/decodeArgoApp.py  --dry-run=true " 
#helmtester --app=main-app-dc-deployments-active
#python decodeArgoApp.py --app main-app-dc-deployments-active --dry-run=true > out.yaml


import yaml
import os
import argparse

isDryRun = "true"
current_directory = os.getcwd()
APPLICATION_NAME = "demo"


def executeMyCommand(command):
    print("isDryRun :" + isDryRun)
    print(command)
    if "false" == isDryRun:
        os.system(command)


def load_yaml_file(file_path):
    with open(file_path, "r") as file:
        try:
            yaml_data = yaml.safe_load(file)
            return yaml_data
        except yaml.YAMLError as exc:
            print(exc)
            return None


def replaceRefValue(sources, filepath):
    ref = filepath.split("/")[0]
    ref_dir = ""
    for repo in sources:
        if ref[1:] in repo.get("ref"):
            ref_dir = repo.get("repoURL").split("/")[4].split(".")[0]

    return filepath.replace(ref, ref_dir)


def getHelmCommand(sources):
    HELM_TEMPLATE_BASE_COMMAND = "helm template"
    FILE_PATH = ""
    for repo in sources:
        if "path" in repo:
            TEMPLATE_PATH = (
                repo.get("repoURL").split("/")[4].split(".")[0] + "/" + repo.get("path")
            )

            for key, values in repo.items():
                if "helm" == key:
                    for key, files in values.items():
                        for filepath in files:
                            # print(filepath)
                            FILE_PATH = (
                                FILE_PATH + " -f " + replaceRefValue(sources, filepath)
                            )
    COMMAND = (
        HELM_TEMPLATE_BASE_COMMAND
        + " "
        + APPLICATION_NAME
        + " "
        + TEMPLATE_PATH
        + " "
        + FILE_PATH
    )
    print("#" + COMMAND)
    os.system(COMMAND)


def getGitCommand(sources):
    for repo in sources:
        GIT_CLONE_BASE_COMMAND = "git clone --depth 1 -b "
        ref_dir = repo.get("repoURL").split("/")[4].split(".")[0]
        repoURL = repo.get("repoURL")
        targetRevision = repo.get("targetRevision")
        executeMyCommand("rm -rf {}".format(os.path.join(current_directory, ref_dir)))
        executeMyCommand(GIT_CLONE_BASE_COMMAND + " " + targetRevision + " " + repoURL)


def main():
    data = load_yaml_file(APPLICATION_NAME + ".yaml")
    sources = data.get("sources")
    if data is None:
        print("Failed to load YAML file.")
        return
    if "false" == isDryRun:
        getGitCommand(sources)
    getHelmCommand(sources)


if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Process command-line arguments")
    # Add arguments
    parser.add_argument("--app", required=True, help="Name of the application")
    parser.add_argument(
        "--dry-run",
        choices=["true", "false"],
        required=True,
        help="Dry run mode (true/false)",
    )

    # Parse arguments
    args = parser.parse_args()
    APPLICATION_NAME = args.app
    isDryRun = args.dry_run
    # Call main function with parsed arguments
    main()
