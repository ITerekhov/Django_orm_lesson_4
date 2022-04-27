from django.db import models 

class Pokemon(models.Model):
    '''Породы покемонов'''
    title = models.CharField('Имя', max_length=200)
    image = models.ImageField('Изображение', null=True, blank=True)
    description = models.TextField('Описание', blank=True)
    title_en = models.CharField('Имя на англисйком', max_length=200, blank=True)
    title_jp = models.CharField('Имя на японском', max_length=200, blank=True)
    previous_evolution = models.ForeignKey("self", on_delete=models.SET_NULL, 
                               related_name='next_evolutions',
                               verbose_name='Предыдущее поколение',
                               null=True,
                               blank=True)
    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    '''Отдельные экземпляры покемонов'''
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE,
                                related_name='endities',
                                verbose_name='Порода покемона')
    lat = models.FloatField('Координаты широты')
    lon = models.FloatField('Координаты долготы')
    appeared_at = models.DateTimeField('Дата появления', null=True, blank=True)
    disappeared_at = models.DateTimeField('Дата исчезновения')
    level = models.IntegerField('Уровень', null=True, blank=True)
    health = models.IntegerField('Здоровье', null=True, blank=True)
    strength = models.IntegerField('Сила', null=True, blank=True)
    defence = models.IntegerField('Защита', null=True, blank=True)
    stamina = models.IntegerField('Выносливость', null=True, blank=True)