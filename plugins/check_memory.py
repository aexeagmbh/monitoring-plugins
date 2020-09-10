#!/usr/bin/env python3

import nagiosplugin
import psutil
from argparse import ArgumentParser


_memory_types = ["total", "available", "used", "free", "active", "inactive", "buffers", "cached"]


class Memory(nagiosplugin.Resource):
    def probe(self):
        memory = psutil.virtual_memory()
        yield nagiosplugin.Metric('percent', memory.percent, uom='%', min=0, max=100)
        for memory_type in _memory_types:
            yield nagiosplugin.Metric(memory_type, getattr(memory, memory_type), uom='B', min=0, max=memory.total)


class MemorySummary(nagiosplugin.Summary):
    def ok(self, result):
        return "{} memory used".format(result['percent'].metric)

    def problem(self, result):
        return self.ok(result)


@nagiosplugin.guarded
def main():
    argp = ArgumentParser()
    argp.add_argument('-w', '--warning', metavar='RANGE', default='')
    argp.add_argument('-c', '--critical', metavar='RANGE', default='')
    args = argp.parse_args()

    check_parameter = [Memory()]
    check_parameter += [nagiosplugin.ScalarContext(memory_type) for memory_type in _memory_types]
    check_parameter += [nagiosplugin.ScalarContext('percent', args.warning, args.critical)]
    check_parameter += [MemorySummary()]

    check = nagiosplugin.Check(
        *check_parameter
    )
    check.main()


if __name__ == "__main__":
    main()
