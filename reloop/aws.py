import boto3


class AwsContext:

    def __init__(self, account_id):
        if not account_id:
            raise ValueError("AWS account identifier is empty or missing")

        self.account_id = str(account_id)

    def ensure_state_store(self):
        pass


def check_for_aws_creds():

    """Checks a handful of sources to see if AWS credentials are set in the environment. This function does not test if
    the credentials are valid."""

    found = True
    return found


def init_aws_ctx():

    """Create a context object for AWS that holds the account identifier and other useful information that need to be
    resolved only once."""

    if not check_for_aws_creds():
        raise Exception()

    account_id = boto3.client('sts').get_caller_identity().get('Account')
    return AwsContext(account_id)


def create_fab_state_store_bucket_name(ctx):

    """Creates an S3 bucket name that is likely to be globally unique"""
    bucket_name = 'fabformer-{0}'.format(ctx.account_id)
    bucket_name  # do something with it


def ensure_fab_state_store(name, engine="s3"):

    """Check for and create if not present a location where Fabformer state is stored."""

    usable_engines = {'s3'}
    engine = str(engine).lower()
    if engine not in usable_engines:
        raise ValueError('Invalid state storage engine (chosen: {}, usable: {})', engine, usable_engines)
    return


def ensure_fabric_dns():
    pass
