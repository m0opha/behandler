import argparse

class HelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action: argparse.Action) -> str:
        if not action.option_strings:
            return super()._format_action_invocation(action)

        if action.nargs == 0:
            return ', '.join(action.option_strings)

        return ', '.join(action.option_strings)

    def _format_args(self, action: argparse.Action, default_metavar: str) -> str:
        return ''
