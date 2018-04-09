from django.core.management.commands.shell import Command as DjangoCommand
from ptpython.repl import embed, run_config
from importlib import import_module
import os


IMPORTED_MODULES = (
    ( 'amod', 'account.models' ),
)


class Command(DjangoCommand):
    '''Makes `ptpython` the default Django shell'''
    shells = [ 'ptpython' ] + DjangoCommand.shells

    def ptpython(self, options):
        history_filename = os.path.expanduser('~/.ptpython_history')

        # globals and locals for the shell
        globals_dict = {}
        for name, mod in IMPORTED_MODULES:
            globals_dict[name] = import_module(mod)
        locals_dict = {}

        # start the interpreter
        embed(globals_dict, locals_dict, history_filename=history_filename, configure=run_config)
