# Copyright 2015-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

archive_file = '/tmp/wazo_purge_db.archive'
purger_file = '/tmp/wazo_purge_db.purge'


def archive_plugin(config):
    with open(archive_file, 'w') as output:
        output.write(
            f'Save tables before purge. {config["days_to_keep"]} days to keep!'
        )


class PurgePlugin:
    @staticmethod
    def purge(days_to_keep, session):
        with open(purger_file, 'w') as output:
            output.write(f'Purged, {days_to_keep} days keeped!')
