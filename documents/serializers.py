from documents.models import Document, Page
from rest_framework import serializers


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    # page_set = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='page-set', lookup_field='document')

    class Meta:
        model = Document
        fields = (
            'id', 'name', 'url', 'course', 'description',
            'user', 'pages', 'date', 'views',
            'downloads', 'state', 'md5',
        )

        extra_kwargs = {
            'user': {'lookup_field': 'netid'},
            'course': {'lookup_field': 'slug'},
        }


class ShortDocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'url', 'course')


class PageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Page
        fields = (
            'document', 'numero', 'bitmap_120',
            'bitmap_600', 'bitmap_900', 'height_120',
            'height_600', 'height_900',
        )

        extra_kwargs = {
            'user': {'lookup_field': 'netid'},
        }