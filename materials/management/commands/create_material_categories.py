from django.core.management.base import BaseCommand
from materials.models import MaterialCategory


class Command(BaseCommand):
    help = 'Create default material categories'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'Matematika',
                'description': 'Matematika fanidan materiallar',
                'icon': 'fa-calculator'
            },
            {
                'name': 'Fizika',
                'description': 'Fizika fanidan materiallar',
                'icon': 'fa-atom'
            },
            {
                'name': 'Kimyo',
                'description': 'Kimyo fanidan materiallar',
                'icon': 'fa-flask'
            },
            {
                'name': 'Biologiya',
                'description': 'Biologiya fanidan materiallar',
                'icon': 'fa-dna'
            },
            {
                'name': 'Geografiya',
                'description': 'Geografiya fanidan materiallar',
                'icon': 'fa-globe'
            },
            {
                'name': 'Tarix',
                'description': 'Tarix fanidan materiallar',
                'icon': 'fa-landmark'
            },
            {
                'name': 'Adabiyot',
                'description': 'Adabiyot fanidan materiallar',
                'icon': 'fa-book'
            },
            {
                'name': 'Ingliz tili',
                'description': 'Ingliz tili fanidan materiallar',
                'icon': 'fa-language'
            },
            {
                'name': 'Rus tili',
                'description': 'Rus tili fanidan materiallar',
                'icon': 'fa-language'
            },
            {
                'name': 'Informatika',
                'description': 'Informatika fanidan materiallar',
                'icon': 'fa-laptop-code'
            },
            {
                'name': 'Umumiy',
                'description': 'Umumiy materiallar',
                'icon': 'fa-folder'
            }
        ]

        created_count = 0
        for category_data in categories:
            category, created = MaterialCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description'],
                    'icon': category_data['icon']
                }
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


