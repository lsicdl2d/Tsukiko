from graia.application.message.elements.internal import Plain


def handler(var_dict: dict):
    print(var_dict.get('msgChain').get(Plain)[0])


def run(var_dict: dict):
    handler(var_dict)
