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
        emails = Uploads.objects.values_list('email_changer', flat=True).distinct()
        for email in emails.exclude(email_changer__in=blacklist): #does this matter
            first_ul = Uploads.objects.filter(email_changer=email).order_by('timestamp')[0]
            last_ul = Uploads.objects.filter(email_changer=email).order_by('timestamp').reverse()[0]
            obj, created = People.objects.get_or_create(email=email,
                                                        defaults={
                                                        'name':last_ul.name_changer,
                                                        'email':last_ul.email_changer,
                                                        'first_upload':first_ul,
                                                        'last_upload':last_ul
                                                        })

    def check_is_active(self):
        for p in People.objects.all():
            last_ul = Uploads.objects.filter(email_changer=p.email).order_by('timestamp').reverse()[0].timestamp
            cutoff_date = timezone.now()-timedelta(days=4*30)
            if last_ul < cutoff_date and p.is_active is not False:
                p.is_active = False
                p.save()
            elif last_ul > cutoff_date and p.is_active is not True:
                p.is_active = True
                p.save()

    def total_uploads(self):
        for p in People.objects.all():
            all_uploads = Uploads.objects.filter(email_changer=p.email)
            total_uploads = len(all_uploads)
            if p.total_uploads != total_uploads:
                p.total_uploads = total_uploads
                p.save()

    def last_seen(self):
        for p in People.objects.all():
            last_ul = Uploads.objects.filter(email_changer=p.email).order_by('timestamp').reverse()[0]
            if p.last_upload != last_ul:
                p.last_upload = last_ul
                p.save()

    def is_debian_dev(self):
        launchpad = lp('d-a-t', anonymous=True, lp_service='production')
        debian_devs = [a.name for a in launchpad.people['ubuntu-dev'].participants] #alternative?
        #separate management command to see if debian 
        for p in People.objects.all():
            if p.email in debian_devs and p.debian_dev is not True:
                p.debian_dev = True
                p.save()
            elif p.email not in debian_devs and p.debian_dev is not False:
                p.debian_dev = False
                p.save()

    def handle_noargs(self, **options):
        self.import_people()
        self.check_is_active()
        self.total_uploads()
        self.last_seen()
        self.is_debian_dev()
