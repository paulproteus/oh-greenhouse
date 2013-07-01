from uploads.models import Uploads, People
from django.core.management.base import NoArgsCommand
from datetime import timedelta
from django.utils import timezone
from uploads.common.launchpad import lp_login as lp

class Command(NoArgsCommand):
    help = "Create entry in people table if new LP id is found in uploads table."

    def import_people(self):
        blacklist = ['katie', 'ps-jenkins', 'ubuntu-langpack',
                     'kubuntu-members', '']
        lpids = Uploads.objects.values_list('lpid_changer', flat=True).distinct()
        for lpid in lpids.exclude(lpid_changer__in=blacklist):
            ul = Uploads.objects.filter(lpid_changer=lpid).order_by('timestamp')[0]
            last_ul = Uploads.objects.filter(lpid_changer=lpid).order_by('timestamp').reverse()[0]
            obj, created = People.objects.get_or_create(lpid=lpid,
                                                        defaults={
                                                        'name':last_ul.name_changer,
                                                        'email':last_ul.email_changer,
                                                        'first_upload':ul,
                                                        'last_upload':last_ul
                                                        })

    def check_is_active(self):
        for p in People.objects.all():
            last_ul = Uploads.objects.filter(lpid_changer=p.lpid).order_by('timestamp').reverse()[0].timestamp
            cutoff_date = timezone.now()-timedelta(days=4*30)
            if last_ul < cutoff_date and p.is_active is not False:
                p.is_active = False
                p.save()
            elif last_ul > cutoff_date and p.is_active is not True:
                p.is_active = True
                p.save()

    def total_uploads(self):
        for p in People.objects.all():
            all_uploads = Uploads.objects.filter(lpid_changer=p.lpid)
            total_uploads = len(all_uploads)
            if p.total_uploads != total_uploads:
                p.total_uploads = total_uploads
                p.save()

    def last_seen(self):
        for p in People.objects.all():
            last_ul = Uploads.objects.filter(lpid_changer=p.lpid).order_by('timestamp').reverse()[0]
            if p.last_upload != last_ul:
                p.last_upload = last_ul
                p.save()

    def is_ubuntu_dev(self):
        launchpad = lp('d-a-t', anonymous=True, lp_service='production')
        ubuntu_devs = [a.name for a in launchpad.people['ubuntu-dev'].participants]
        for p in People.objects.all():
            if p.lpid in ubuntu_devs and p.ubuntu_dev is not True:
                p.ubuntu_dev = True
                p.save()
            elif p.lpid not in ubuntu_devs and p.ubuntu_dev is not False:
                p.ubuntu_dev = False
                p.save()

    def handle_noargs(self, **options):
        self.import_people()
        self.check_is_active()
        self.total_uploads()
        self.last_seen()
        self.is_ubuntu_dev()
