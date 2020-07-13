#!/usr/bin/python3

import os, json
from action_src import call_algo


if __name__ == "__main__":
    api_key = os.getenv("INPUT_API_KEY")
    metric = os.getenv("INPUT_METRIC")
    threshold = os.getenv("INPUT_THRESHOLD")
    checkpoints = os.getenv("INPUT_CHECKPOINTS")

    repo_name = os.getenv("INPUT_PATH")
    algo_hash = os.getenv("GITHUB_SHA")

    github_token = os.getenv("GITHUB_TOKEN")
    github_repo = os.getenv("GITHUB_REPOSITORY")

    repo_path = "/github/workspace/{}".format(repo_name)

    if not api_key:
        raise Exception("field 'api_key' not defined in workflow")
    if not repo_name:
        raise Exception("field 'repo_name' not defined in workflow")
    if not metric:
        raise Exception("field 'metric' not defined in workflow")
    if not threshold:
        raise Exception("field 'threshold' not defined in workflow")
    if not checkpoints:
        raise Exception("field 'checkpoints' not defined in workflow")

    model_eval_data = {
        "metric": metric,
        "threshold": threshold,
        "checkpoints": checkpoints,
    }

    if os.path.exists(repo_path):
        with open("{}/{}".format(repo_path, "algorithmia.conf")) as f:
            config_data = json.load(f)
        algo_name = "{}/{}".format(config_data["username"], config_data["algoname"])

        algo_input_dict = {
            "github_params": {
                "github_token": github_token,
                "github_repo": github_repo,
                "commit_sha": algo_hash,
            },
            "eval_params": model_eval_data,
        }

        algo_input = json.dumps(algo_input_dict)
        call_algo(api_key, algo_name, algo_hash, algo_input)
    else:
        raise Exception(
            "actions/checkout on the local repo must be run before this action can be completed"
        )
