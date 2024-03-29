import argparse
import sys

from pdm.cli.commands.run import Command as RunCommand
from pdm.cli.commands.run import TaskRunner
from pdm.cli.hooks import HookManager
from pdm.cli.options import skip_option
from pdm.cli.utils import check_project_file


class Command(RunCommand):
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
    hooks.try_emit("pre_run", script=options.command, args=options.args)
    exit_code = runner.run(options.command, self.COMMAND_PREFIX[1:] + options.args)
    hooks.try_emit("post_run", script=options.command, args=options.args)
    sys.exit(exit_code)


class InvCommand(Command):
  COMMAND_PREFIX = ['inv']


class InvokeCommand(Command):
  COMMAND_PREFIX = ['invoke']


def reg_commands(core):
  core.register_command(InvCommand, "inv")
  core.register_command(InvokeCommand, "invoke")
