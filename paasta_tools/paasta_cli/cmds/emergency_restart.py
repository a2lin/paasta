#!/usr/bin/env python
# Copyright 2015 Yelp Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from paasta_tools.paasta_cli.utils import execute_paasta_serviceinit_on_remote_master
from paasta_tools.paasta_cli.utils import figure_out_service_name
from paasta_tools.paasta_cli.utils import lazy_choices_completer
from paasta_tools.paasta_cli.utils import list_services
from paasta_tools.paasta_cli.utils import list_instances
from paasta_tools.utils import compose_job_id
from paasta_tools.utils import list_clusters


def add_subparser(subparsers):
    status_parser = subparsers.add_parser(
        'emergency-restart',
        description="Restarts a PaaSTA service instance in an emergency",
        help="Restarts a PaaSTA service instance by running emergency-stop then emergency-start on it.")
    status_parser.add_argument(
        '-s', '--service',
        help="Service that you want to restart. Like 'example_service'.",
    ).completer = lazy_choices_completer(list_services)
    status_parser.add_argument(
        '-i', '--instance',
        help="Instance of the service that you want to restart. Like 'main' or 'canary'.",
        required=True,
    ).completer = lazy_choices_completer(list_instances)
    status_parser.add_argument(
        '-c', '--cluster',
        help="The PaaSTA cluster that has the service you want to restart. Like 'norcal-prod'.",
        required=True,
    ).completer = lazy_choices_completer(list_clusters)
    status_parser.set_defaults(command=paasta_emergency_restart)


def paasta_emergency_restart(args):
    """Performs an emergency restart on a given service instance on a given cluster

    Warning: This command is only intended to be used in an emergency.
    It should not be needed in normal circumstances.

    See the service-docs for paasta emergency-stop and emergency-start for details of what exactly this does:
    http://servicedocs.yelpcorp.com/docs/paasta_tools/generated/paasta_tools.paasta_cli.cmds.emergency_stop.html
    http://servicedocs.yelpcorp.com/docs/paasta_tools/generated/paasta_tools.paasta_cli.cmds.emergency_start.html
    """
    service = figure_out_service_name(args)
    print "Performing an emergency restart on %s...\n" % compose_job_id(service, args.instance)
    execute_paasta_serviceinit_on_remote_master('restart', args.cluster, service, args.instance)
    print "%s" % "\n".join(paasta_emergency_restart.__doc__.splitlines()[-7:])
    print "Run this to see the status:"
    print "paasta status --service %s --clusters %s" % (service, args.cluster)
