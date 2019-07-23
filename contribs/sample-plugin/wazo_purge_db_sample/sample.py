# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

sample_file = '/tmp/wazo_purge_db.sample'


def sample_plugin(config):
    with open(sample_file, 'w') as output:
        output.write(
            'Save tables before purge. {0} days to keep!'.format(config['days_to_keep'])
        )
