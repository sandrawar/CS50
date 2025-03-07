# Generated by Django 3.2 on 2021-04-22 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=64)),
                ('description', models.TextField()),
                ('bid', models.DecimalField(decimal_places=2, max_digits=5)),
                ('photo', models.URLField(blank=True)),
                ('category', models.TextField(choices=[('Fashion', 'Fashion'), ('Toys', 'Toys'), ('Electronics', 'Electronics'), ('Home', 'Home'), ('Books', 'Books')])),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='listings',
            field=models.ManyToManyField(blank=True, related_name='owner', to='auctions.Listing'),
        ),
    ]
