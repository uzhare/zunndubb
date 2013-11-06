# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Attribute'
        db.create_table('attributes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('namespace', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal(u'movies', ['Attribute'])

        # Adding model 'Movie'
        db.create_table('movies', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('imdb_id', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('rating', self.gf('django.db.models.fields.FloatField')()),
            ('plot', self.gf('django.db.models.fields.TextField')()),
            ('rated', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('poster', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('year', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('release_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('progress', self.gf('django.db.models.fields.CharField')(default='not started', max_length=16)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'movies', ['Movie'])

        # Adding M2M table for field attributes on 'Movie'
        db.create_table('movies_attributes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm[u'movies.movie'], null=False)),
            ('attribute', models.ForeignKey(orm[u'movies.attribute'], null=False))
        ))
        db.create_unique('movies_attributes', ['movie_id', 'attribute_id'])

        # Adding model 'IMDBLink'
        db.create_table('imdb_links', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('data', self.gf('django.db.models.fields.TextField')(default='{}', blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'movies', ['IMDBLink'])


    def backwards(self, orm):
        # Deleting model 'Attribute'
        db.delete_table('attributes')

        # Deleting model 'Movie'
        db.delete_table('movies')

        # Removing M2M table for field attributes on 'Movie'
        db.delete_table('movies_attributes')

        # Deleting model 'IMDBLink'
        db.delete_table('imdb_links')


    models = {
        u'movies.attribute': {
            'Meta': {'object_name': 'Attribute', 'db_table': "'attributes'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'namespace': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'movies.imdblink': {
            'Meta': {'object_name': 'IMDBLink', 'db_table': "'imdb_links'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'movies.movie': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Movie', 'db_table': "'movies'"},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['movies.Attribute']", 'symmetrical': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_id': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'plot': ('django.db.models.fields.TextField', [], {}),
            'poster': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'progress': ('django.db.models.fields.CharField', [], {'default': "'not started'", 'max_length': '16'}),
            'rated': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'rating': ('django.db.models.fields.FloatField', [], {}),
            'release_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['movies']