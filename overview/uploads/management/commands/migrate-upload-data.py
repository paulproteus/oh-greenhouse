from django.core.management.base import NoArgsCommand
from django.core.exceptions import ObjectDoesNotExist
from uploads.common.launchpad import lp_login as lp
from django.db import connections
from uploads.models import Uploads

class Command(NoArgsCommand):
    help = "Migrate upload data from UDD to django managed database."

    def import_uploads(self):
        cursor = connections['udd'].cursor()
        sql = """SELECT date, distribution, source, version, changed_by_name,
                 changed_by_email, signed_by_name, signed_by_email
                 FROM ubuntu_upload_history ORDER BY date"""
        cursor.execute(sql)
        bulk_insert = []
        try:
            t = 'timestamp'
            latest_entry = Uploads.objects.values(t).latest(t)[t]
        except ObjectDoesNotExist:
            latest_entry = None
        for row in cursor.fetchall():
            if latest_entry is None or row[0] > latest_entry:
                if row[4] == row[6] or row[5] == row[7]:
                    spon_email = ''
                    spon_name = ''
                else:
                    spon_name = row[6]
                    spon_email = row[7]
                uploads = Uploads(timestamp=row[0], release=row[1],
                                  package=row[2], version=row[3],
                                  name_changer=row[4], email_changer=row[5],
                                  name_sponsor=spon_name, email_sponsor=spon_email,
                                  lpid_changer='' ,lpid_sponsor='')
                bulk_insert.append(uploads)
        Uploads.objects.bulk_create(bulk_insert)

    def add_lpids(self):
        self.launchpad = lp('d-a-t', anonymous=True, lp_service='production')

        changer_emails = Uploads.objects.values_list('email_changer',
                                                     flat=True).distinct()
        for e in changer_emails:
            uploads = Uploads.objects.filter(email_changer=e)
            if uploads[0].lpid_changer == '' and (uploads[0].email_changer not in ('', 'N/A')):
                lpid = self.email_to_lp(e)
                if lpid != '':
                    for ul in uploads.filter(lpid_changer=''):
                        ul.lpid_changer = lpid
                        ul.save()
            else:
                for ul in uploads.filter(lpid_changer=''):
                    if ul.email_changer not in ('', 'N/A'):
                        ul.lpid_changer = uploads[0].lpid_changer
                        ul.save()

        sponsor_emails = Uploads.objects.values_list('email_sponsor',
                                                     flat=True).distinct()
        for e in sponsor_emails:
            uploads = Uploads.objects.filter(email_sponsor=e)
            if uploads[0].lpid_sponsor == '' and (uploads[0].email_sponsor not in ('', 'N/A')):
                lpid = self.email_to_lp(e)
                if lpid != '':
                    for ul in uploads.filter(lpid_sponsor=''):
                        ul.lpid_sponsor = lpid
                        ul.save()
            else:
                for ul in uploads.filter(lpid_sponsor=''):
                    if ul.email_sponsor not in ('', 'N/A'):
                        ul.lpid_sponsor = uploads[0].lpid_sponsor
                        ul.save()

    def email_to_lp(self, e):
        try:
            lp_person = self.launchpad.people.getByEmail(email=e)
            lpid = lp_person.name
        except:
            lpid = ''
        return lpid

    def handle_noargs(self, **options):
        self.import_uploads()
        self.add_lpids()
