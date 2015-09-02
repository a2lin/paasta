from paasta_tools.paasta_cli.utils import _run
from paasta_tools.utils import compose_job_id


def get_serviceinit_status(service, namespace):
    command = "paasta_serviceinit -v %s status" % compose_job_id(service, namespace)
    return _run(command, timeout=10)[1]


def get_context(service, namespace):
    """Tries to get more context about why a service might not be OK.
    returns a string useful for inserting into monitoring email alerts."""
    status = get_serviceinit_status(service, namespace)
    context = "\nMore context from paasta status:\n%s" % status
    return context
