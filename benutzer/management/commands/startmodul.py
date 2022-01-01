from django.core.management.templates import TemplateCommand
from django.core.management.base import CommandError

import benutzer
import os

class Command(TemplateCommand):
    help = (
        "Creates a Django module directory structure for the given module name in "
        "the current directory or optionally in the given directory. You must provide"
        "a kuerzel and a klassname as keyword arguments to autogenerate a class"
    )
    missing_args_message = "You must provide an module name."
    rewrite_template_suffixes = (
        # Allow shipping invalid .py files without byte-compilation.
        ('.py-tpl', '.py'),
        ('.tpl', '.py'),
    )

    def handle(self, **options):
        app_name = options.pop('name')
        target = options.pop('directory')
        super().handle('app', app_name, target, **options)
        
    def add_arguments(self, parser):
        # Named (optional) arguments
        super().add_arguments(parser)
        parser.add_argument(
            '--kuerzel',
            default='kls',
            help='Kuerzel fÃ¼r Feldnamen'
        )

        parser.add_argument(
            '--klassname',
            default='Klasse',
            help='Klassenname.',
        )

    def handle_template(self, template, subdir):
        if template is None:
            return os.path.join(benutzer.__path__[0], 'management/conf', subdir)
        else:
            if template.startswith('file://'):
                template = template[7:]
            expanded_template = os.path.expanduser(template)
            expanded_template = os.path.normpath(expanded_template)
            if os.path.isdir(expanded_template):
                return expanded_template
            if self.is_url(template):
                # downloads the file and returns the path
                absolute_path = self.download(template)
            else:
                absolute_path = os.path.abspath(expanded_template)
            if os.path.exists(absolute_path):
                return self.extract(absolute_path)

        raise CommandError("couldn't handle %s template %s." %
        (self.app_or_project, template))

                    
                                                                                                                                                   
