from django.core.management.base import BaseCommand

from main.resume import write_pdf


class Command(BaseCommand):
    help = 'Перегенерирует резюме (PDF) из контента CMS.'

    def handle(self, *args, **options):
        path = write_pdf()
        self.stdout.write(self.style.SUCCESS(f'Резюме записано: {path}'))