#!/usr/bin/env python3

from argparse import ArgumentParser
import docker
import json
import nagiosplugin


def get_active_minions():
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    docker_exec = client.exec_create('salt-master', 'salt-run --out json manage.up', stderr=False)
    result = client.exec_start(docker_exec['Id'])
    return json.loads(result)


class DeadMinions(nagiosplugin.Resource):
    def __init__(self, expected_minions):
        self.expected_minions = expected_minions
        self.active_minions = None

    def probe(self):
        active_minions = get_active_minions()
        self.dead_minions = set(self.expected_minions) - set(active_minions)
        return nagiosplugin.Metric('dead minions', len(self.dead_minions), min=0)


class DeadMinionsSummary(nagiosplugin.Summary):
    def ok(self, result):
        return "All salt minions are alive"

    def problem(self, results):
        result = results['dead minions']
        dead_minions = result.resource.dead_minions
        return "{} minions are not connected to the salt master: {}".format(
            len(dead_minions),
            ", ".join(dead_minions)
        )


@nagiosplugin.guarded
def main():
    argp = ArgumentParser()
    argp.add_argument('-w', '--warning', metavar='RANGE', default='')
    argp.add_argument('-c', '--critical', metavar='RANGE', default='0')
    argp.add_argument('expected_minions', nargs='*')
    args = argp.parse_args()

    check = nagiosplugin.Check(
        DeadMinions(args.expected_minions),
        nagiosplugin.ScalarContext('dead minions', args.warning, args.critical),
        DeadMinionsSummary()
    )
    check.main()


if __name__ == "__main__":
    main()
