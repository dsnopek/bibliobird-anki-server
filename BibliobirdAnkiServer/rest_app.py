
import os

from AnkiServer.apps.rest_app import RestHandlerBase, RestApp
from BibliobirdAnkiServer.common import CollectionInitializer

class CollectionHandler(RestHandlerBase):
    """Custom collection funtions for Bibliobird."""

    def resync_notes(self, col, req):
        # build a fast lookup table
        lookup = dict([(id, True) for id in req.data.get('external_ids', [])])

        remove = []

        # Loop through all the notes on the 'bibliobird' deck - adding any to the
        # remove list which aren't on the lookup table, and pruning all the ids
        # that we've found from the lookup table (leaving only the missing ids)
        for nid in col.findNotes('deck:"bibliobird"'):
            note = col.getNote(nid)
            try:
                id = note['External ID']
            except:
                id = False

            # Remove any notes with no 'External ID'
            if not id:
                remove.append(nid)
                continue

            # Remove any notes which can't be found in the lookup list
            if not lookup.has_key(id):
                remove.append(nid)
            else:
                del lookup[id]

        # Remove all the notes on the remove list
        col.remNotes(remove)

        # Return the missing list
        return {'missing': lookup.keys()}

# Our entry point
def make_app(global_conf, **local_conf):
    # setup the logger (copied from AnkiServer.apps.rest_app.make_app())
    from AnkiServer.utils import setup_logging
    setup_logging(local_conf.get('logging.config_file'))

    setup_collection = CollectionInitializer()

    app = RestApp(
        data_root=local_conf['data_root'],
        allowed_hosts=local_conf.get('allowed_hosts', '127.0.0.1'),
        setup_new_collection=setup_collection,
        hook_pre_execute=setup_collection
    )

    app.add_handler_group('collection', CollectionHandler())

    return app

