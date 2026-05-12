import factory
from datetime import datetime, timedelta
from faker import Faker

Faker.seed(42)
fake = Faker()


class RefreshTokenFactory(factory.Factory):
    """Factory for RefreshToken model"""
    
    class Meta:
        model = dict
    
    id = factory.Sequence(lambda n: n + 1)
    jti = factory.LazyFunction(lambda: fake.uuid4())
    user_id = factory.Sequence(lambda n: n + 1)
    expires_at = factory.LazyFunction(lambda: datetime.utcnow() + timedelta(days=7))
    revoked = False
    created_at = factory.LazyFunction(lambda: fake.date_time_this_year())
    updated_at = factory.LazyFunction(lambda: fake.date_time_this_year())
    created_by = None
    updated_by = None


class RevokedRefreshTokenFactory(RefreshTokenFactory):
    """Factory for revoked refresh tokens"""
    revoked = True


class ExpiredRefreshTokenFactory(RefreshTokenFactory):
    """Factory for expired refresh tokens"""
    expires_at = factory.LazyFunction(lambda: datetime.utcnow() - timedelta(days=1))
