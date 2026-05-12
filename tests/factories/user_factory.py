import factory
from faker import Faker

Faker.seed(42)
fake = Faker()


class UserFactory(factory.Factory):
    """Factory for User model"""
    
    class Meta:
        model = dict
    
    id = factory.Sequence(lambda n: n + 1)
    username = factory.LazyFunction(lambda: fake.unique.user_name())
    email = factory.LazyFunction(lambda: fake.unique.email())
    hashed_password = factory.LazyFunction(lambda: fake.password(length=60))
    role = "user"
    created_at = factory.LazyFunction(lambda: fake.date_time_this_year())
    updated_at = factory.LazyFunction(lambda: fake.date_time_this_year())
    created_by = None
    updated_by = None


class AdminUserFactory(UserFactory):
    """Factory for admin users"""
    role = "admin"


class InactiveUserFactory(UserFactory):
    """Factory for inactive users (if needed in future)"""
    role = "user"
