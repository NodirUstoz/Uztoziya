from django.core.management.base import BaseCommand
from materials.models import MaterialCategory
from tests.models import TestCategory


class Command(BaseCommand):
    help = 'Create all default categories (materials and tests)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating Material Categories...'))
        
        material_categories = [
            {'name': 'Matematika', 'description': 'Matematika fanidan materiallar', 'icon': 'fa-calculator'},
            {'name': 'Fizika', 'description': 'Fizika fanidan materiallar', 'icon': 'fa-atom'},
            {'name': 'Kimyo', 'description': 'Kimyo fanidan materiallar', 'icon': 'fa-flask'},
            {'name': 'Biologiya', 'description': 'Biologiya fanidan materiallar', 'icon': 'fa-dna'},
            {'name': 'Geografiya', 'description': 'Geografiya fanidan materiallar', 'icon': 'fa-globe'},
            {'name': 'Tarix', 'description': 'Tarix fanidan materiallar', 'icon': 'fa-landmark'},
            {'name': 'Adabiyot', 'description': 'Adabiyot fanidan materiallar', 'icon': 'fa-book'},
            {'name': 'Ingliz tili', 'description': 'Ingliz tili fanidan materiallar', 'icon': 'fa-language'},
            {'name': 'Rus tili', 'description': 'Rus tili fanidan materiallar', 'icon': 'fa-language'},
            {'name': 'Informatika', 'description': 'Informatika fanidan materiallar', 'icon': 'fa-laptop-code'},
            {'name': 'Umumiy', 'description': 'Umumiy materiallar', 'icon': 'fa-folder'}
        ]

        material_count = 0
        for category_data in material_categories:
            category, created = MaterialCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description'],
                    'icon': category_data.get('icon', '')
                }
            )
            if created:
                material_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {category.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Exists: {category.name}'))

        self.stdout.write(self.style.SUCCESS(f'\nCreated {material_count} new material categories\n'))
        
        # Test Categories
        self.stdout.write(self.style.SUCCESS('Creating Test Categories...'))
        
        test_categories = [
            {'name': 'Matematika', 'description': 'Matematika fanidan testlar'},
            {'name': 'Fizika', 'description': 'Fizika fanidan testlar'},
            {'name': 'Kimyo', 'description': 'Kimyo fanidan testlar'},
            {'name': 'Biologiya', 'description': 'Biologiya fanidan testlar'},
            {'name': 'Geografiya', 'description': 'Geografiya fanidan testlar'},
            {'name': 'Tarix', 'description': 'Tarix fanidan testlar'},
            {'name': 'Adabiyot', 'description': 'Adabiyot fanidan testlar'},
            {'name': 'Ingliz tili', 'description': 'Ingliz tili fanidan testlar'},
            {'name': 'Rus tili', 'description': 'Rus tili fanidan testlar'},
            {'name': 'Informatika', 'description': 'Informatika fanidan testlar'},
            {'name': 'Umumiy', 'description': 'Umumiy bilim testlari'}
        ]

        test_count = 0
        for category_data in test_categories:
            category, created = TestCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            if created:
                test_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {category.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Exists: {category.name}'))

        self.stdout.write(self.style.SUCCESS(f'\nCreated {test_count} new test categories\n'))
        
        self.stdout.write(self.style.SUCCESS(
            f'Setup complete! Total: {material_count + test_count} new categories created.'
        ))


