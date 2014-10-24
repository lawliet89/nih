# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ChatItem.who'
        db.alter_column('jukebox_chatitem', 'who', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ChatItem.who'
        raise RuntimeError("Cannot reverse this migration. 'ChatItem.who' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'ChatItem.who'
        db.alter_column('jukebox_chatitem', 'who', self.gf('django.db.models.fields.CharField')(max_length=200))

    models = {
        'jukebox.chatitem': {
            'Meta': {'ordering': "['-when']", 'object_name': 'ChatItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jukebox.MusicFile']", 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'what': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'who': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'jukebox.musicfile': {
            'Meta': {'object_name': 'MusicFile'},
            'album': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'failed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'got_metadata': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jukebox.WebPath']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'trackLength': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trackNumber': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        'jukebox.queueitem': {
            'Meta': {'ordering': "['index']", 'object_name': 'QueueItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.FloatField', [], {}),
            'what': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jukebox.MusicFile']"}),
            'who': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'jukebox.webpath': {
            'Meta': {'object_name': 'WebPath'},
            'checked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'failed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jukebox.WebPath']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['jukebox']