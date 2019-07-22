#
# cron jobs for wazo-purge-db
#

25 3 * * * root /usr/bin/wazo-purge-db > /dev/null
