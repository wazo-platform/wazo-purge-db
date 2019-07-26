# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

archive_file = '/tmp/wazo_purge_db.archive'
purger_file = '/tmp/wazo_purge_db.purge'


def archive_plugin(config):
    with open(archive_file, 'w') as output:
        output.write(
            'Save tables before purge. {0} days to keep!'.format(config['days_to_keep'])
        )


class PurgePlugin:
    @staticmethod
    def purge(days_to_keep, session):
        with open(purger_file, 'w') as output:
            output.write('Purged, {0} days keeped!'.format(days_to_keep))
