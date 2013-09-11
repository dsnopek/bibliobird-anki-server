# -*- coding: utf-8 -*-
# Copyright: David Snopek <dsnopek@gmail.com>
# License: GNU Affero GPL, version 3 or later; http://www.gnu.org/copyleft/agpl-3.0.html
#
# Sync decks to BiblioBird.com instead of AnkiWeb.
#
# This allows BiblioBird users to access a special "bibliobird" deck, which
# contains flashcards for all the words in their "Words I Am Learning" list
# on BiblioBird.com.  Changes on BiblioBird will automatically be sync'ed to
# this deck and vice-a-versa.
#
# You can also sync any other decks you like to BiblioBird -- for the time 
# being, there are no restrictions what-so-ever.
#

import anki.consts, anki.sync

# production
anki.consts.SYNC_URL = anki.sync.SYNC_URL = 'http://anki.bibliobird.com/sync/'
# development
#anki.consts.SYNC_URL = anki.sync.SYNC_URL = 'http://172.31.31.10:27701/sync/'

# Monkey patch the "_" function to replace the "Create free account" links.
# TODO: There are probably better ways to do this but this was the easiest!
def monkeyPatchTranslations():
    # get the translation function (is actually ankiqt.ui.main.AnkiQt.getTranslation())
    import __builtin__
    orig_t = __builtin__.__dict__['_']

    replacements = [
        ('<a href="%s">', '<a href="http://www.bibliobird.com/user"><!--%s-->'),
        ('AnkiWeb', 'Bibliobird')
    ]

    def t(s):
        s = orig_t(s)
        for match, replace in replacements:
            s = s.replace(match, replace)
        return s

    # only replace where its needed!
    import aqt.sync, aqt.toolbar 
    aqt.sync._ = aqt.toolbar._ = t

monkeyPatchTranslations()

