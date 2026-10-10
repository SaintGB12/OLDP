"""Create a few clearly-labelled FAKE cases to validate the DB -> search pipeline.

Usage:
    python manage.py import_test_cases

Idempotent: re-running updates the same rows (matched by slug / court code).
"""

from django.core.management.base import BaseCommand

from oldp.apps.cases.models import Case
from oldp.apps.courts.models import Country, Court, State
from oldp.apps.sources.models import Source

TEST_CASES = [
    {
        "slug": "test-ma-cassation-2024-001",
        "file_number": "TEST-001/2024",
        "date": "2024-03-12",
        "type": "Arrêt",
        "title": "[TEST] Arrêt fictif - responsabilité contractuelle",
        "content": "<p>[DONNÉES DE TEST] Arrêt fictif relatif à la responsabilité "
        "contractuelle et à l'indemnisation du préjudice.</p>"
        "<p>قرار تجريبي وهمي يتعلق بالمسؤولية العقدية والتعويض عن الضرر.</p>",
    },
    {
        "slug": "test-ma-cassation-2024-002",
        "file_number": "TEST-002/2024",
        "date": "2024-05-20",
        "type": "Arrêt",
        "title": "[TEST] Arrêt fictif - bail commercial",
        "content": "<p>[DONNÉES DE TEST] Arrêt fictif en matière de bail commercial "
        "et de résiliation.</p><p>قرار تجريبي وهمي في مادة الكراء التجاري.</p>",
    },
    {
        "slug": "test-ma-cassation-2024-003",
        "file_number": "TEST-003/2024",
        "date": "2024-09-02",
        "type": "Jugement",
        "title": "[TEST] Jugement fictif - droit de la famille",
        "content": "<p>[DONNÉES DE TEST] Jugement fictif en droit de la famille "
        "(pension alimentaire).</p><p>حكم تجريبي وهمي في قضايا الأسرة (النفقة).</p>",
    },
]


class Command(BaseCommand):
    help = "Import 3 fake (TEST) cases to validate indexing and search."

    def handle(self, *args, **options):
        country, _ = Country.objects.get_or_create(code="ma", defaults={"name": "Maroc"})
        state, _ = State.objects.get_or_create(
            slug="maroc", defaults={"name": "Maroc", "country": country}
        )
        court, _ = Court.objects.get_or_create(
            code="TESTMA",
            defaults={
                "name": "[TEST] Cour de cassation (fictive)",
                "slug": "test-cour-cassation-ma",
                "state": state,
                "court_type": "CC",
                "jurisdiction": "Ordinaire",
                "level_of_appeal": "Cassation",
            },
        )
        source, _ = Source.objects.get_or_create(
            name="TEST data",
            defaults={"homepage": "http://localhost:8000/", "private": False},
        )

        for item in TEST_CASES:
            data = dict(item)
            slug = data.pop("slug")
            case, created = Case.objects.update_or_create(
                slug=slug,
                defaults={
                    **data,
                    "court": court,
                    "source": source,
                    "source_url": "http://localhost:8000/test/%s" % slug,
                    "review_status": "accepted",
                },
            )
            self.stdout.write("%s %s" % ("created" if created else "updated", case.slug))
