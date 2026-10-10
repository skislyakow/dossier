from django.core.management.base import BaseCommand

from main.audit import audit_content


class Command(BaseCommand):
    help = 'Проверяет связку тегов проектов и навыков (кликабельность секции Skills).'

    def handle(self, *args, **options):
        errors, warnings = audit_content()
        for warning in warnings:
            self.stdout.write(self.style.WARNING('W101: ' + warning))
        for error in errors:
            self.stdout.write(self.style.ERROR('E100: ' + error))
        if errors:
            self.stdout.write(self.style.NOTICE(
                '%d предупреждений, %d ошибок' % (len(warnings), len(errors)),
            ))
            raise SystemExit(1)
        if warnings:
            self.stdout.write(self.style.NOTICE(
                '%d предупреждений (не критично)' % len(warnings),
            ))
            return
        self.stdout.write(self.style.SUCCESS('Контент согласован: теги ↔ навыки'))