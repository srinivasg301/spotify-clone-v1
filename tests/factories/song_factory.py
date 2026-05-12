import factory
from faker import Faker

Faker.seed(42)
fake = Faker()


class SongFactory(factory.Factory):
    """Factory for Song model"""
    
    class Meta:
        model = dict
    
    id = factory.Sequence(lambda n: n + 1)
    title = factory.LazyFunction(lambda: fake.sentence(nb_words=3).rstrip('.'))
    artist_id = factory.Sequence(lambda n: n + 1)
    album = factory.LazyFunction(lambda: fake.sentence(nb_words=2).rstrip('.'))
    duration = factory.LazyFunction(lambda: fake.random_int(min=60, max=600))
    thumbnail_url = factory.LazyFunction(lambda: fake.image_url())
    created_at = factory.LazyFunction(lambda: fake.date_time_this_year())
    updated_at = factory.LazyFunction(lambda: fake.date_time_this_year())
    created_by = factory.LazyFunction(lambda: fake.user_name())
    updated_by = factory.LazyFunction(lambda: fake.user_name())


class SongWithoutAlbumFactory(SongFactory):
    """Factory for songs without album"""
    album = None


class SongWithoutThumbnailFactory(SongFactory):
    """Factory for songs without thumbnail"""
    thumbnail_url = None
