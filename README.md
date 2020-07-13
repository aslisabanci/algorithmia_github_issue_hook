# Algorithmia-Github Issue Hook
Inspired by [Algorithmia CI/CD](https://github.com/marketplace/actions/algorithmia-ci-cd), I created this Github action as a POC when playing with Github Actions and Algorithmia. 

If you have a model that you evaluate periodically against your configured metric and a threshold, and you want to be notified of its performance drops; you can incorporate this action as a workflow. 

Through this action, you can configure: 
- The path of the checkpoint weights that you want to restore your model with
- Metric name 
- Threshold value to compare the test results

Behind the scenes, your Github token, Github repo name and the latest commit SHA is also passed to your Algorithmia algorithm. Given these, your algorithm can use this hook as a feedback line and can report its problems back to you by creating a Github issue on your repo.


# Workflow Input

```
api_key:
    description: 'Algorithmia API key'
    required: true
path:
    description: 'directory name for the local project stored in /github/workspace due to an "actions/checkout" command'
    required: true
metric:
    description: Evaluation metric of the model on the test set
    required: true
threshold:
    description: Threshold value for the test metric, under which the algorithm creates a Github issue
    required: true
checkpoints:
    description: The path of the checkpoints to restore your model from
    required: true
```


# Example workflow
The workflow below shows a periodic run setup, scheduled to run every 10 minutes. 
Checkout my sample repository https://github.com/aslisabanci/algorithmia_issue_reporter to see this in action.

```
name: Algorithmia-Github Issue Hook

on:
  schedule:
    - cron: "*/0 8 * * *"

jobs:
  algorithmia-ci:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v2.0.0
        with:
          ref: ${{github.sha}}
          path: algorithm
      - name: Algorithmia-Github Issue Hook
        uses: aslisabanci/algorithmia_github_issue_hook@v0.1-alpha
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ secrets.GITHUB_REPOSITORY }}
        with:
          api_key: ${{ secrets.api_key }}
          path: algorithm
          metric: accuracy
          threshold: 0.85
          checkpoints: ./checkpoints/fashion_mnist_checkpoint
          
```

# Improvement ideas
Since this is only a POC hack to play with and learn more about Github Actions and Algorithmia, a few things can be done differently for normal use cases. 
- Instead of using model checkpoints, you can restore your model directly from a saved model. Restoring a model from saved weights requires that you first create a model with the same architecture as the original model - so you may not prefer that. 
- You can update the workflow to make use of multiple performance metrics (and multiple thresholds), and not just a single one
- You can apply this "issue reporting" logic to check your model's input data as well. If the distribution or the quality of your data changes, you can again get notified of this through your responsible algorithm's bug reports :]
