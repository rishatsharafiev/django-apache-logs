import re
from datetime import datetime
from typing import Dict, List

import requests
from apps.logger.models import Log
from django.core.management.base import BaseCommand
from tqdm import tqdm


class Command(BaseCommand):
    """Download command"""

    help = 'Download apache logs from external url'

    __pattern = r'(?P<ip_address>(?:[0-9]{1,3}\.){3}[0-9]{1,3})' \
        r'.+(?:\[(?P<date>\d+\/[a-zA-Z]{3}\/\d+):(?P<hour>\d+):(?P<minutes>\d+):(?P<seconds>\d+)'\
        r'\s(?P<timedelta>[\-\+]\w+)\])\s(?:\"(?P<method>.+?)\s(?P<uri>.+?)' \
        r'\s(?P<protocol>.[^\s]*)\")\s(?P<code>\d{3}|\-)\s(?P<size>\d+|\-)'
    __regexp = re.compile(__pattern)

    def add_arguments(self, parser):
        """Add arguments"""
        parser.add_argument(
            '-su',
            '--source_url',
            required=True,
            type=str,
            nargs='?',
            help='Source url'
        )

    def handle(self, *args, **options):
        """Handle command"""
        source_url = options['source_url']

        # remove previous logs
        Log.objects.all().delete()

        # set up line iterator
        iter_logs = self.__iter_logs(url=source_url)
        content_length = next(iter_logs)

        batch_logs = []
        batch_counter = 0
        batch_size = 2000

        with tqdm(total=content_length) as progress_bar:
            for line in iter_logs:
                content, size = line

                # parse line and collect batch logs
                result = self.__parse_line(content)
                if result:
                    groupdict = result.groupdict()
                    groupdict['created_at'] = datetime.strptime(groupdict.get('date'), '%d/%b/%Y').date()
                    batch_logs.append(groupdict)
                    batch_counter += 1
                else:
                    self.stdout.write(self.style.WARNING(f"Can't parse log line: {content}"))

                # batch insert
                if batch_counter == batch_size:
                    self.__batch_insert(logs=batch_logs)
                    batch_counter = 0
                    batch_logs.clear()

                # show progress
                progress_bar.update(size)

            # save edge
            if batch_counter:
                self.__batch_insert(logs=batch_logs)

        self.stdout.write(self.style.SUCCESS('Successfully downloaded!!!'))

    def __iter_logs(self, url: str) -> str:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            response.encoding = 'utf-8'

            yield int(response.headers['Content-length'])

            for line in response.iter_lines(chunk_size=256, decode_unicode=True):
                if line:
                    yield line, len(line)

    def __parse_line(self, line: str) -> Dict:
        return self.__regexp.search(line)

    def __batch_insert(self, logs: List[Dict]):
        Log.objects.bulk_create([
            Log(
                ip_address=log.get('ip_address')[:255],
                created_at=log.get('created_at'),
                method=log.get('method')[:255],
                uri=log.get('uri')[:255],
                code=log.get('code')[:255],
                size=log.get('size') if log.get('size') != "-" else 0,
            ) for log in logs])
