import factory
from faker import Faker

Faker.seed(42)
fake = Faker()


class ArtistFactory(factory.Factory):
    """Factory for Artist model"""
    
    class Meta:
        model = dict
    
    id = factory.Sequence(lambda n: n + 1)
    name = factory.LazyFunction(lambda: fake.unique.name())
    created_at = factory.LazyFunction(lambda: fake.date_time_this_year())
    updated_at = factory.LazyFunction(lambda: fake.date_time_this_year())
    created_by = factory.LazyFunction(lambda: fake.user_name())
    updated_by = factory.LazyFunction(lambda: fake.user_name())
