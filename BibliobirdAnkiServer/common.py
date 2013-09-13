
class CollectionInitializer(object):
    def _setup_model(self, col, did):
        """Create the 'External' model used by Bibliobird.com."""
        mm = col.models
        
        m = mm.byName('External')
        if m is None:
            m = mm.new('External')
        m['did'] = did

        # NOTE: Supposedly, Anki will check the first field on any model
        # for uniqueness. Since it's really important to us that the 'External ID'
        # is unique, we're giving that one first!

        fields = mm.fieldNames(m)
        for field_name in ['External ID', 'Front', 'Back']:
            if field_name not in fields:
                fm = mm.newField(field_name)
                mm.addField(m, fm)

        templates = [t['name'] for t in m['tmpls']]

        if 'Forward' not in templates:
            t = mm.newTemplate('Forward')
            t['qfmt'] = '{{Front}}'
            t['afmt'] = '{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}'
            mm.addTemplate(m, t)

        if 'Reverse' not in templates:
            t = mm.newTemplate('Reverse')
            t['qfmt'] = '{{Back}}'
            t['afmt'] = '{{FrontSide}}\n\n<hr id=answer>\n\n{{Front}}'
            mm.addTemplate(m, t)

        if not m['id']:
            mm.add(m)
        else:
            mm.update(m)
    
    def _setup_deck(self, col):
        """Create the 'bibliobird' deck so we can keep our cards seperate."""
        did = col.decks.id('bibliobird', create=True)
        col.decks.flush()
        return did
    
    # NOTE: we accept an optional 'session' argument so this can work as SyncApp hook
    # as well.
    def __call__(self, col, session=None):
        did = self._setup_deck(col)
        self._setup_model(col, did)
        col.save()

