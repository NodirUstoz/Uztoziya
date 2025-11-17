from django.core.management.base import BaseCommand
from tests.models import TestCategory


class Command(BaseCommand):
    help = 'Create default test categories'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'Matematika',
                'description': 'Matematika fanidan testlar'
            },
            {
                'name': 'Fizika',
                'description': 'Fizika fanidan testlar'
            },
            {
                'name': 'Kimyo',
                'description': 'Kimyo fanidan testlar'
            },
            {
                'name': 'Biologiya',
                'description': 'Biologiya fanidan testlar'
            },
            {
                'name': 'Geografiya',
                'description': 'Geografiya fanidan testlar'
            },
            {
                'name': 'Tarix',
                'description': 'Tarix fanidan testlar'
            },
            {
                'name': 'Adabiyot',
                'description': 'Adabiyot fanidan testlar'
            },
            {
                'name': 'Ingliz tili',
                'description': 'Ingliz tili fanidan testlar'
            },
            {
                'name': 'Rus tili',
                'description': 'Rus tili fanidan testlar'
            },
            {
                'name': 'Informatika',
                'description': 'Informatika fanidan testlar'
            },
            {
                'name': 'Umumiy',
                'description': 'Umumiy bilim testlari'
            }
        ]

        created_count = 0
        for category_data in categories:
            category, created = TestCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new categories')
        )
