import Algorithmia


def call_algo(mgmt_api_key: str, algo_name: str, algo_hash: str, algo_input: str):
    client = Algorithmia.client(api_key=mgmt_api_key)
    algo = client.algo("{}/{}".format(algo_name, algo_hash))
    print("algo obj: {}".format(algo))
    print(algo.pipe(algo_input).result)
