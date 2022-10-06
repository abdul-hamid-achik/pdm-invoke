import argparse
import subprocess
import sys

from pdm.cli.utils import PdmFormatter
from pdm.cli.commands.base import BaseCommand
from pdm.cli.commands.run import Command as RunCommand
from pdm.cli.commands.run import TaskRunner
from pdm.cli.hooks import HookManager
from pdm.cli.options import skip_option
from pdm.cli.utils import check_project_file


class InvokeCommand(RunCommand):
  OPTIONS = []
  COMMAND_PREFIX = ['inv']

  def add_arguments(self, parser):
    skip_option.add_to_parser(parser)
    parser.add_argument(
      "args",
      nargs=argparse.REMAINDER,
      help="Arguments that will be passed to the command",
    )

  def handle(self, project, options):
    options.list = False
    options.command = self.COMMAND_PREFIX[0]

    check_project_file(project)
    hooks = HookManager(project, options.skip)
    runner = TaskRunner(project, hooks=hooks)
    sys.exit(runner.run(options.command, self.COMMAND_PREFIX[1:] + options.args))

    hooks.try_emit("pre_run", script=options.command, args=options.args)
    exit_code = runner.run(options.command, self.COMMAND_PREFIX[1:] + options.args)
    hooks.try_emit("post_run", script=options.command, args=options.args)
    sys.exit(exit_code)


def reg_commands(core):
  core.register_command(InvokeCommand, "inv")
