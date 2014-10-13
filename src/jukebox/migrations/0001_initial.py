# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'WebPath'
        db.create_table('jukebox_webpath', (
            ('url', self.gf('django.db.models.fields.TextField')()),
            ('failed', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('checked', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('root', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jukebox.WebPath'], null=True, blank=True)),
        ))
        db.send_create_signal('jukebox', ['WebPath'])

        # Adding model 'MusicFile'
        db.create_table('jukebox_musicfile', (
            ('album', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('trackLength', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jukebox.WebPath'])),
            ('artist', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.TextField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('failed', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('got_metadata', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('trackNumber', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('jukebox', ['MusicFile'])

        # Adding model 'ChatItem'
        db.create_table('jukebox_chatitem', (
            ('info', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jukebox.MusicFile'], null=True, blank=True)),
            ('what', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('who', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('jukebox', ['ChatItem'])

        # Adding model 'QueueItem'
        db.create_table('jukebox_queueitem', (
            ('index', self.gf('django.db.models.fields.FloatField')()),
            ('what', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jukebox.MusicFile'])),
            ('who', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('jukebox', ['QueueItem'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'WebPath'
        db.delete_table('jukebox_webpath')

        # Deleting model 'MusicFile'
        db.delete_table('jukebox_musicfile')

        # Deleting model 'ChatItem'
        db.delete_table('jukebox_chatitem')

        # Deleting model 'QueueItem'
        db.delete_table('jukebox_queueitem')
    
    
    models = {
        'jukebox.chatitem': {
            'Meta': {'object_name': 'ChatItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jukebox.MusicFile']", 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'what': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'who': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'jukebox.musicfile': {
            'Meta': {'object_name': 'MusicFile'},
            'album': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'failed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'got_metadata': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jukebox.WebPath']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'trackLength': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trackNumber': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        'jukebox.queueitem': {
            'Meta': {'object_name': 'QueueItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.FloatField', [], {}),
            'what': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jukebox.MusicFile']"}),
            'who': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'jukebox.webpath': {
            'Meta': {'object_name': 'WebPath'},
            'checked': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'failed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jukebox.WebPath']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {})
        }
    }
    
    complete_apps = ['jukebox']
