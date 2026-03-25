from django.utils.text import slugify


def generate_unique_slug(instance, value, slug_field_name='slug', max_length=120):
    base_slug = slugify(value)[:max_length] or 'item'
    slug = base_slug
    model_class = instance.__class__
    counter = 2

    while model_class.objects.filter(**{slug_field_name: slug}).exclude(pk=instance.pk).exists():
        suffix = f'-{counter}'
        slug = f'{base_slug[: max_length - len(suffix)]}{suffix}'
        counter += 1

    return slug
