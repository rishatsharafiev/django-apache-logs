from django.core.management.base import BaseCommand, CommandError
import requests
import re
from apps.logger.models import Log
from tqdm import tqdm
from typing import List, Dict
from datetime import datetime


class Command(BaseCommand):
    help = 'Download apache logs from external url'
    pattern = r'(?P<ip_address>(?:[0-9]{1,3}\.){3}[0-9]{1,3}).+(?:\[(?P<date>\d+\/[a-zA-Z]{3}\/\d+):(?P<hour>\d+):(?P<minutes>\d+):(?P<seconds>\d+)\s(?P<timedelta>[\-\+]\w+)\])\s(?:\"(?P<method>.+?)\s(?P<uri>.+?)\s(?P<protocol>.[^\s]*)\")\s(?P<code>\d{3}|\-)\s(?P<size>\d+|\-)'
    regexp = re.compile(pattern)

    def add_arguments(self, parser):
        parser.add_argument(
            '-su',
            '--source_url', 
            required=True, 
            type=str, 
            nargs='?', 
            help='Source url'
        )

    def handle(self, *args, **options):
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
                    # run logger
                    pass
                
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

    def __iter_logs(self, url: str) -> str:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            yield int(response.headers['Content-length'])

            for line in response.iter_lines(chunk_size=256, decode_unicode=True):
                if line:
                    yield line, len(line)

    def __parse_line(self, line: str) -> Dict:
        return self.regexp.search(line)

    def __batch_insert(self, logs: List[Dict]):
        Log.objects.bulk_create([
            Log(
                ip_address=log.get('ip_address'),
                created_at=log.get('created_at'),
                method=log.get('method')[:255],
                uri=log.get('uri'),
                code=log.get('code') if log.get('code') != "-" else 0,
                size=log.get('size') if log.get('size') != "-" else 0,
            ) for log in logs])
